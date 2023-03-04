.. somerandomapi.py documentation master file, created by
   sphinx-quickstart on Sat Feb 25 22:53:53 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to somerandomapi.py's documentation!
============================================

Installation
-------------

You can get the library directly from PyPI:

.. code-block:: bash

   $ python -m pip install somerandomapi.py
   
Simple Examples
----------------

.. code-block:: python3

   import asyncio
   # import the library
   import somerandomapi

   # create a client
   sr_api = somerandomapi.Client()

   # define a function to get a random joke
   async def get_random_joke():
       joke = await sr_api.get_joke()
       # print the joke
       print(joke)

   # run the function
   asyncio.run(get_random_joke())

More Examples in the `Examples <https://github.com/Soheab/somerandomapi.py/blob/main/examples>`_ folder on the respository.

Links
------

**API**: https://somerandomapi.com/
**API Discord**: https://discord.gg/tTUMWFd

**Library Discord**: https://discord.gg/yCzcfju

.. toctree::
   :caption: API Reference
   :maxdepth: 2

   clients
   enums
   models
   errors
   whats_new
   
