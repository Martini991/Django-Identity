import os
import saml2
from saml2.md import SamlBase
from saml2.saml import (NAMEID_FORMAT_PERSISTENT,
                        NAMEID_FORMAT_TRANSIENT,
                        NAMEID_FORMAT_UNSPECIFIED)
from saml2.sigver import get_xmlsec_binary

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

BASE = 'http://sp1.testunical.it:8000'
BASE_URL = '{}/saml2'.format(BASE)

LOGIN_URL = '/spid/login/'
# LOGOUT_URL = '/saml2/logout/'
LOGOUT_URL = '/logout/'


SPID_DEFAULT_BINDING = saml2.BINDING_HTTP_POST
SPID_DIG_ALG = saml2.xmldsig.DIGEST_SHA256
SPID_SIG_ALG = saml2.xmldsig.SIG_RSA_SHA256
SPID_NAMEID_FORMAT = NAMEID_FORMAT_TRANSIENT
SPID_AUTH_CONTEXT = 'https://www.spid.gov.it/SpidL1'

# Avviso 29v3
SPID_PREFIXES = dict(
    spid = "https://spid.gov.it/saml-extensions",
    fpa = "https://spid.gov.it/invoicing-extensions"
)

# other or billing, not together at the same time!
SPID_CONTACTS = [
    # {
    # 'contact_type': 'other',
    # 'telephone_number': '+39 8475634785',
    # 'email_address': 'tech-info@example.org',
    # 'VATNumber': 'IT12345678901',
    # 'FiscalCode': 'XYZABCAAMGGJ000W',
    # 'Private': ''
    # },
    # {
    # 'contact_type': 'other',
    # 'telephone_number': '+39 84756344785',
    # 'email_address': 'info@example.org',
    # 'VATNumber': 'IT12345678901',
    # 'FiscalCode': 'XYasdasdadasdGGJ000W',
    # 'Private': ''
    # },
    {
    'contact_type': 'billing',
    'telephone_number': '+39 84756344785',
    'email_address': 'info@example.org',
    'company': 'example s.p.a.',
    # 'CodiceFiscale': 'NGLMRA80A01D086T',
    'IdCodice': '983745349857',
    'IdPaese': 'IT',
    'Denominazione': 'Destinatario Fatturazione',
    'Indirizzo': 'via tante cose',
    'NumeroCivico': '12',
    'CAP': '87100',
    'Comune': 'Cosenza',
    'Provincia': 'CS',
    'Nazione': 'IT',
    },
]

SAML_CONFIG = {
    'debug' : True,
    'xmlsec_binary': get_xmlsec_binary(['/opt/local/bin',
                                        '/usr/bin/xmlsec1']),
    'entityid': '%s/metadata/' % BASE_URL,

    'attribute_map_dir': os.path.join(os.path.join(os.path.join(BASE_DIR,
                                                                'djangosaml2_spid'),
                                      'saml2_config/'),
                                      'attribute-maps'),

    'service': {
        'sp': {
            'name': '%s/metadata/' % BASE_URL,

            'name_qualifier': BASE,
            # SPID needs NAMEID_FORMAT_TRANSIENT
            'name_id_format': [SPID_NAMEID_FORMAT],

            'endpoints': {
                'assertion_consumer_service': [
                    ('%s/acs/' % BASE_URL, SPID_DEFAULT_BINDING),
                    ],
                "single_logout_service": [
                    ("%s/ls/post/" % BASE_URL, saml2.BINDING_HTTP_POST),
                    ("%s/ls/" % BASE_URL, saml2.BINDING_HTTP_REDIRECT),
                ],
                }, # end endpoints

            # Mandates that the identity provider MUST authenticate the
            # presenter directly rather than rely on a previous security context.
            "force_authn": False, # SPID
            'name_id_format_allow_create': False,

            # attributes that this project need to identify a user
            'required_attributes': ['spidCode',
                                    'name',
                                    'familyName',
                                    'fiscalNumber',
                                    'email'],

            'requested_attribute_name_format': saml2.saml.NAME_FORMAT_BASIC,
            'name_format': saml2.saml.NAME_FORMAT_BASIC,
            #

            # attributes that may be useful to have but not required
            'optional_attributes': ['gender',
                                    'companyName',
                                    'registeredOffice',
                                    'ivaCode',
                                    'idCard',
                                    'digitalAddress',
                                    'placeOfBirth',
                                    'countyOfBirth',
                                    'dateOfBirth',
                                    'address',
                                    'mobilePhone',
                                    'expirationDate'],

            'signing_algorithm':  saml2.xmldsig.SIG_RSA_SHA256,
            'digest_algorithm':  saml2.xmldsig.DIGEST_SHA256,
            
            'authn_requests_signed': True,
            'logout_requests_signed': True,
            # Indicates that Authentication Responses to this SP must
            # be signed. If set to True, the SP will not consume
            # any SAML Responses that are not signed.
            'want_assertions_signed': True,

            # When set to true, the SP will consume unsolicited SAML
            # Responses, i.e. SAML Responses for which it has not sent
            # a respective SAML Authentication Request.
            'allow_unsolicited': False,

            # Permits to have attributes not configured in attribute-mappings
            # otherwise...without OID will be rejected
            'allow_unknown_attributes': True,

            }, # end sp

    },

    # many metadata, many idp...
    'metadata': {
        # 'local': [os.path.join(os.path.join(os.path.join(BASE_DIR, 'djangosaml2_spid'),
                  # 'saml2_config'), 'idp_metadata.xml'),
                  # os.path.join(os.path.join(os.path.join(BASE_DIR, 'saml2_sp'),
                  # 'saml2_config'), 'idp_metadata.xml'),
                  # other here...
                  # ],
        #
        "remote": [{
            "url":"http://localhost:8080/metadata.xml",
            }]
    },

    # Signing
    'key_file': f'{BASE_DIR}/certificates/private.key',
    'cert_file': f'{BASE_DIR}/certificates/public.cert',

    # Encryption
    'encryption_keypairs': [{
        'key_file': f'{BASE_DIR}/certificates/private.key',
        'cert_file': f'{BASE_DIR}/certificates/public.cert',
    }],

    # you can set multilanguage information here
    'organization': {
      'name': [('Example', 'it'), ('Example', 'en')],
      'display_name': [('Example', 'it'), ('Example', 'en')],
      'url': [('http://www.example.it', 'it'), ('http://www.example.it', 'en')],
      },

}

# OR NAME_ID or MAIN_ATTRIBUTE (not together!)
SAML_USE_NAME_ID_AS_USERNAME = True
# SAML_DJANGO_USER_MAIN_ATTRIBUTE = 'email'
SAML_DJANGO_USER_MAIN_ATTRIBUTE_LOOKUP = '__iexact'

SAML_CREATE_UNKNOWN_USER = True

# logout
SAML_LOGOUT_REQUEST_PREFERRED_BINDING = saml2.BINDING_HTTP_POST

SAML_ATTRIBUTE_MAPPING = {
    ## 'uid': ('username', ),
    'email': ('email', ),
    'name': ('first_name', ),
    'familyName': ('last_name', ),
    'fiscalNumber': ('codice_fiscale',),
    'placeOfBirth': ('place_of_birth',),
    'dateOfBirth': ('birth_date',),
}
