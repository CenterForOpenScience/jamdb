Installing JamDB
================
JamDB is written in `Python <http://python.org>`_ using the `Tornado <http://www.tornadoweb.org/en/stable/>`_ Web Framework.

It requires `MongoDB <http://mongodb.org>`_ version >= 3.2 and `Elasticsearch <https://www.elastic.co/products/elasticsearch>`_ version >= 1.8.

Steps
#####
#. Clone the JamDB git repo.
#. Create a new `virtual environment <https://virtualenv.readthedocs.org/en/latest/>`_ for JamDB called ``jam``
#. Once in your virtual env, change directory into the directory you cloned JamDB into and execute ``python setup.py develop``
