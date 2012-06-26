+---------------------+----------------+----------------+
+ Package             | Required       | Recommended    |
+---------------------+----------------+----------------+
| Django              | 1.3            | 1.4            |
| Python              | 2.6            | 2.7            |
| MySQL-python        | 1.2.3          | 1.2.3          |
| South               | 0.7.4          | 0.7.4          |
| django-tastypie     | 0.9.11         | 0.9.11         |
| lxml                | 2.3.4          | 2.3.4          |
+---------------------+----------------+----------------+

1. Create a virtualenv with the required packages
2. Create a MySQL database (utf8_unicode encoding)
3. Open bash, cd ~/yourprojectdir/iati
4. nano local_settings.py
5. configure and paste your settings:

ADMINS = (
    ('Your name', 'your_name@your_domain.com'),
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '***',
        'USER': '***',
        'PASSWORD': '***',
        'HOST': '',
        'PORT': '',
        },
    }

6. ctrl+o, enter, ctrl-x
7. python manage.py syncdb
8. python manage.py schemamigration data --initial
9. python manage.py schemamigration utils --initial
10. python manage.py migrate --fake
11. python manage.py runserver 127.0.0.1 --8080
12. Login the admin and add a country or collection file (for example http://siteresources.worldbank.org/IATI/WB-298.xml)
13. python manage.py import_iati_xml media/utils/activity_files/twb/wb-298.xml
14. curl -X GET http://127.0.0.1:8080/api/v2/activities?format=json or visit http://127.0.0.1:8080/api/v2/activities?format=json in a browser
