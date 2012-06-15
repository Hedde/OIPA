from django.utils.translation import ugettext_lazy as _


TYPE_CHOICES = (
    (10, _(u"Government")),
    (15, _(u"Other Public Sector")),
    (21, _(u"International NGO")),
    (22, _(u"National NGO")),
    (23, _(u"Regional NGO")),
    (30, _(u"Public Private Partnership")),
    (40, _(u"Multilateral")),
    (60, _(u"Foundation")),
    (70, _(u"Private Sector")),
    (80, _(u"Academic, Training and Research")),
)

REGION_CHOICES = (
    (89, _(u"Europe, regional")),
    (189, _(u"North of Sahara, regional")),
    (289, _(u"South of Sahara, regional")),
    (298, _(u"Africa, regional")),
    (380, _(u"West Indies, regional")),
    (389, _(u"North and Central America, regional")),
    (489, _(u"South America, regional")),
    (498, _(u"America, regional")),
    (589, _(u"Middle East, regional")),
    (619, _(u"Central Asia, regional")),
    (679, _(u"South Asia, regional")),
    (689, _(u"Far East Asia, regional")),
    (789, _(u"Asia, regional")),
    (798, _(u"Oceania, regional")),
    (998, _(u"Bilateral, unspecified")),
)

COUNTRY_ISO_MAP = {u'WF': _(u'Wallis and Futuna Islands'), u'JP': _(u'Japan'), u'JM': _(u'Jamaica'), u'JO': _(u'Jordan'), u'WS': _(u'Samoa'), u'JE': _(u'Jersey'), u'GW': u'Guinea-Bissau', u'GU': _(u'Guam'), u'GT': _(u'Guatemala'), u'GS': _(u'South Georgia South Sandwich Islands'), u'GR': _(u'Greece'), u'GQ': _(u'Equatorial Guinea'), u'GP': _(u'Guadeloupe'), u'GY': _(u'Guyana'), u'GG': _(u'Guernsey'), u'GF': _(u'French Guiana'), u'GE': _(u'Georgia'), u'GD': _(u'Grenada'), u'GB': _(u'United Kingdom'), u'GA': _(u'Gabon'), u'GN': _(u'Guinea'), u'GM': _(u'Gambia'), u'GL': _(u'Greenland'), u'GI': _(u'Gibraltar'), u'GH': _(u'Ghana'), u'PR': _(u'Puerto Rico'), u'PS': _(u'Palestine'), u'PW': _(u'Palau'), u'PT': _(u'Portugal'), u'PY': _(u'Paraguay'), u'PA': _(u'Panama'), u'PF': _(u'French Polynesia'), u'PG': _(u'Papua New Guinea'), u'PE': _(u'Peru'), u'PK': _(u'Pakistan'), u'PH': _(u'Philippines'), u'PN': _(u'Pitcairn Islands'), u'PL': _(u'Poland'), u'PM': _(u'Saint Pierre and Miquelon'), u'ZM': _(u'Zambia'), u'ZA': _(u'South Africa'), u'ZW': _(u'Zimbabwe'), u'ME': _(u'Montenegro'), u'MD': _(u'Republic of Moldova'), u'MG': _(u'Madagascar'), u'MF': _(u'Saint Martin'), u'MA': _(u'Morocco'), u'MC': _(u'Monaco'), u'MM': _(u'Burma'), u'ML': _(u'Mali'), u'MO': _(u'Macau'), u'MN': _(u'Mongolia'), u'MH': _(u'Marshall Islands'), u'MK': _(u'The former Yugoslav Republic of Macedonia'), u'MU': _(u'Mauritius'), u'MT': _(u'Malta'), u'MW': _(u'Malawi'), u'MV': _(u'Maldives'), u'MQ': _(u'Martinique'), u'MP': _(u'Northern Mariana Islands'), u'MS': _(u'Montserrat'), u'MR': _(u'Mauritania'), u'MY': _(u'Malaysia'), u'MX': _(u'Mexico'), u'MZ': _(u'Mozambique'), u'FR': _(u'France'), u'FI': _(u'Finland'), u'FJ': _(u'Fiji'), u'FK': u'Falkland Islands (Malvinas)', u'FM': u'Micronesia, Federated States of', u'FO': _(u'Faroe Islands'), u'CK': _(u'Cook Islands'), u'CI': u"Cote d'Ivoire", u'CH': _(u'Switzerland'), u'CO': _(u'Colombia'), u'CN': _(u'China'), u'CM': _(u'Cameroon'), u'CL': _(u'Chile'), u'CC': u'Cocos (Keeling) Islands', u'CA': _(u'Canada'), u'CG': _(u'Congo'), u'CF': _(u'Central African Republic'), u'CD': _(u'Democratic Republic of the Congo'), u'CZ': _(u'Czech Republic'), u'CY': _(u'Cyprus'), u'CX': _(u'Christmas Island'), u'CR': _(u'Costa Rica'), u'CV': _(u'Cape Verde'), u'CU': _(u'Cuba'), u'SZ': _(u'Swaziland'), u'SY': _(u'Syrian Arab Republic'), u'SR': _(u'Suriname'), u'SV': _(u'El Salvador'), u'ST': _(u'Sao Tome and Principe'), u'SK': _(u'Slovakia'), u'SJ': _(u'Svalbard'), u'SI': _(u'Slovenia'), u'SH': _(u'Saint Helena'), u'SO': _(u'Somalia'), u'SN': _(u'Senegal'), u'SM': _(u'San Marino'), u'SL': _(u'Sierra Leone'), u'SC': _(u'Seychelles'), u'SB': _(u'Solomon Islands'), u'SA': _(u'Saudi Arabia'), u'SG': _(u'Singapore'), u'SE': _(u'Sweden'), u'SD': _(u'Sudan'), u'YE': _(u'Yemen'), u'YT': _(u'Mayotte'), u'LB': _(u'Lebanon'), u'LC': _(u'Saint Lucia'), u'LA': u"Lao People's Democratic Republic", u'LK': _(u'Sri Lanka'), u'LI': _(u'Liechtenstein'), u'LV': _(u'Latvia'), u'LT': _(u'Lithuania'), u'LU': _(u'Luxembourg'), u'LR': _(u'Liberia'), u'LS': _(u'Lesotho'), u'LY': _(u'Libyan Arab Jamahiriya'), u'VA': u'Holy See (Vatican City)', u'VC': _(u'Saint Vincent and the Grenadines'), u'VE': _(u'Venezuela'), u'VG': _(u'British Virgin Islands'), u'IQ': _(u'Iraq'), u'VI': _(u'United States Virgin Islands'), u'IS': _(u'Iceland'), u'IR': u'Iran (Islamic Republic of)', u'IT': _(u'Italy'), u'VN': _(u'Viet Nam'), u'IM': _(u'Isle of Man'), u'VU': _(u'Vanuatu'), u'IO': _(u'British Indian Ocean Territory'), u'IN': _(u'India'), u'IE': _(u'Ireland'), u'ID': _(u'Indonesia'), u'BD': _(u'Bangladesh'), u'BE': _(u'Belgium'), u'BF': _(u'Burkina Faso'), u'BG': _(u'Bulgaria'), u'BA': _(u'Bosnia and Herzegovina'), u'BB': _(u'Barbados'), u'BL': _(u'Saint Barthelemy'), u'BM': _(u'Bermuda'), u'BN': _(u'Brunei Darussalam'), u'BO': _(u'Bolivia'), u'BH': _(u'Bahrain'), u'BI': _(u'Burundi'), u'BJ': _(u'Benin'), u'BT': _(u'Bhutan'), u'BV': _(u'Bouvet Island'), u'BW': _(u'Botswana'), u'BR': _(u'Brazil'), u'BS': _(u'Bahamas'), u'BY': _(u'Belarus'), u'BZ': _(u'Belize'), u'RU': _(u'Russia'), u'RW': _(u'Rwanda'), u'RS': _(u'Serbia'), u'RE': _(u'Reunion'), u'RO': _(u'Romania'), u'OM': _(u'Oman'), u'HR': _(u'Croatia'), u'HT': _(u'Haiti'), u'HU': _(u'Hungary'), u'HK': _(u'Hong Kong'), u'HN': _(u'Honduras'), u'HM': _(u'Heard Island and McDonald Islands'), u'EH': _(u'Western Sahara'), u'EE': _(u'Estonia'), u'EG': _(u'Egypt'), u'EC': _(u'Ecuador'), u'ET': _(u'Ethiopia'), u'ES': _(u'Spain'), u'ER': _(u'Eritrea'), u'UY': _(u'Uruguay'), u'UZ': _(u'Uzbekistan'), u'US': _(u'United States'), u'UM': _(u'United States Minor Outlying Islands'), u'UG': _(u'Uganda'), u'UA': _(u'Ukraine'), u'IL': _(u'Israel'), u'NI': _(u'Nicaragua'), u'NL': _(u'Netherlands'), u'NO': _(u'Norway'), u'NA': _(u'Namibia'), u'NC': _(u'New Caledonia'), u'NE': _(u'Niger'), u'NF': _(u'Norfolk Island'), u'NG': _(u'Nigeria'), u'NZ': _(u'New Zealand'), u'NP': _(u'Nepal'), u'NR': _(u'Nauru'), u'NU': _(u'Niue'), u'XK': _(u'Kosovo'), u'KG': _(u'Kyrgyzstan'), u'KE': _(u'Kenya'), u'KI': _(u'Kiribati'), u'KH': _(u'Cambodia'), u'KN': _(u'Saint Kitts and Nevis'), u'KM': _(u'Comoros'), u'KR': u'Korea, Republic of', u'KP': u"Korea, Democratic People's Republic of", u'KW': _(u'Kuwait'), u'KZ': _(u'Kazakhstan'), u'KY': _(u'Cayman Islands'), u'DO': _(u'Dominican Republic'), u'DM': _(u'Dominica'), u'DJ': _(u'Djibouti'), u'DK': _(u'Denmark'), u'DE': _(u'Germany'), u'DZ': _(u'Algeria'), u'TZ': _(u'United Republic of Tanzania'), u'TV': _(u'Tuvalu'), u'TW': _(u'Taiwan'), u'TT': _(u'Trinidad and Tobago'), u'TR': _(u'Turkey'), u'TN': _(u'Tunisia'), u'TO': _(u'Tonga'), u'TL': u'Timor-Leste', u'TM': _(u'Turkmenistan'), u'TJ': _(u'Tajikistan'), u'TK': _(u'Tokelau'), u'TH': _(u'Thailand'), u'TF': _(u'French Southern and Antarctic Lands'), u'TG': _(u'Togo'), u'TD': _(u'Chad'), u'TC': _(u'Turks and Caicos Islands'), u'AE': _(u'United Arab Emirates'), u'AD': _(u'Andorra'), u'AG': _(u'Antigua and Barbuda'), u'AF': _(u'Afghanistan'), u'AI': _(u'Anguilla'), u'AM': _(u'Armenia'), u'AL': _(u'Albania'), u'AO': _(u'Angola'), u'AN': _(u'Netherlands Antilles'), u'AQ': _(u'Antarctica'), u'AS': _(u'American Samoa'), u'AR': _(u'Argentina'), u'AU': _(u'Australia'), u'AT': _(u'Austria'), u'AW': _(u'Aruba'), u'AX': u'Aland Islands', u'AZ': _(u'Azerbaijan'), u'QA': _(u'Qatar')}

COUNTRIES_TUPLE = (
    COUNTRY_ISO_MAP.items()
)
