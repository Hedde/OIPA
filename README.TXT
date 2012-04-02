OIPA: OpenAid IATI parser and API
============

Technology developed within the openaid.nl platform enables IATI standard compliant datasets to easily parse and interface that data using the OIPA framework that has been developed. So what is IATI? IATI is a global aid transparency standard and it makes information about aid spending easier to access, use and understand using a unified open standard. You can find more about IATA standard at: 

http://iatistandard.org/

OIPA has an open-source license, meaning you can download the package from Github under the AGPL license. 

We have interfaced the IATI set of the Dutch ministry of foreign affairs at: http://search-api.openaid.nl/whereaid_api/ or take a look at its documentation here: http://search-api-data.openaid.nl/api/documentation/ and play around with it using this URL: http://search-api-data.openaid.nl/api/data/activity/ - create some REST calls yourself and see how it works.

============
Use:

python manage.py import_iati_xml ../IATI_ORGANISATIONS_XXXXX_XXXX.xml ../IATI_ACTIVITIES_XXXXX_XXXX.xml

