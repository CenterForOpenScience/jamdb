.. JamDB documentation master file, created by
   sphinx-quickstart on Fri Feb 19 09:36:34 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to JamDB's documentation!
=================================

JamDB is a schema-less, immutable database that can optionally enforce a schema and stores provenance. It supports efficient full-text search, filtering by nested keys, and is accessible a REST API.

It has pluggable storage backends. It defaults to using both `MongoDB <http://mongodb.org>`_ and `Elasticsearch <https://www.elastic.co/products/elasticsearch>`_.

The full BDD test suite lives in the `features directory <https://github.com/CenterForOpenScience/jamdb/tree/master/features>`_ and describes in human-readable prose how each endpoint works. What it's expecting for input and what it expects for output.

*Please note: This documentation is a work in progress.*

Contents:

.. toctree::
   :maxdepth: 15

   prerequisites
   install
   namespaces
   collections
   documents
   authentication
   data-modeling
   permissions
   contributing
   limitations
   api

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
