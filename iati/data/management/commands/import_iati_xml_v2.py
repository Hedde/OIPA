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
from data.models.constants import VOCABULARY_CHOICES_MAP
from data.models.activity import IATIActivity
from data.models.activity import IATIActivityTitle
from data.models.activity import IATIActivityDescription
from data.models.activity import IATIActivitySector
from data.models.common import ActivityStatusType
from data.models.common import VocabularyType
from data.models.common import Language
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
        # get_or_create >
        # Organisation(models.Model)
        reporting_organisation_name = el['reporting-org']
        reporting_organisation_ref = el['reporting-org'].get('ref')
        reporting_organisation_type = el['reporting-org'].get('type')

        if reporting_organisation_type:
            try:
                reporting_organisation_type = int(reporting_organisation_type)
            except ValueError:
                for k, v in ORGANISATION_TYPE_CHOICES:
                    if reporting_organisation_type == v:
                        reporting_organisation_type = k

        organisation, created = Organisation.objects.get_or_create(
                                    ref=reporting_organisation_ref,
                                    org_name=reporting_organisation_name,
                                    type=reporting_organisation_type
                                )

        # get_or_create >
        # IATIActivity(models.Model)
        iati_identifier = str(el['iati-identifier'])
        date_updated = self._parse_datetime(el.get('last-updated-datetime'))

        iati_activity, created = IATIActivity.objects.get_or_create(
                                     iati_identifier=iati_identifier,
                                     reporting_organisation=organisation,
                                     date_updated=date_updated
                                 )

#        if not self.force_update and iati_activity.date_updated >= date_updated:
#            print "Don't override existing records"
#            return

        # get_or_create >
        # ActivityStatusType(models.Model)
        # @todo
        # description & language
        activity_status_name = el['activity-status']
        activity_status_code = el['activity-status'].get('code')

        if activity_status_name:
            activity_status, created = ActivityStatusType.objects.get_or_create(
                                           name=str(activity_status_name).capitalize()
                                       )
            if activity_status_code:
                activity_status.code = activity_status_code
                activity_status.save()

            iati_activity.activity_status = activity_status
            iati_activity.save() # todo

        # get_or_create >
        # IATIActivityTitle(models.Model)
        # @todo
        # type
        iati_activity_title = unicode(el.title)
        iati_activity_title_type = el['title'].get('type')
        iati_activity_title_language = str(el['title'].get('{http://www.w3.org/XML/1998/namespace}lang')).lower()

        activity_title, created = IATIActivityTitle.objects.get_or_create(
                                      iati_activity=iati_activity,
                                      title=iati_activity_title
                                  )
        if iati_activity_title_language:
            activity_title.language = Language.objects.get_or_create(
                                          code=iati_activity_title_language
                                      )[0]
            activity_title.save()

        # get_or_create >
        # IATIActivityDescription(models.Model)
        # @todo
        # type
        iati_activity_description = unicode(el.description)
        iati_activity_description_type = el['description'].get('type')
        iati_activity_description_language = str(el['description'].get('{http://www.w3.org/XML/1998/namespace}lang')).lower()

        activity_description, created = IATIActivityDescription.objects.get_or_create(
                                            iati_activity=iati_activity,
                                            description=iati_activity_description
                                        )
        if iati_activity_description_language:
            activity_description.language = Language.objects.get_or_create(
                                                code=iati_activity_description_language
                                            )[0]
            activity_description.save()


        # get_or_create >
        # IATIActivitySector(models.Model)
        # @todo
        # percentage
        iati_activity_sector_code = el['sector'].get('code')
        iati_activity_sector_vocabulary_type = str(el['sector'].get('vocabulary')).replace(' ', '_').replace('-', '_')

        activity_sector, created = IATIActivitySector.objects.get_or_create(
                                       iati_activity=iati_activity,
                                       code=iati_activity_sector_code
                                   )

        if iati_activity_sector_vocabulary_type:
            try:
                iati_activity_sector_vocabulary_type = int(iati_activity_sector_vocabulary_type)
            except ValueError:
                for k, v in VOCABULARY_CHOICES_MAP:
                    if k == iati_activity_sector_vocabulary_type:
                        iati_activity_sector_vocabulary_type = v

            activity_sector.vocabulary_type = VocabularyType.objects.get_or_create(
                                                  code=iati_activity_sector_vocabulary_type
                                              )[0]
            activity_sector.save()


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
        @todo
        > builtin availability check for all required fields
        > commit_on_succes / transaction save impl
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