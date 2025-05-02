.. somerandomapi.py documentation master file, created by
   sphinx-quickstart on Sat Feb 25 22:53:53 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to somerandomapi.py!
=============================
An actively maintained wrapper for the `somerandomapi API <https://somerandomapi.com>`_.

Installation
+++++++++++++
Install the stable version from `PyPI <https://pypi.org/project/somerandomapi.py/>`_ using pip:

.. code-block:: bash

    python -m pip install somerandomapi

Or the latest dev version from GitHub using pip and `git <https://git-scm.com/>`_:

.. code-block:: bash

   python -m pip install "somerandomapi.py @ git+https://github.com/Soheab/somerandomapi.py"

Basic Examples
+++++++++++++++

Get a random joke


.. code-block:: python3

   import asyncio

   import somerandomapi

   sra_api = somerandomapi.Client("<optional api token>")

   async def main():
      joke = await sra_api.joke()
      print(joke)
      await sra_api.close()

   asyncio.run(main())

Use the chatbot feature:

.. code-block:: python

   import asyncio

   import somerandomapi


   async def main():
      async with somerandomapi.Client("<optional api token>") as sra_api:
         stopped: bool = False
         while not stopped:
               # can also do await sra-api.chatbot("message") to get a response immediately
               # but this is more efficient for long conversations
               async with sra_api.chatbot() as chatbot:
                  user_input = input("You: ")
                  if user_input.lower() == "stop":
                     stopped = True
                     print("Stopping the chatbot.")
                     break

                  # can also do await chatbot.send("message") to get a response
                  async with chatbot.send(user_input) as response:
                     if response is None:
                           print("No response received.")
                           continue
                     print(f"Bot: {response.response}")


   asyncio.run(main())

See more examples in the `examples directory on GitHub <https://github.com/Soheab/somerandomapi.py/tree/main/examples>`_.

Documentation
++++++++++++++
Visit the full documentation at: https://somerandomapipy.readthedocs.io

Contact
++++++++
For any questions, suggestions, or issues, feel free to reach out to me on Discord (@Soheab_).

- `My Discord <https://discord.gg/yCzcfju>`_
- `Library Discord <https://discord.gg/tTUMWFd>`_

License
++++++++

This project is licensed under the MPL2-0 License. See the `LICENSE <https://github.com/Soheab/somerandomapi.py/blob/main/LICENSE>`_ file for details.


