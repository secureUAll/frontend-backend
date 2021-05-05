import os
import saml2
from saml2.saml import (NAMEID_FORMAT_PERSISTENT,
                        NAMEID_FORMAT_TRANSIENT,
                        NAMEID_FORMAT_UNSPECIFIED)
from saml2.sigver import get_xmlsec_binary


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

LOGIN_URL = '/saml2/login/'
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

BASE = 'https://deti-vuln-mon.ua.pt'

BASE_URL = '{}/saml2'.format(BASE)

LOGIN_URL = '/saml2/login/'
LOGOUT_URL = '/saml2/logout/'

IDP_URL = 'https://idp.ua.pt'

SAML_CONFIG = {
  'debug': True,
  # full path to the xmlsec1 binary programm
  'xmlsec_binary': '/usr/bin/xmlsec1',
  'entityid': "https://deti-vuln-mon.ua.pt/saml2/metadata/",
  'attribute_map_dir': os.path.join(os.path.join(BASE_DIR,
                                      'login'),
                                      'attribute_maps'),

  'service': {
      'sp' : {
          'name': "Vuln Mon",
          #'name_id_format': saml2.saml.NAMEID_FORMAT_EMAILADDRESS,
          #'authn_requests_signed': True,
          #'want_assertions_signed': True,
          #'allow_unsolicited': True,
          "name_id_format_allow_create": True,

          'endpoints': {
                'assertion_consumer_service': [
                    ('%s/acs' % BASE_URL, saml2.BINDING_HTTP_POST),
                    ],
                "single_logout_service": [
                    ("%s/ls/post/" % BASE_URL, saml2.BINDING_HTTP_POST),
                    ("%s/ls/" % BASE_URL, saml2.BINDING_HTTP_REDIRECT),
                ],
          }, # end endpoints
    },
  },
  'metadata': {
      'local':[os.path.join(BASE_DIR, 'login/idp/metadata.xml')],
      'remote': [{
            "url":"{}/idp/shibboleth".format(IDP_URL),
            "cert":"idp_cert.pem"
        }],

  },
  # Signing
  'key_file': os.path.join(BASE_DIR, 'login/idp/key.pem'),  # private part
  'cert_file': os.path.join(BASE_DIR, 'login/idp/cert.pem'),  # public part

  # Encryption
  'encryption_keypairs': [{
      'key_file': os.path.join(BASE_DIR, 'login/idp/key.pem'),  # private part
      'cert_file': os.path.join(BASE_DIR, 'login/idp/cert.pem'),  # public part
  }],

  'valid_for': 3650,  # how long is our metadata valid
  'contact_person': [ {'given_name': 'Vuln', 'sur_name': 'Mon', 'email_address': 'jpbarraca@ua.pt'},],
}


SAML_USE_NAME_ID_AS_USERNAME = False
SAML_DJANGO_USER_MAIN_ATTRIBUTE = 'email'
SAML_LOGOUT_REQUEST_PREFERRED_BINDING = saml2.BINDING_HTTP_POST

SAML_ATTRIBUTE_MAPPING = {
    'givenName' : ('first_name',),
    'sn': ('last_name',),
    'mail': ('email',),
}
