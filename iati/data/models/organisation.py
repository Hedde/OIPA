from django.db import models

class IATISet(models.Model):
    organisation = models.CharField(max_length=500)
    last_updated = models.DateTimeField()

    class Meta:
        app_label = "data"


class Organisation(models.Model):
    name = models.CharField(max_length=500)
    type = models.CharField(max_length=250)
    default_currency = models.CharField(max_length=10)
    ref = models.CharField(max_length=100, unique=True)
    last_updated = models.DateTimeField()

    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.name

    class Meta:
        app_label = "data"


class BaseBudget(models.Model):
    organisation = models.ForeignKey(Organisation)
    period_start = models.DateField()
    period_end = models.DateField()
    value = models.DecimalField(max_digits=20, decimal_places=2)

    class Meta:
        abstract = True
        app_label = "data"

class RecipientCountryBudget(BaseBudget):
    country_code = models.CharField(max_length=3)
    country_name = models.CharField(max_length=255)

    def __unicode__(self):
        return '%s %s' % (self.organisation, self.country_name)

    class Meta:
        app_label = "data"

class RecipientOrgBudget(BaseBudget):
    recipient_org = models.CharField(max_length=500)
    recipient_ref = models.DecimalField(max_digits=20, decimal_places=0)

    class Meta:
        app_label = "data"

class TotalBudget(BaseBudget):
    pass

    class Meta:
        app_label = "data"


class Activity(models.Model):
    identifier = models.CharField(max_length=50, unique=True)
    organisation = models.ForeignKey(Organisation)
    title = models.CharField(max_length=500)
    description = models.TextField()
    sector = models.CharField(max_length=500)
    sector_code = models.CharField(max_length=50)
    recipient_country_code = models.CharField(max_length=3, blank=True)
    total_budget = models.DecimalField(max_digits=25, decimal_places=2, default=0)

    start_planned = models.DateField(blank=True, null=True)
    start_actual = models.DateField(blank=True, null=True)
    end_planned = models.DateField(blank=True, null=True)
    end_actual = models.DateField(blank=True, null=True)

    collaboration_type = models.CharField(max_length=500, blank=True)
    collaboration_type_code = models.CharField(max_length=50, blank=True)
    default_flow_type = models.CharField(max_length=500, blank=True)
    default_flow_type_code = models.CharField(max_length=50, blank=True)
    default_aid_type = models.CharField(max_length=500, blank=True)
    default_aid_type_code = models.CharField(max_length=50, blank=True)
    default_finance_type = models.CharField(max_length=500, blank=True)
    default_finance_code = models.CharField(max_length=50, blank=True)
    default_tied_status = models.CharField(max_length=500, blank=True)
    default_tied_status_code = models.CharField(max_length=50, blank=True)
    activity_status = models.CharField(max_length=500, blank=True)
    activity_status_code = models.CharField(max_length=50, blank=True)

    last_updated = models.DateTimeField()

    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = "data"
        verbose_name_plural = u'activities'

    def __unicode__(self):
        return self.identifier


class ParticipatingOrganisation(models.Model):
    activity = models.ForeignKey(Activity)
    name = models.CharField(max_length=500)
    role = models.CharField(max_length=500)
    type = models.CharField(max_length=250)
    ref = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name

    class Meta:
        app_label = "data"


class Transaction(models.Model):
    activity = models.ForeignKey(Activity)
    transaction_type = models.CharField(max_length=100)
    provider_org = models.CharField(max_length=250)
    receiver_org = models.CharField(max_length=100)
    value = models.DecimalField(max_digits=20, decimal_places=2)
    value_date = models.DateField()
    transaction_date = models.DateField()

    class Meta:
        app_label = "data"


class PolicyMarker(models.Model):
    """
      <xsd:element name="policy-marker">
        <xsd:annotation>
          <xsd:documentation xml:lang="en">
            A policy or theme addressed by the activity.  A text
            description of the theme appears in the content, and a formal
            identifier appears in the @ref attribute.  The @vocabulary
            attribute can also help to segment the markers into separate
            vocabularies.  This element can be repeated for each policy
            marker.  For the value of the @code attribute, see
            http://iatistandard.org/codelists/policy_marker
          </xsd:documentation>
        </xsd:annotation>
        <xsd:complexType mixed="true">
          <xsd:sequence>
            <xsd:any namespace="##other" processContents="lax" minOccurs="0" maxOccurs="unbounded"/>
          </xsd:sequence>
          <xsd:attributeGroup ref="textAtts"/>
          <xsd:attribute ref="code" use="optional"/>
          <xsd:attribute name="vocabulary" type="xsd:string" use="optional">
            <xsd:annotation>
              <xsd:documentation xml:lang="en">
                An identifier for the vocabulary in use, to segment codes
                into different vocabularies (e.g. Rio, Environment) to aid
                with comparison and classification.

                See http://iatistandard.org/codelists/vocabulary
              </xsd:documentation>
            </xsd:annotation>
          </xsd:attribute>
          <xsd:attribute name="significance" type="xsd:string" use="optional">
            <xsd:annotation>
              <xsd:documentation xml:lang="en">
                The significance of the policy marker for this activity
                (e.g. principal or significant), from a list defined by
                IATI.  If a marker is not significant, the policy-marker
                element will not be present.

                See http://iatistandard.org/codelists/policy_significance
              </xsd:documentation>
            </xsd:annotation>
          </xsd:attribute>
          <xsd:anyAttribute processContents="lax" namespace="##other"/>
        </xsd:complexType>
      </xsd:element>
    """
    activity = models.ForeignKey(Activity)
    description = models.TextField()
    vocabulary = models.CharField(max_length=32)
    significance = models.CharField(max_length=2, blank=True)
    code = models.CharField(max_length=8)

    class Meta:
        app_label = "data"