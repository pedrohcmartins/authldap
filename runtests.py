import sys

try:
    from django.conf import settings
    from django.test.utils import get_runner

    settings.configure(
        DEBUG=True,
        USE_TZ=True,
        DATABASES={
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
            }
        },
        ROOT_URLCONF="authldap.urls",
        INSTALLED_APPS=[
            "django.contrib.auth",
            "django.contrib.contenttypes",
            "django.contrib.sites",
            "authldap",
            'rest_framework',
            'rest_framework.authtoken',
            'corsheaders',
            'django_python3_ldap',
        ],
        SITE_ID=1,
        MIDDLEWARE_CLASSES=(
            'django.middleware.security.SecurityMiddleware',
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.middleware.common.CommonMiddleware',
            'django.middleware.csrf.CsrfViewMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
            'django.contrib.messages.middleware.MessageMiddleware',
            'django.middleware.clickjacking.XFrameOptionsMiddleware',
            'corsheaders.middleware.CorsMiddleware',    
        ),

        AUTHENTICATION_BACKENDS = (
            # 'django_python3_ldap.auth.LDAPBackend',
            'django.contrib.auth.backends.ModelBackend',
        ),

        ########## AUTH USER RESPONSE DATA ##########
        AUTH_USER_RESPONSE= {
            'is_superuser': 'is_superuser',
            'is_staff': 'is_staff',
        },
        ########## END AUTH USER RESPONSE DATA ##########

        # ########## LDAP CONFIG ##########
        # LDAP_AUTH_URL = 'ldap://0.0.0.0:389',
        # LDAP_AUTH_USE_TLS = False,
        # LDAP_AUTH_SEARCH_BASE = 'ou=Users,ou=users,o=rede,c=br',
        # LDAP_AUTH_USER_FIELDS = {
        #     "username": "uid",
        #     "name": "cn",
        #     "last_name": "sn",
        #     "email": "mail",
        # },
        # LDAP_AUTH_USER_LOOKUP_FIELDS = ("username",),
        # ########## END LDAP CONFIG ##########

        # # AUTH BACKEND CONFIG TEST USER VALIDATION
        # LDAP_USER = '',
        # LDAP_PASSWORD = '',
             
    )

    try:
        import django
        setup = django.setup
    except AttributeError:
        pass
    else:
        setup()

except ImportError:
    import traceback
    traceback.print_exc()
    raise ImportError("To fix this error, run: pip install -r requirements-test.txt")


def run_tests(*test_args):
    if not test_args:
        test_args = ['tests']

    # Run tests
    TestRunner = get_runner(settings)
    test_runner = TestRunner()

    failures = test_runner.run_tests(test_args)

    if failures:
        sys.exit(bool(failures))


if __name__ == '__main__':
    run_tests(*sys.argv[1:])
