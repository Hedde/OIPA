Test:
- file link available in preview? (no xml download required)
- parse ok for OrganisationModel & ActivityModel (FK & relational models NOT tested!)

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
untested, connection timeout 15:58 19/06/2012
http://iatiregistry.org/publisher/finland_mfa
untested, connection timeout 15:58 19/06/2012
http://iatiregistry.org/publisher/eu
untested, connection timeout 15:58 19/06/2012
http://iatiregistry.org/publisher/ewb_canada
untested, connection timeout 15:58 19/06/2012
http://iatiregistry.org/publisher/dfid
untested, connection timeout 15:58 19/06/2012
http://iatiregistry.org/publisher/ausaid
untested, connection timeout 15:58 19/06/2012
http://iatiregistry.org/publisher/childhopeuk
untested, connection timeout 15:58 19/06/2012
http://iatiregistry.org/publisher/buildafrica
untested, connection timeout 15:58 19/06/2012
http://iatiregistry.org/publisher/hpa
untested, connection timeout 15:58 19/06/2012
http://iatiregistry.org/publisher/lead_international