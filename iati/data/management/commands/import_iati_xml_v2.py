from settings import rel

from datetime import datetime
from lxml import etree, objectify
from optparse import make_option

# Django specific
from django.core.management import BaseCommand
from django.db.transaction import commit_on_success

# App specific
from data.models.constants import COUNTRIES_TUPLE
from data.models.constants import REGION_CHOICES
from data.models.constants import FLOW_TYPE_CHOICES_MAP
from data.models.constants import ORGANISATION_TYPE_CHOICES
from data.models.constants import POLICY_MARKER_CODE_CHOICES
from data.models.constants import VOCABULARY_CHOICES_MAP
from data.models.activity import IATIActivity
from data.models.activity import IATIActivityTitle
from data.models.activity import IATIActivityDescription
from data.models.activity import IATIActivityContact
from data.models.activity import IATIActivityCountry
from data.models.activity import IATIActivityRegion
from data.models.activity import IATIActivitySector
from data.models.activity import IATIActivityPolicyMarker
from data.models.common import ActivityStatusType
from data.models.common import Country
from data.models.common import CollaborationType
from data.models.common import FlowType
from data.models.common import FinanceType
from data.models.common import AidType
from data.models.common import TiedAidStatusType
from data.models.common import Region
from data.models.common import SignificanceType
from data.models.common import VocabularyType
from data.models.common import Language
from data.models.organisation import Organisation
from data.models.organisation import ParticipatingOrganisation


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
    """
    XML PARSER IN COMPLIANCE WITH THE IATI ACTIVITY STANDARD
    source: http://iatistandard.org/activities-standard/overview

    @todo
    DRY, typo catches
    """
    def parse(self):
        count = len(self.root['iati-activity'])
        i = 0
        for el in self.root['iati-activity']:
            i += 1
#            if i % 100 == 0 and self.verbosity >= 2:
            if i % 100 == 0:
                print '%s of %s' % (i, count)
            self._save_activity(el)

    def _save_activity(self, el):
        # ====================================================================
        # IDENTIFICATION
        # ====================================================================

        # get_or_create >
        # Organisation(models.Model)
        # --------------------------------------------------------------------

        reporting_organisation_name = el['reporting-org']
        reporting_organisation_ref = el['reporting-org'].get('ref')
        reporting_organisation_type = el['reporting-org'].get('type')

        if reporting_organisation_type:
            try:
                reporting_organisation_type = int(reporting_organisation_type)
            except ValueError:
                # reverse lookup
                for k, v in ORGANISATION_TYPE_CHOICES:
                    if reporting_organisation_type == v:
                        reporting_organisation_type = k

        try:
            organisation = Organisation.objects.get(
                                                    ref=reporting_organisation_ref
                                                )
        except Organisation.DoesNotExist:
            organisation = Organisation.objects.create(
                                                    ref=reporting_organisation_ref,
                                                    org_name=reporting_organisation_name,
                                                    type=reporting_organisation_type
                                                )

        # get_or_create >
        # IATIActivity(models.Model)
        # --------------------------------------------------------------------

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

        # ====================================================================
        # BASIC ACTIVITY INFORMATION
        # ====================================================================

        # get_or_create >
        # IATIActivityTitle(models.Model)
        # @todo
        # type
        # --------------------------------------------------------------------

        iati_activity.iatiactivitytitle_set.all().delete()
        iati_activity_title = unicode(el.title).encode('UTF-8')
        iati_activity_title_type = el['title'].get('type')
        iati_activity_title_language = str(el['title'].get('{http://www.w3.org/XML/1998/namespace}lang', 'default')).lower()

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
        # --------------------------------------------------------------------

        iati_activity.iatiactivitydescription_set.all().delete()
        iati_activity_description = unicode(el.description).encode('UTF-8')
        iati_activity_description_type = el['description'].get('type')
        iati_activity_description_language = str(el['description'].get('{http://www.w3.org/XML/1998/namespace}lang', 'default')).lower()

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
        # ActivityStatusType(models.Model)
        # @todo
        # description & language
        # --------------------------------------------------------------------

        if hasattr(el, 'activity-status'):
            activity_status_name = unicode(el['activity-status'])
            activity_status_code = el['activity-status'].get('code')
            activity_status = None

            if activity_status_code:
                activity_status, created = ActivityStatusType.objects.get_or_create(
                                               code=activity_status_code
                                           )
            else:
                if activity_status_name:
                    activity_status, created = ActivityStatusType.objects.get_or_create(
                                                   name=str(activity_status_name).capitalize()
                                               )

            iati_activity.activity_status = activity_status
            iati_activity.save() # todo

        # --------------------------------------------------------------------

        for activity_date in el['activity-date']:
            if activity_date.get('type') == 'start-planned':
                iati_activity.start_planned = activity_date.get('iso-date')
            elif activity_date.get('type') == 'start-actual':
                iati_activity.start_actual = activity_date.get('iso-date')
            elif activity_date.get('type') == 'end-planned':
                iati_activity.end_planned = activity_date.get('iso-date')
            elif activity_date.get('type') == 'end-actual':
                iati_activity.end_actual = activity_date.get('iso-date')
            iati_activity.save()

        # --------------------------------------------------------------------

        iati_activity.iatiactivitycontact_set.all().delete()
        if hasattr(el, 'contact-info'):
            iati_activity_contact = IATIActivityContact.objects.create(
                                        iati_activity=iati_activity
                                    )
            if hasattr(el['contact-info'], 'organisation'):
                iati_activity_contact.organisation = el['contact-info']['organisation']
            if hasattr(el['contact-info'], 'telephone'):
                iati_activity_contact.telephone = el['contact-info']['telephone']
            if hasattr(el['contact-info'], 'email'):
                iati_activity_contact.email = el['contact-info']['email']
            if hasattr(el['contact-info'], 'mailing-address'):
                iati_activity_contact.mailing_address = el['contact-info']['mailing-address']
            iati_activity_contact.save()

        # ====================================================================
        # PARTICIPATING ORGANISATIONS
        # ====================================================================

        # get_or_create >
        # ParticipatingOrganisation(models.Model)
        # @todo
        # org_name_lang
        # --------------------------------------------------------------------

        iati_activity.participatingorganisation_set.all().delete()
        if hasattr(el, 'participating-org'):
            for participating_org in el['participating-org']:
                self._save_participating_org(participating_org, iati_activity)

        # ====================================================================
        # GEOPOLITICAL INFORMATION
        # ====================================================================

        # get_or_create >
        # IATIActivityCountry(models.Model)
        # @todo
        # lang
        # --------------------------------------------------------------------

        iati_activity.iatiactivitycountry_set.all().delete()
        if hasattr(el, 'recipient-country'):
            for recipient_country in el['recipient-country']:
                self._save_recipient_country(recipient_country, iati_activity)

        # get_or_create >
        # IATIActivityRegion(models.Model)
        # @todo
        # lang
        # --------------------------------------------------------------------

        iati_activity.iatiactivityregion_set.all().delete()
        if hasattr(el, 'recipient-region'):
            for recipient_region in el['recipient-region']:
                self._save_recipient_region(recipient_region, iati_activity)

        # ====================================================================
        # CLASSIFICATIONS
        # ====================================================================

        # get_or_create >
        # IATIActivitySector(models.Model)
        # @todo
        # percentage
        # --------------------------------------------------------------------

        iati_activity.iatiactivitysector_set.all().delete()
        if hasattr(el, 'sector'):
            for sector in el.sector:
                self._save_sector(sector, iati_activity)

        # get_or_create >
        # IATIActivityPolicyMarker(models.Model)
        # --------------------------------------------------------------------

        iati_activity.iatiactivitypolicymarker_set.all().delete()
        if hasattr(el, 'policy-marker'):
            for policy_marker in el['policy-marker']:
                if policy_marker.get('significance'):
                    try:
                        if int(policy_marker.get('significance')) in range(1, 4):
                            self._save_policy_marker(policy_marker, iati_activity)
                    except ValueError:
                        pass

        # get_or_create >
        # CollaborationType(models.Model)
        # --------------------------------------------------------------------
        if hasattr(el, 'collaboration-type'):
            collaboration_type_code = el['collaboration-type'].get('code')
            if collaboration_type_code:
                iati_activity.collaboration_type = CollaborationType.objects.get_or_create(
                                                       code=collaboration_type_code
                                                   )[0]

        # get_or_create >
        # FlowType(models.Model)
        # --------------------------------------------------------------------
        if hasattr(el, 'default-flow-type'):
            # todo catch typo
            try:
                iati_activity.default_flow_type = FlowType.objects.get_or_create(
                                                      code=int(el['default-flow-type'].get('code'))
                                                  )[0]
                iati_activity.save()
            except ValueError:
                default_flow_type = str(el['default-flow-type']).replace(' ', '_').replace('-', '_').upper()
                try:
                    iati_activity.default_flow_type = FlowType.objects.get_or_create(
                                                          code=int(default_flow_type)
                                                      )[0]
                    iati_activity.save()
                except ValueError:
                    match = None
                    for k, v in FLOW_TYPE_CHOICES_MAP:
                        if k == default_flow_type:
                            match = v
                    if match:
                        iati_activity.default_flow_type = FlowType.objects.get_or_create(
                                                              code=match
                                                          )[0]
                        iati_activity.save()
                    else:
                        pass
#                        e = "ValueError: Unsupported vocabulary_type '"+str(iati_activity_sector_vocabulary_type)+"' in VOCABULARY_CHOICES_MAP"
#                        raise Exception(e)

        # get_or_create >
        # FinanceType(models.Model)
        # --------------------------------------------------------------------

        if hasattr(el, 'default-finance-type'):
            try:
                iati_activity.default_finance_type = FinanceType.objects.get_or_create(
                                                         code=int(el['default-finance-type'].get('code'))
                                                     )[0]
                iati_activity.save()
            except ValueError:
                pass

        # get_or_create >
        # AidType(models.Model)
        # --------------------------------------------------------------------
        if hasattr(el, 'default-aid-type'):
            aid_type_code = el['default-aid-type'].get('code')
            if aid_type_code:
                iati_activity.default_aid_type = AidType.objects.get_or_create(
                    code=aid_type_code
                )[0]

        # get_or_create >
        # TiedAidStatus(models.Model)
        # --------------------------------------------------------------------
        if hasattr(el, 'default-tied-status'):
            tied_aid_status = el['default-tied-status'].get('code')
            try:
                if int(tied_aid_status) in range(3, 6):
                    iati_activity.default_aid_type = TiedAidStatusType.objects.get_or_create(
                                                         code=int(tied_aid_status)
                                                     )[0]
            except ValueError:
                pass


        # ====================================================================
        # FINANCIAL
        # ====================================================================

        # ====================================================================
        # TRANSACTION
        # ====================================================================

        # ====================================================================
        # RELATED DOCUMENTS
        # ====================================================================

        # ====================================================================
        # PERFORMANCE
        # ====================================================================


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


    def _save_recipient_country(self, recipient_country, iati_activity):
        match = None
        for key in dict(COUNTRIES_TUPLE).keys():
            if key == recipient_country.get('code'):
                match = key
        if match:
            IATIActivityCountry.objects.create(
                iati_activity=iati_activity,
                country=Country.objects.get_or_create(
                                            iso=match
                                        )[0]
            )
        else:
#            e = "ValueError: Unsupported country_iso '"+str(recipient_country.get('code'))+"' in COUNTRIES_TUPLE"
#            raise Exception(e)
            pass

    def _save_recipient_region(self, recipient_region, iati_activity):
        match = None
        for key in dict(REGION_CHOICES).keys():
            if key == int(recipient_region.get('code')):
                match = key
        if match:
            IATIActivityRegion.objects.create(
                iati_activity=iati_activity,
                region=Region.objects.get_or_create(
                                            code=match
                                        )[0]
            )
        else:
#            e = "ValueError: Unsupported country_iso '"+str(recipient_country.get('code'))+"' in REGION_CHOICES"
#            raise Exception(e)
            pass

    def _save_participating_org(self, participating_org, iati_activity):
        participating_organisation = ParticipatingOrganisation.objects.create(
            iati_activity=iati_activity
        )
        participating_organisation.org_name = unicode(participating_org).encode('UTF-8') # TODO trim spaces
        participating_organisation.ref = participating_org.get('ref')
        participating_organisation.role = participating_org.get('role')

        participating_organisation_type = participating_org.get('type')
        if participating_organisation_type:
            try:
                participating_organisation.type = int(participating_organisation_type)
            except ValueError:
                # reverse lookup
                for k, v in ORGANISATION_TYPE_CHOICES:
                    if participating_organisation_type == v:
                        participating_organisation.type = k
            participating_organisation.save()

    def _save_policy_marker(self, policy_marker, iati_activity):
        policy = None
        policy_significance_type = SignificanceType.objects.get_or_create(
                                       code=int(policy_marker.get('significance'))
                                   )[0]
        try:
            policy_code = int(policy_marker.get('code'))
            if policy_code in dict(POLICY_MARKER_CODE_CHOICES).keys():
                policy = IATIActivityPolicyMarker.objects.create(
                             iati_activity=iati_activity,
                             code=policy_code,
                             significance_type=policy_significance_type
                         )

        except ValueError:
            pass

        vocabulary_type = str(policy_marker.get('vocabulary')).replace(' ', '_').replace('-', '_')
        if vocabulary_type and policy:
            try:
                policy.vocabulary_type = int(vocabulary_type)
            except ValueError:
                match = None
                for key in dict(VOCABULARY_CHOICES_MAP).keys():
                    if key == vocabulary_type:
                        match = key
                if match:
                    policy.vocabulary_type = match
                else:
                    pass
#                    e = "ValueError: Unsupported vocabulary_type '"+str(iati_activity_sector_vocabulary_type)+"' in VOCABULARY_CHOICES_MAP"
#                    raise Exception(e)

    def _save_sector(self, sector, iati_activity):
        iati_activity_sector_code = sector.get('code')
        iati_activity_sector_vocabulary_type = str(sector.get('vocabulary')).replace(' ', '_').replace('-', '_')

        activity_sector, created = IATIActivitySector.objects.get_or_create(
            iati_activity=iati_activity,
            code=iati_activity_sector_code
        )

        if iati_activity_sector_vocabulary_type:
            try:
                iati_activity_sector_vocabulary_type = int(iati_activity_sector_vocabulary_type)
                activity_sector.vocabulary_type = VocabularyType.objects.get_or_create(
                    code=iati_activity_sector_vocabulary_type
                )[0]
                activity_sector.save()
            except ValueError:
                match = None
                for key in dict(VOCABULARY_CHOICES_MAP).keys():
                    if key == iati_activity_sector_vocabulary_type:
                        match = key
                if match:
                    iati_activity_sector_vocabulary_type = match
                    activity_sector.vocabulary_type = VocabularyType.objects.get_or_create(
                        code=iati_activity_sector_vocabulary_type
                    )[0]
                    activity_sector.save()
                else:
                    pass
                #                    e = "ValueError: Unsupported vocabulary_type '"+str(iati_activity_sector_vocabulary_type)+"' in VOCABULARY_CHOICES_MAP"
                #                    raise Exception(e)
        return


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