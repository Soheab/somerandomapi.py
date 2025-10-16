.. currentmodule:: somerandomapi

.. _whats_new:

Changelog
==========

This page keeps a detailed, human-friendly rendering of what's new and changed
in specific versions.

v0.1.2
-------

- Hotfix for Python 3.14 compatibility. The wrapper now supports Python 3.11 to 3.14.
- Other Miscellaneous fixes and improvements internally. For example, the type 
  checking implementation was improved to handle more edge cases and be less error-prone.
- Improve error messages for some exceptions, like missing keyword arguments or passing
  positional arguments when only keyword arguments are accepted.

**Full Changelog**: `GitHub Diff <https://github.com/Soheab/somerandomapi.py/compare/0.1.1...0.1.2>`_

v0.1.1
-------

Just for PyPi because v0.1.0 already uploaded to PyPi but something went wrong with it.

**Full Changelog**: `GitHub Diff <https://github.com/Soheab/somerandomapi.py/compare/0.1.0...0.1.1>`_

v0.1.0
-------

Big update! Lots of QoL changes.

New Features
~~~~~~~~~~~~~

- Added support for Authorization token; pass your token to the 
  ``token=`` parameter in the constructor of the :class:`Client`. 
  
  This may be required for some endpoints, in the future.

  This replaces the ``key=`` parameter. This parameter is removed from
  all relevent classes and methods.
- Added support for the ``username_color`` field for the rankcard endpoint 
  (:meth:`PremiumClient.rankcard`, :class:`Rankcard`).
- Added :meth:`AnimuClient.get` method.
- Added :class:`.Animu` enum for the :meth:`AnimuClient.get` method.
- Added :meth:`AnimalClient.get_image_or_fact` method.
- Added shortcuts to using :meth:`AnimuClient.get`:

  - :meth:`AnimuClient.pat`
  - :meth:`AnimuClient.kiss`
  - :meth:`AnimuClient.poke`
  - :meth:`AnimuClient.nom`
  - :meth:`AnimuClient.cry`

- Added shortcuts to using :meth:`CanvasClient.filter`:

  - :meth:`CanvasClient.blue_filter`
  - :meth:`CanvasClient.blurple_filter`
  - :meth:`CanvasClient.blurple2_filter`
  - :meth:`CanvasClient.green_filter`
  - :meth:`CanvasClient.greyscale_filter`
  - :meth:`CanvasClient.invert_filter`
  - :meth:`CanvasClient.invertgreyscale_filter`
  - :meth:`CanvasClient.red_filter`
  - :meth:`CanvasClient.sepia_filter`
  - :meth:`CanvasClient.blur_filter`
  - :meth:`CanvasClient.pixelate_filter`

- Added :class:`.TweetTheme` enum for the 
  :meth:`CanvasClient.generate_tweet` method and :class:`somerandomapi.Tweet` class.
- All color methods can now take an integer as a value for the color 
  parameter. This is a hex value, e.g. 0xFF0000 for red.
- :class:`somerandomapi.Rankcard` and :meth:`PremiumClient.rankcard` now take a 
  ``template`` parameter. This takes an integer from 1 to 9.

Removals
~~~~~~~~~

- Support for Python 3.9 and 3.10 was removed. The library now requires Python 3.11 or higher.

- :meth:`Client.generate_bot_token` no longer takes a ``bot_id`` parameter. 
  This is because the API no longer supports this feature.
- ``Client.dictionary`` was removed. The API no longer has this feature.
- The class ``LyricsLinks`` was removed. The API no longer has this feature.
- ``AnimuClient.face_palm`` was removed. The API no longer has this feature.

Bug Fixes
~~~~~~~~~~

- Fixed a bug where :meth:`PremiumClient.rankcard` did not use the correct endpoint.
- Fixed a bug where the random color from the library would be less than 6 characters long.

Miscellaneous
~~~~~~~~~~~~~~

- The ``session=`` parameter in the constructor of the :class:`Client` 
  can no longer take ``None`` as a value and the passed session will **not**
  be closed by the library, you are responsible for that.
- Most parameters for the following methods can no longer take ``None`` as a value:

  - :meth:`Client.welcome_image`
  - :meth:`CanvasClient.generate_tweet`
  - :meth:`CanvasClient.generate_youtube_comment`
  - :meth:`CanvasClient.generate_tweet`
  - :meth:`CanvasClient.generate_genshin_namecard`

  Either pass a value or don't pass the parameter at all.
- The ``font`` parameter in :meth:`Client.welcome_image`, :class:`PremiumClient.welcome_image`, 
  :class:`WelcomeFree`, and :class:`WelcomePremium` now takes a range of 1 to 7 instead of 0 to 8.
- Renamed ``FactAnimal`` enum to :class:`.Animal`.
- Renamed ``ImgAnimal`` enum to :class:`.Img`.
- Renamed ``AnimuClient.quote`` to :meth:`.AnimuClient.random_quote`.
- Renamed ``Canvad.filter_colo[u]r`` to :meth:`CanvasClient.color_filter` and 
  :meth:`CanvasClient.colour_filter`.
- Renamed ``CanvasClient.filter_threshold`` to :meth:`CanvasClient.threshold_filter`.
- The ``theme`` parameter in :meth:`CanvasClient.generate_tweet` now takes an enum of type
  :class:`.TweetTheme` instead of a string. Still defaults to
  dark (:attr:`.TweetTheme.DARK`).
- The ``lyrics`` endpoint has changed. The following changes were made in this library:

  - ``.author`` was changed to :attr:`.Lyrics.artist`.
  - ``.thumbnail`` and ``.links`` are simply strings now, :attr:`.Lyrics.thumbnail` and 
    :attr:`.Lyrics.url`, respectively.

- Overall the backend of the library was partially rewritten to make it faster and more efficient.
- The readthedocs theme changed from ``sphinx_rtd_theme`` to ``furo``.
- All docstrings were revisited to be constsistent and follow the same format.
- Brand new README.

**Full Changelog**: `GitHub Diff <https://github.com/Soheab/somerandomapi.py/compare/0.0.8...0.1.0>`_

v0.0.8
------

- Add debug logging to the http client and endpoints validation. This will log the request and response data if the logger is set to debug. Here is how to enable it:

  .. code-block:: python

    import logging

    # http
    sra_http_logger = logging.getLogger("somerandomapi.http")
    sra_http_logger.setLevel(logging.DEBUG)
    # endpoints validation
    sra_endpoints_logger = logging.getLogger("somerandomapi.endpoints")
    sra_endpoints_logger.setLevel(logging.DEBUG)

- Corrected the font range for the welcome cards to be between 0 and 7. It was previously between 0 and 10.
  To prevent a breaking change, the library sets the font to 7 if the provided font is greater than 7.

  Affected classes and methods:
    - :meth:`.Client.welcome_image`
    - :class:`PremiumClient.welcome_image`
    - :class:`.WelcomeFree`
    - :class:`.WelcomePremium`
- Added a new method to the :class:`.AnimalClient` class to help with trying all available animal endpoints in order to get an image and a fact or just one of them.
  The method is called :meth:`.AnimalClient.get_image_or_fact` and takes all the available animal names and endpoints and tries to get an image and 
  a fact from each one until it succeeds. It returns an instance of :class:`.AnimalImageOrFact` with two optional attributes: `image` and `fact`. 
  If the method fails to get an image and a fact, it will return `None` for both attributes.

  .. code-block:: python

    import somerandomapi

    client = somerandomapi.Client(...)
    image_fact = await client.animal.get_image_or_fact(<enum or str>) # Example: "cat" or somerandomapi.Animal.PIKACHU
    print(image_fact.image, image_fact.fact) # <image url or None> <fact or None>

**Full Changelog**: `GitHub Diff <https://github.com/Soheab/somerandomapi.py/compare/0.0.7...0.0.8>`_

v0.0.7
-------
- **Fix**: ``discriminator`` field in relevant classes and methods:

  - :meth:`.Client.welcome_image`
  - :class:`.PremiumClient`
  - :class:`.Rankcard`
  - :class:`.WelcomeFree`
  - :class:`WelcomePremium`
It would previously raise an error if the discriminator was provided.

- Fix an internal error when the API returns an unexpected status code.
- Fix unparsed TypingError.
Sometimes it would send "_UnionGenericAlias" in the error message instead of the actual field type. This was fixed by always parsing the field's type.

**Full Changelog**: `GitHub Diff <https://github.com/Soheab/somerandomapi.py/compare/0.0.6...0.0.7>`_

v0.0.6
-------

- **Make**: `discriminator` optional in relevant classes and methods:
  - :meth:`.Client.welcome_image`
  - :class:`.PremiumClient`
  - :class:`.Rankcard`
  - :class:`.WelcomeFree`
  - :class:`WelcomePremium`

**Full Changelog**: `GitHub Diff <https://github.com/Soheab/somerandomapi.py/compare/0.0.5...0.0.6>`_

v0.0.5
-------

- **Fix**: Exceptions not being accessed from the main namespace (``somerandomapi...``).
- **Fix**: Link to API in README.

**Full Changelog**: `GitHub Diff <https://github.com/Soheab/somerandomapi.py/compare/0.0.4...0.0.5>`_

v0.0.4
-------

- **Urgent Fix**: Base URL for requests to the API changed from 
  ``https://some-random-api.ml/`` to ``https://some-random-api.com/``.

**Full Changelog**: `GitHub Diff <https://github.com/Soheab/somerandomapi.py/compare/0.0.3...0.0.4>`_

v0.0.3
-------

- Correct base API URL. URL changed from ``https://some-random-api.ml/`` to ``https://some-random-api.com/``.
- Fix mistake in :class:`.AnimalClient.get_image_and_fact`
- Fix enum conversion errors
- Fix link to API in documentation.

**Full Changelog**: `GitHub Diff <https://github.com/Soheab/somerandomapi.py/compare/0.0.2...0.0.3>`_

v0.0.2
-------

- **Fix**: Critical NameError in ``Client``.

v0.0.1
-------

- Initial Release!
