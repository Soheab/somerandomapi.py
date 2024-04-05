"""
Clients
--------

This module contains all the clients for the library. Each client represents a different endpoint of the API.
"""

# fmt: off
# isort: off
from .animal import AnimalClient as AnimalClient
from .animu import AnimuClient as AnimuClient
from .canvas import CanvasClient as CanvasClient, CanvasMemes as CanvasMemes
from .chatbot import Chatbot as Chatbot
from .client import Client as Client
from .pokemon import PokemonClient as PokemonClient
from .premium import PremiumClient as PremiumClient
# isort: on
# fmt: on
