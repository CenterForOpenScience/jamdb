Installing JamDB
================

JamDB is written in [Python](http://python.org) using the [Tornado](http://www.tornadoweb.org/en/stable/) Web Framework.

It requires [MongoDB](http://mongodb.org) version >= 3.2 and [Elasticsearch](https://www.elastic.co/products/elasticsearch) version 1.7.

Steps
-----

1.  Clone the JamDB git repo
2.  Create a new [virtual environment](https://virtualenv.readthedocs.org/en/latest/) for JamDB called `jam`
3.  Setup your new virtual environment for JamDB
    - Once in your virtual env, change into the directory you cloned JamDB into and execute `python setup.py develop`
    - Then execute `pip install -r requirements.txt`
4. Install [MongoDB](https://docs.mongodb.org/manual/installation/) and [Elasticsearch](https://www.elastic.co/guide/en/elasticsearch/reference/current/_installation.html)
5. Confirm they're both running: ``ps aux | grep -i 'elasticsearch\|mongod'``
6. Run ``jam server``
7. In another terminal, run ``curl http://localhost:1212/v1/namespaces/`` to confirm you can connect to the server. The response should be: ``{"data": [], "links": {}, "meta": {"perPage": 50, "total": 0}}``

Next you should see the [Namespaces](namespaces.html) section for instructions on creating your first namespace.
