=============================
authldap
=============================

.. image:: https://badge.fury.io/py/authldap.png
    :target: https://badge.fury.io/py/authldap

.. image:: https://travis-ci.org/dagnaldo/authldap.png?branch=master
    :target: https://travis-ci.org/dagnaldo/authldap

A simple project to auth with ldap

Documentation
-------------

The full documentation is at https://authldap.readthedocs.org.

Quickstart
----------

Install authldap::

    pip install authldap

Then use it in a project::

    import authldap

To add user attrs with your response, you need to add it in your settings, 
(Where the object key is the value in your response, and the object value is the data from your model), as::
    AUTH_USER_RESPONSE = {
        'is_superuser': 'is_superuser',
        'is_staff': 'is_staff',
    }

Features
--------

* TODO::
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
