==========================
Compliance Test 19/06/2012
==========================
note: If there wasn't a collection file for all activities, a single country was picked randomly

@requirements:

- file link available in preview? (no xml download required)
    > link ok
- parse ok for all Models
    > parse ok

@results:

http://iatiregistry.org/publisher/unops

previous:
[ v ] link ok, parse ok
current:


http://iatiregistry.org/publisher/undp

previous:
[ v ] link ok, parse ok
current:


http://iatiregistry.org/publisher/transparency-international

previous:
[ v ] link ok, parse ok
current:


http://iatiregistry.org/publisher/worldbank

previous:
[ v ] link ok, parse ok
current:
[ v ] link ok, parse ok
comment:
    1. value-date is required on Transactions, if there wasn't a value-date the transaction-date was used.


http://iatiregistry.org/publisher/theglobalfund

previous:
[ x ] link failed, parse failed (ValueError: time data '2011-08-09' does not match format '%Y-%m-%d %H:%M:%S')
current:
[ v ] link ok, parse ok
comment:
    1. missing ref, added participating_org.get('ref', 'UNDEFINED') for exceptions

http://iatiregistry.org/publisher/sida

previous:
[ v ] link ok, parse ok
current:
[ v ] link ok, parse ok

http://iatiregistry.org/publisher/spark

previous:
[ ~ ] link ok, parse warning (building resource_uri problem, possibly due to whitespace in iati_identifier)
current:
[ v ] link ok, parse ok
comment:
    1. building resource_uri problem, added fix_whitespaces decorator for iati_identifier
    2. comma value (must be pointer for decimal), value=str(getattr(el.budget, 'value')).replace(',', '.') for exceptions @todo DRY

http://iatiregistry.org/publisher/pwyf

previous:
[ x ] link ok, parse failed (ValueError: time data '2011-11-29T00:00:00+00:00' does not match format '%Y-%m-%d+%H:%M:%S')
current:


http://iatiregistry.org/publisher/oxfamgb

previous:
[ v ] link ok, parse ok
current:
[ v ] link ok, parse ok

http://iatiregistry.org/publisher/aa

previous:
[ ~ ] link ok, parse failed, manual fix (Leading whitespace on some iati-identifier and reporting-org elements)
current:


http://iatiregistry.org/publisher/globalgiving

previous:
[ x ] link failed, parse (ValueError: time data '2010-07-23T16:18:17.000' does not match format '%Y-%m-%d %H:%M:%S')
current:
[ v ] link ok, parse ok
comment:
    missing activity-date, added hasattr(el, 'activity-date') for exceptions

http://iatiregistry.org/publisher/finland_mfa

previous:
[ v ] link ok, parse ok
current:
[ v ] link ok, parse ok

http://iatiregistry.org/publisher/eu

previous:
[ v ] link ok, parse ok
current:
[ v ] link ok, parse ok

http://iatiregistry.org/publisher/ewb_canada

previous:
[ x ] link ok, parse failed (ValueError: time data '2011-11-29T00:00:00+00:00' does not match format '%Y-%m-%d+%H:%M:%S')
current:
[ v ] link ok, parse ok
comment:
    1. missing description, added hasattr(el, 'description') for exceptions

http://iatiregistry.org/publisher/dfid

previous:
[ x ] link ok, parse failed (TypeError: strptime() argument 1 must be string, not None)
current:
[ v ] link ok, parse ok
comment:
    dateutil.parser error for format '%Y-%m-%dZ', slicing s for exceptions

http://iatiregistry.org/publisher/ausaid

previous:
[ x ] link failed, parse ? (custom upload required)
current:


http://iatiregistry.org/publisher/childhopeuk

previous:
[ v ] link ok, parse ok
current:


http://iatiregistry.org/publisher/buildafrica

previous:
[ v ] link ok, parse ok
current:


http://iatiregistry.org/publisher/hpa

previous:
[ v ] link ok, parse ok
current:


http://iatiregistry.org/publisher/lead_international

previous:
[ v ] link ok, parse ok
current:
