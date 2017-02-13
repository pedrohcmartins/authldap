=============================
authldap
=============================

.. image:: https://badge.fury.io/py/authldap.png
    :target: https://badge.fury.io/py/authldap

.. image:: https://travis-ci.org/dagnaldo/authldap.png?branch=master
    :target: https://travis-ci.org/dagnaldo/authldap

A simple project that implements authentication via ldap with user custom models:

Quickstart
----------

Install authldap::

    pip install authldap

Then use it in a project::

    import authldap

To add custom user attributes to your response, you must add it into your settings file::
    AUTH_USER_RESPONSE = {
        'is_superuser': 'is_superuser',
        'is_staff': 'is_staff',
        'management': 'coord...', 
    }

Features
--------

* TODO:
	- Add user session validation;


Running Tests
--------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install -r requirements-test.txt
    (myenv) $ python runtests.py

Credits
---------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-pypackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
