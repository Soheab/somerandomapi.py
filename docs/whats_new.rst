.. currentmodule:: somerandomapi

.. _whats_new:

Changelog
============

This page keeps a detailed human friendly rendering of what's new and changed
in specific versions.

v0.0.5
------

- Fix exceptions not being accessed from main namespace (``somerandomapi...``).
- Fix link to API in README

**Full Changelog**: https://github.com/Soheab/somerandomapi.py/compare/0.0.4...0.0.5

v0.0.4
-------

- Urgent fix for the base URL for requests to the API. The base URL changed from ``https://some-random-api.ml/`` to ``https://some-random-api.com/``.

**Full Changelog**: https://github.com/Soheab/somerandomapi.py/compare/0.0.3...0.0.4

v0.0.3
-------

- Correct base API URL. URL changed from ``https://some-random-api.ml/`` to ``https://some-random-api.com/``.
- Fix mistake in :class:`.AnimalClient.get_image_and_fact`
- Fix enum conversion errors
- Fix link to API in documentation.

**Full Changelog**: https://github.com/Soheab/somerandomapi.py/compare/0.0.2...0.0.3

v0.0.2
-------

- Fixed a critical NameError in ``Client``.

v0.0.1
-------

- Initial release!
