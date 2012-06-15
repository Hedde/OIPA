from django.core.management import BaseCommand
from settings import rel
from lxml import etree, objectify
from data.models.organisation import Organisation, RecipientCountryBudget, RecipientOrgBudget,\
    TotalBudget, Activity, Transaction, PolicyMarker, ParticipatingOrganisation,\
    IATISet
from datetime import datetime
from optparse import make_option
from django.db.transaction import commit_on_success


class ImportError(Exception):
    pass


class Parser(object):

    def __init__(self, tree, force_update=False, verbosity=2):
        self.tree = tree
        self.root = tree.getroot()
        self.force_update = force_update
        self.verbosity = verbosity

    def _parse_date(self, s, format='%Y-%m-%d'):
        return datetime.strptime(s, format).date()

    def _parse_datetime(self, s, format='%Y-%m-%dT%H:%M:%S'):
        return datetime.strptime(s, format)


class OrganisationParser(Parser):

    def parse(self):
        count = len(self.root['iati-organisation'])
        i = 0
        for el in self.root['iati-organisation']:
            i += 1
            if i % 10 == 0 and self.verbosity >= 2:
                print '%s of %s' % (i, count)
            self._save_organisation(el)

    def _save_organisation(self, el):
        ref = el['reporting-org'].get('ref')
        last_updated = self._parse_datetime(el.get('last-updated-datetime'))

        try:
            org = Organisation.objects.get(ref=ref)
            if not self.force_update and org.last_updated >= last_updated:
                return
        except Organisation.DoesNotExist:
            org = Organisation(ref=ref, last_updated=last_updated)

        org.name = unicode(el.name)
        org.default_currency = el.get('default-currency')
        org.type = unicode(el['reporting-org'].get('type'))
        org.save()

        org.recipientcountrybudget_set.all().delete()

        for item in el['recipient-country-budget']:
            obj = RecipientCountryBudget(organisation=org)
            self._parse_base_budget(item, obj)
            obj.country_code = item['recipient-country'].get('code')
            obj.country_name = unicode(item['recipient-country'])
            obj.save()

        org.recipientorgbudget_set.all().delete()

        for item in el['recipient-org-budget']:
            obj = RecipientOrgBudget(organisation=org)
            self._parse_base_budget(item, obj)
            obj.recipient_org = unicode(item['recipient-org'])
            obj.recipient_ref = item['recipient-org'].get('ref')
            obj.save()

        org.totalbudget_set.all().delete()

        for item in el['total-budget']:
            obj = TotalBudget(organisation=org)
            self._parse_base_budget(item, obj)
            obj.save()

    def _parse_base_budget(self, el, obj):
        period_start = self._parse_date(el['period-start'].get('iso-date'))
        if el['period-start']:
            period_start.replace(year=el['period-start'])
        obj.period_start = period_start

        period_end = self._parse_date(el['period-end'].get('iso-date'))
        if el['period-end']:
            period_end.replace(year=el['period-end'])
        obj.period_end = period_end

        obj.value = el.value.text


class ActivityParser(Parser):

    def parse(self):
        count = len(self.root['iati-activity'])
        i = 0
        for el in self.root['iati-activity']:
            i += 1
            if i % 100 == 0 and self.verbosity >= 2:
                print '%s of %s' % (i, count)
            self._save_activity(el)

    def _save_activity(self, el):
        identifier = el['iati-identifier']
        last_updated = self._parse_datetime(el.get('last-updated-datetime'))

        try:
            activity = Activity.objects.get(identifier=identifier)
            if not self.force_update and activity.last_updated >= last_updated:
                return
        except Activity.DoesNotExist:
            activity = Activity(identifier=identifier, last_updated=last_updated)

        org_ref = el['reporting-org'].get('ref')

        try:
            activity.organisation = Organisation.objects.get(ref=org_ref)
        except Organisation.DoesNotExist:
            print 'Activity organisation does not exist'
            return

        activity.title = unicode(el.title)
        activity.description = unicode(el.description)
        activity.sector = unicode(el.sector)
        activity.sector_code = el.sector.get('code')

        for item in el['activity-date']:
            name = item.get('type').replace('-', '_')
            if hasattr(activity, name):
                date_str = item.get('iso-date')
                if date_str:
                    setattr(activity, name, self._parse_date(date_str))

        fields = ['collaboration-type', 'default-flow-type', 'default-aid-type',
                  'default-finance-type', 'default-tied-status', 'activity-status']

        for name in fields:
            field_name = name.replace('-', '_')
            code_field_name = field_name + '_code'
            setattr(activity, field_name, unicode(el[name]))
            setattr(activity, code_field_name, el[name].get('code') or '')

        try:
            activity.recipient_country_code = el['recipient-country'].get('code')
        except AttributeError:
            pass
        activity.save()

        # save participating-org

        activity.participatingorganisation_set.all().delete()

        for item in el['participating-org']:
            self._save_participating_org(item, activity)

        # save transactions
        activity.transaction_set.all().delete()

        total_budget = 0
        for item in el.transaction:
            tr = self._save_transaction(item, activity)
            if tr.transaction_type == 'Commitments':
                total_budget += float(tr.value)

        activity.total_budget = str(total_budget)
        activity.save()

        # save policy-marker
        activity.policymarker_set.all().delete()

        for item in el['policy-marker']:
            self._save_policy_marker(item, activity)

    def _save_participating_org(self, el, activity):
        if el.get('type'):
            po = ParticipatingOrganisation(activity=activity)
            po.name = unicode(el)
            po.role = el.get('role')
            po.type = el.get('type')
            po.ref = el.get('ref')
            po.save()

    def _save_policy_marker(self, el, activity):
        pm = PolicyMarker(activity=activity)
        pm.description = unicode(el)
        pm.vocabulary = unicode(el.get('vocabulary'))
        pm.significance = unicode(el.get('significance', ''))
        pm.code = unicode(el.get('code'))
        pm.save()
        return pm

    def _save_transaction(self, el, activity):
        tr = Transaction(activity=activity)
        tr.transaction_type = el['transaction-type']
        tr.provider_org = unicode(el['provider-org'])
        tr.receiver_org = unicode(el['receiver-org'])
        tr.value = el.value.text
        tr.value_date = self._parse_date(el.value.get('value-date'))
        tr.transaction_date = self._parse_date(el['transaction-date'].get('iso-date'))
        tr.save()
        return tr


class Command(BaseCommand):
    parsers = {
        'iati-organisations': OrganisationParser,
        'iati-activities': ActivityParser
    }

    option_list = BaseCommand.option_list + (
        make_option('-U', '--force-update',
            action='store_true',
            dest='force_update',
            default=False,
            help='Force saving information and ignore last-updated-datetime'),
        )

    def handle(self, *args, **options):
        force_update = options.get('force_update')
        verbosity = int(options.get('verbosity'))

        for item in args:
            print '=====', item, '====='
            try:
                f = open(rel(item))
                tree = objectify.parse(f)
                self.save(tree, force_update, verbosity)
                f.close()
            except UnicodeEncodeError, e:
                print type(e).__name__, ':', e
                print 'Text: ', e.args[1]
                #except Exception, e:
                #    print type(e).__name__, ':', e

    @commit_on_success
    def save(self, tree, force_update=False, verbosity=2):
        try:
            parser_cls = self.parsers[tree.getroot().tag]
            parser_cls(tree, force_update, verbosity).parse()
            try:
                iatiset = IATISet.objects.get(organisation='Dutch Government')
            except IATISet.DoesNotExist:
                IATISet.objects.create(organisation='Dutch Government', last_updated=datetime.now())
            else:
                iatiset.last_updated = datetime.now()
                iatiset.save()
        except KeyError:
            raise ImportError('Undefined document structure')

    def _parse_date(self, s, format='%Y-%m-%d'):
        return datetime.strptime(s, format).date()

    def _parse_datetime(self, s, format='%Y-%m-%dT%H:%M:%S'):
        return datetime.strptime(s, format)