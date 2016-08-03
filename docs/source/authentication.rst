Authentication
==============

JamDB uses `Json Web Tokens`_ for authentication.

Authenticating
--------------

JamDB allows authentication through many providers. Currently ``osf`` and ``self`` are the only available providers.

A user may authenticate to JamDB by sending a properly formatted ``POST`` request to Jam’s auth endpoint, ``/v1/auth``

.. code:: http

    POST /v1/auth HTTP/1.1

    {
      "data": {
        "type": "users",
        "attributes": {
          "provider": ...
          ...
        }
      }
    }

.. note:: The elements of ``attributes`` have been left blank in this example as they vary per provider.
    The following sections will cover what each provider needs to properly authenticate

A successful authentication request will return the following data

.. code:: json

        {
            "data": {
                "id": "<type>-<provider>-<id>",
                "type": "users",
                "attributes": {
                    "id": "<id>",
                    "type": "<type>",
                    "provider": "<provider>",
                    "token": "<jwt>",
                }
            }
        }

``data.id`` is the `user id`_ it will be matched against `user selectors`_ to calculate it’s permissions.

``data.attributes.id`` is the provider specific id for this user.

``data.attributes.type`` is the `type of user`_ for this user.

``data.attributes.provider`` is the provider that was used to authenticate as this user.

``data.attributes.token`` is the jwt used to authorize requests to JamDB

OSF
~~~

You will need an OSF account and an `OAuth2`_ access token to authenticate via the OSF provider.

You may sign up for an account at `osf.io`_.

To acquire an access token you may either generate a personal access token in `user settings`_ or via an `OAuth2`_ authorization flow of an `OSF app`_.

.. code:: http

    GET /v1/auth HTTP/1.1

    {
      "data": {
        "type": "users",
        "attributes": {
          "provider": "osf",
          "access_token": "<token>",
        }
      }
    }

Authorizing
-----------

Authorization may be provided for an HTTP request in either the ``Authorization`` header or the ``token`` query parameter.

    Note: The ``Authorization`` header takes precedence over the
    ``token`` query parameter

.. code:: http

    GET /v1/namespaces/ProgrammingLanguages HTTP/1.1
    Authorization: mycooljwt

.. code:: http

    PUT /v1/namespaces/ProgrammingLanguages?token=mycooljwt HTTP/1.1

User Ids
--------

User Ids are made of three parts separated by ``-``\ s.

``<type>-<provider>-<id>``

    Note: ``*``, ``-`` and ``.`` are illegal characters in user ids

Type
~~~~

Currently there are 3 types, ``user``, ``anon``, and ``jam``.

``user`` indicates that the user was authenticated via a 3rd party service, such as the OSF, Google, or even Facebook.

``anon`` indicates that the user simply requested a token to access JamDB, **anyone may be a anon user**.

``jam`` indicates that the user was authenticated via a collection existing in jam.

Provider
~~~~~~~~

A provider is simply the service that was used to authenticate.

In the case of the ``user`` type this may be ``osf``, ``google``, ``facebook``, etc.

``anon`` users do not have a provider.

For the ``jam`` user type, provider is the namespace and collection that the user “logged into” separated by a ``:``. ie ``ProgrammingLanguages:Functional``

Id
~~

An id is any given string used by their provider to identify a user.

User Selectors
--------------

+-------------------+--------------------------------------------------------+
| Selector          | Meaning                                                |
+===================+========================================================+
| ``*``             | Matches **ALL** users, authenticated or not            |
+-------------------+--------------------------------------------------------+
| ``<type>-*``      | Matches all authenticated users with the type          |
|                   | ``<type>``                                             |
+-------------------+--------------------------------------------------------+
| ``<type>-<provide | Matches all users of the given type that have          |
| r>-*``            | authenticated via ``<provider>``                       |
+-------------------+--------------------------------------------------------+
| ``<type>-<provide | Matches an exact user                                  |
| r>-<id>``         |                                                        |
+-------------------+--------------------------------------------------------+

User Selectors
~~~~~~~~~~~~~~

+---------------------------------------------------------+----------------------+
| Objective                                               | Selector             |
+=========================================================+======================+
| Match everyone                                          | ``*``                |
+---------------------------------------------------------+----------------------+
| Match all users authenticated via OSF                   | ``user-osf-*``       |
+---------------------------------------------------------+----------------------+
| Match all users authenticated via a 3rd party service   | ``user-*``           |
+---------------------------------------------------------+----------------------+
| Match anonymous users                                   | ``anon-*``           |
+---------------------------------------------------------+----------------------+
| Match a specific user                                   | ``user-osf-juwia``   |
+---------------------------------------------------------+----------------------+

.. _Json Web Tokens: https://jwt.io
.. _user id: #user-selectors
.. _user selectors: #user-selectors
.. _type of user: #type
.. _osf.io: https://osf.io
.. _user settings: https://osf.io/settings/tokens/
.. _OSF app: https://osf.io/settings/applications/
.. _OAuth2: https://tools.ietf.org/html/rfc6749
