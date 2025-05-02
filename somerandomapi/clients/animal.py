from __future__ import annotations

from typing import TYPE_CHECKING, Any, overload
from collections.abc import Coroutine
import logging

from .. import (
    enums,
    utils as _utils,
)
from ..internals.endpoints import (
    Animal as AnimalEndpoint,
    Facts as AnimalFactsEndpoint,
    Img as AnimalImgEndpoint,
)
from ..models.animal_fact import AnimalImageFact, AnimalImageOrFact
from .abc import BaseClient

if TYPE_CHECKING:
    from ..types.animal import (
        Animal as AnimalPayload,
        ValidAnimal as AnimalsLiterals,
    )
    from ..types.facts import (
        Fact as FactPayload,
        ValidFact as FactsAnimalsLiterals,
    )
    from ..types.img import (
        Img as ImgPayload,
        ValidImg as ImgAnimalsLiterals,
    )


__all__ = ("AnimalClient",)

_log = logging.getLogger(__name__)


class AnimalClient(BaseClient):
    """Represents the "Animal" endpoint.

    This class is not meant to be instantiated by you. Instead, access it through the
    :attr:`~somerandomapi.Client.animal` attribute of the :class:`~somerandomapi.Client` class.
    """

    @overload
    def __handle_animal(
        self,
        _enum: type[enums.Animal],
        _input: enums.Animal | AnimalsLiterals,
    ) -> Coroutine[Any, Any, AnimalPayload]: ...

    @overload
    def __handle_animal(
        self,
        _enum: type[enums.Img],
        _input: enums.Img | ImgAnimalsLiterals,
    ) -> Coroutine[Any, Any, ImgPayload]: ...

    @overload
    def __handle_animal(
        self,
        _enum: type[enums.Fact],
        _input: enums.Fact | FactsAnimalsLiterals,
    ) -> Coroutine[Any, Any, FactPayload]: ...

    def __handle_animal(
        self,
        _enum: type[enums.Animal | enums.Img | enums.Fact],
        _input: enums.Animal | AnimalsLiterals | enums.Img | ImgAnimalsLiterals | enums.Fact | FactsAnimalsLiterals,
    ) -> Coroutine[Any, Any, AnimalPayload | ImgPayload | FactPayload]:
        endpoint_from_enum = {
            enums.Animal: AnimalEndpoint,
            enums.Img: AnimalImgEndpoint,
            enums.Fact: AnimalFactsEndpoint,
        }
        return self._http.request(endpoint_from_enum[_enum].from_enum(_utils._str_or_enum(_input, _enum)))

    async def get_image_and_fact(self, animal: enums.Animal | AnimalsLiterals) -> AnimalImageFact:
        """Get a random image and fact about an animal.

        Parameters
        ----------
        animal: Union[:class:`.Animal`, :class:`str`]
            The animal to get an image and fact about.

        Returns
        -------
        :class:`.AnimalImageFact`
            Object representing the requested animal and its image and fact.
            Use :attr:`.fact` and :attr:`.image` to get the fact and image url respectively.

        """
        response = await self.__handle_animal(enums.Animal, animal)
        return AnimalImageFact(**response)

    # @BaseClient._contextmanager
    async def get_image(self, animal: enums.Img | ImgAnimalsLiterals) -> str:
        """Get a random image of an animal.


        Parameters
        ----------
        animal: Union[:class:`.Img`, :class:`str`]
            The animal to get an image of.

        Returns
        -------
        :class:`str`
            The image URL.
        """
        response = await self.__handle_animal(enums.Img, animal)
        return response["link"]

    async def get_fact(self, animal: enums.Fact | FactsAnimalsLiterals) -> str:
        """Get a random fact about an animal.

        Parameters
        ----------
        animal: Union[:class:`.Fact`, :class:`str`]
            The animal to get a fact about.

        Returns
        -------
        :class:`str`
            The fact about the animal.

        """
        response = await self.__handle_animal(enums.Fact, animal)
        return response["fact"]

    #    @BaseClient._contextmanager
    async def get_image_or_fact(
        self,
        animal: enums.Animal | AnimalsLiterals | enums.Img | ImgAnimalsLiterals | enums.Fact | FactsAnimalsLiterals,
    ) -> AnimalImageOrFact:
        """A helper method to get either an image or a fact or both about an animal since the API
        provides different endpoints for each.

        .. versionadded:: 0.1.0

        This uses the following methods in order to get the image or fact or both:

        1. :meth:`~somerandomapi.AnimalClient.get_image_and_fact`
        2. :meth:`~somerandomapi.AnimalClient.get_fact`
        3. :meth:`~somerandomapi.AnimalClient.get_image`

        And returns an :class:`~somerandomapi.models.animal_fact.AnimalImageOrFact` object with the results.

        Parameters
        ----------
        animal: Union[:class:`.Animal`, :class:`.Img`, :class:`.Fact`, :class:`str`]
            The animal to get an image or fact or both of.

        Returns
        -------
        :class:`.AnimalImageOrFact`
            Object representing the requested animal and its image or fact or both.

            Use :attr:`.fact` and :attr:`.image` to get the fact and image url respectively.
        """
        fact: str | None = None
        image: str | None = None

        animal_str: Any = str(animal.value) if not isinstance(animal, str) else animal.lower()

        # try getting both image and fact
        try:
            res = await self.get_image_and_fact(animal_str)
            fact = res.fact
            image = res.image
        except (ValueError, TypeError) as e:
            _log.debug("Failed to get image and fact for %r. Error: %s", animal_str, e)

        # get fact if not yet gotten
        if not fact:
            try:
                fact = await self.get_fact(animal_str)
            except (ValueError, TypeError) as e:
                _log.debug("Failed to get fact for %r. Error: %s", animal_str, e)

        # get image if not yet gotten
        if not image:
            try:
                image = await self.get_image(animal_str)
            except (ValueError, TypeError) as e:
                _log.debug("Failed to get image for %r. Error: %s", animal_str, e)

        return AnimalImageOrFact(fact=fact, image=image)
