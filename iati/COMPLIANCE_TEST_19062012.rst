==========================
Compliance Test 19/06/2012
==========================
note: If there wasn't a collection file for all activities, a single country was picked randomly

@requirements:

- file link available in preview? (no xml download required)
    > link ok
- parse ok for OrganisationModel & ActivityModel (FK & relational models NOT tested!)
    > parse ok

@results:

http://iatiregistry.org/publisher/unops
[ v ] link ok, parse ok

http://iatiregistry.org/publisher/undp
[ v ] link ok, parse ok

http://iatiregistry.org/publisher/transparency-international
[ v ] link ok, parse ok

http://iatiregistry.org/publisher/worldbank
[ v ] link ok, parse ok

http://iatiregistry.org/publisher/theglobalfund
[ x ] link failed, parse ? (custom upload required)

http://iatiregistry.org/publisher/sida
[ v ] link ok, parse ok

http://iatiregistry.org/publisher/spark
[ ~ ] link ok, parse warning (building resource_uri problem, possibly due to whitespace in iati_identifier)

http://iatiregistry.org/publisher/pwyf
[ x ] link ok, parse failed (ValueError: time data '2011-11-29T00:00:00+00:00' does not match format '%Y-%m-%d+%H:%M:%S')

http://iatiregistry.org/publisher/oxfamgb
[ v ] link ok, parse ok

http://iatiregistry.org/publisher/aa
[ ~ ] link ok, parse failed, manual fix (Leading whitespace on some iati-identifier and reporting-org elements)

http://iatiregistry.org/publisher/globalgiving
[ x ] link failed, parse ? (custom upload required)

http://iatiregistry.org/publisher/finland_mfa
[ v ] link ok, parse ok

http://iatiregistry.org/publisher/eu
[ v ] link ok, parse ok

http://iatiregistry.org/publisher/ewb_canada
[ x ] link ok, parse failed (ValueError: time data '2011-11-29T00:00:00+00:00' does not match format '%Y-%m-%d+%H:%M:%S')

http://iatiregistry.org/publisher/dfid
[ x ] link ok, parse failed (TypeError: strptime() argument 1 must be string, not None)

http://iatiregistry.org/publisher/ausaid
[ x ] link failed, parse ? (custom upload required)

http://iatiregistry.org/publisher/childhopeuk
[ v ] link ok, parse ok

http://iatiregistry.org/publisher/buildafrica
[ v ] link ok, parse ok

http://iatiregistry.org/publisher/hpa
[ v ] link ok, parse ok

http://iatiregistry.org/publisher/lead_international
[ v ] link ok, parse ok