from settings import rel

from datetime import datetime
from lxml import etree, objectify
from optparse import make_option
import types

# Django specific
from django.core.management import BaseCommand
from django.db.transaction import commit_on_success

# App specific
from data.models.constants import ORGANISATION_TYPE_CHOICES
from data.models.activity import IATIActivity
from data.models.common import ActivityStatusType
from data.models.organisation import Organisation


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
        try:
            return datetime.strptime(s, format)
        except ValueError:
            return datetime.strptime(s, '%Y-%m-%d %H:%M:%S')


class OrganisationParser(Parser):
    pass


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

        # Get or create Organisation
        reporting_organisation_name = el['reporting-org']
        reporting_organisation_ref = el['reporting-org'].get('ref')
        reporting_organisation_type = el['reporting-org'].get('type')

        if reporting_organisation_type:
            try:
                reporting_organisation_type = int(reporting_organisation_type)
            except ValueError:
                for k, v in ORGANISATION_TYPE_CHOICES:
                    if reporting_organisation_type == v:
                        print k
                        reporting_organisation_type = k

        organisation, created = Organisation.objects.get_or_create(
                                    ref=reporting_organisation_ref,
                                    org_name=reporting_organisation_name
                                )

        if reporting_organisation_type:
            organisation.type = reporting_organisation_type
            organisation.save()

        # Get or create IATIActivity
        iati_identifier = el['iati-identifier']
        date_updated = self._parse_datetime(el.get('last-updated-datetime'))

        iati_activity, created = IATIActivity.objects.get_or_create(
            iati_identifier=str(iati_identifier),
            reporting_organisation=organisation,
            date_updated=date_updated
        )

        if not self.force_update and iati_activity.date_updated >= date_updated:
            print "Don't override existing records"
            return

#        activity.title = unicode(el.title)
#        activity.description = unicode(el.description)
#        activity.sector = unicode(el.sector)
#        activity.sector_code = el.sector.get('code')
#        activity.flow_type = FlowType(code=1, name='test') # HARD CODE
#
#        for item in el['activity-date']:
#            name = item.get('type').replace('-', '_')
#            if hasattr(activity, name):
#                date_str = item.get('iso-date')
#                if date_str:
#                    setattr(activity, name, self._parse_date(date_str))
#
#        try:
#            activity.recipient_country_code = el['recipient-country'].get('code')
#        except AttributeError:
#            pass
#        activity.save()
#
#        # save participating-org
#        #        activity.participatingorganisation_set.all().delete()
#
#        for item in el['participating-org']:
#            self._save_participating_org(item, activity)
#
#        # save transactions
#        activity.transaction_set.all().delete()
#
#        total_budget = 0
#        for item in el.transaction:
#            tr = self._save_transaction(item, activity)
#            if tr.transaction_type == 'Commitments':
#                total_budget += float(tr.value)
#
#        activity.total_budget = str(total_budget)
#        activity.save()
#
#        # save policy-marker
#        activity.policymarker_set.all().delete()
#
#        for item in el['policy-marker']:
#            self._save_policy_marker(item, activity)
#
#    def _save_participating_org(self, el, activity):
#        if el.get('type'):
#            po = ParticipatingOrganisation(activity=activity)
#            po.name = unicode(el)
#            po.role = el.get('role')
#            po.type = el.get('type')
#            po.ref = el.get('ref')
#            po.save()
#
#    def _save_policy_marker(self, el, activity):
#        pm = PolicyMarker(activity=activity)
#        pm.description = unicode(el)
#        pm.vocabulary = unicode(el.get('vocabulary'))
#        pm.significance = unicode(el.get('significance', ''))
#        pm.code = unicode(el.get('code'))
#        pm.save()
#        return pm
#
#    def _save_transaction(self, el, activity):
#        tr = Transaction(activity=activity)
#        tr.transaction_type = el['transaction-type']
#        tr.provider_org = unicode(el['provider-org'])
#        tr.receiver_org = unicode(el['receiver-org'])
#        tr.value = el.value.text
#        tr.value_date = self._parse_date(el.value.get('value-date'))
#        tr.transaction_date = self._parse_date(el['transaction-date'].get('iso-date'))
#        tr.save()
#        return tr


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
        """
        TODO: builtin availability check for all required fields
        """
        try:
            parser_cls = self.parsers[tree.getroot().tag]
            parser_cls(tree, force_update, verbosity).parse()

        except KeyError:
            raise ImportError('Undefined document structure')

    def _parse_date(self, s, format='%Y-%m-%d'):
        return datetime.strptime(s, format).date()

    def _parse_datetime(self, s, format='%Y-%m-%dT%H:%M:%S'):
        return datetime.strptime(s, format)