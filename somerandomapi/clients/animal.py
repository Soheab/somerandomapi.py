from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any, Coroutine, Optional, Union, overload

from .. import enums
from ..internals.endpoints import Animal as AnimalEndpoint, Facts as AnimalFactsEndpoint, Img as AnimalImgEndpoint
from ..models.animal_fact import AnimalImageFact, AnimalImageOrFact
from .abc import BaseClient


if TYPE_CHECKING:
    from ..types.animal import ValidAnimal as AnimalsLiterals, Animal as AnimalPayload
    from ..types.facts import ValidFact as FactsAnimalsLiterals, Fact as FactPayload
    from ..types.img import ValidImg as ImgAnimalsLiterals, Img as ImgPayload


__all__ = ("AnimalClient",)

_log = logging.getLogger(__name__)


class AnimalClient(BaseClient):
    """Represents the "Animal" endpoint.

    This class is not meant to be instantiated by the user. Instead, access it through the :attr:`~somerandomapi.Client.animal` attribute of the :class:`~somerandomapi.Client` class.
    """

    @overload
    def __handle_animal(
        self,
        _enum: type[enums.Animal],
        _input: Union[enums.Animal, AnimalsLiterals],
    ) -> Coroutine[Any, Any, AnimalPayload]: ...

    @overload
    def __handle_animal(
        self,
        _enum: type[enums.Img],
        _input: Union[enums.Img, ImgAnimalsLiterals],
    ) -> Coroutine[Any, Any, ImgPayload]: ...

    @overload
    def __handle_animal(
        self,
        _enum: type[enums.Fact],
        _input: Union[enums.Fact, FactsAnimalsLiterals],
    ) -> Coroutine[Any, Any, FactPayload]: ...

    def __handle_animal(
        self,
        _enum: Union[type[enums.Animal], type[enums.Img], type[enums.Fact]],
        _input: Union[enums.Animal, AnimalsLiterals, enums.Img, ImgAnimalsLiterals, enums.Fact, FactsAnimalsLiterals],
    ) -> Coroutine[Any, Any, Union[AnimalPayload, ImgPayload, FactPayload]]:
        endpoint_from_enum = {
            enums.Animal: AnimalEndpoint,
            enums.Img: AnimalImgEndpoint,
            enums.Fact: AnimalFactsEndpoint,
        }

        valid_animals = list(map(str, list(_enum)))
        not_valid_error: str = f"'animal' must be an instance of 'somerandomapi.{_enum.__name__}' or one of {', '.join(valid_animals)}, not {_input!r}."

        if str(_input) not in valid_animals:
            raise ValueError(not_valid_error)

        try:
            _endpoint = endpoint_from_enum[_enum].from_enum(_enum(_input))
        except ValueError:
            raise ValueError(not_valid_error) from None

        return self._http.request(_endpoint)

    # @BaseClient._contextmanager
    async def get_image_and_fact(self, animal: Union[enums.Animal, AnimalsLiterals]) -> AnimalImageFact:
        """Get a random animal.

        Parameters
        ----------
        animal: Union[:class:`.Animal`, :class:`str`]
            The animal to get.

        Returns
        -------
        :class:`.AnimalImageFact`
            Object representing the requested animal and its fact.
        """
        response = await self.__handle_animal(enums.Animal, animal)
        return AnimalImageFact(**response)

    # @BaseClient._contextmanager
    async def get_image(self, animal: Union[enums.Img, ImgAnimalsLiterals]) -> str:
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

    #  @BaseClient._contextmanager
    async def get_fact(self, animal: Union[enums.Fact, FactsAnimalsLiterals]) -> str:
        """Get a random fact about something (mostly animals).

        Parameters
        ----------
        animal: Union[:class:`.Fact`, :class:`str`]
            The animal to get a fact about.

        Returns
        -------
        :class:`str`
            The fact.
        """
        response = await self.__handle_animal(enums.Fact, animal)
        return response["fact"]

    #    @BaseClient._contextmanager
    async def get_image_or_fact(
        self,
        animal: Union[enums.Animal, AnimalsLiterals, enums.Img, ImgAnimalsLiterals, enums.Fact, FactsAnimalsLiterals],
    ) -> AnimalImageOrFact:
        """A helper method to get either an image or a fact or both about an animal since the API provides different endpoints for each.

        .. versionadded:: 0.1.0

        This uses the following methods in order to get the image or fact or both:

        1. :meth:`~somerandomapi.AnimalClient.get_image_and_fact`
        2. :meth:`~somerandomapi.AnimalClient.get_fact`
        3. :meth:`~somerandomapi.AnimalClient.get_image`

        And returns an :class:`~somerandomapi.models.animal_fact.AnimalImageOrFact` object with the results.

        Parameters
        ----------
        animal: Union[:class:`.Animal`, :class:`.ImgAnimal`, :class:`.FactAnimal`, :class:`str`]
            The animal to get an image or fact or both of.

        Returns
        -------
        :class:`.AnimalImageOrFact`
            Object representing the requested animal and its image or fact or both.
        """
        fact: Optional[str] = None
        image: Optional[str] = None

        animal_str = str(animal.value) if not isinstance(animal, str) else animal.lower()

        # try getting both image and fact
        try:
            res = await self.get_image_and_fact(animal_str)  # type: ignore
            fact = res.fact
            image = res.image
        except Exception as e:
            _log.debug("Failed to get image and fact for %r. Error: %s", animal_str, e)
            pass

        # get fact if not yet gotten
        if not fact:
            try:
                fact = await self.get_fact(animal_str)  # type: ignore
            except Exception as e:
                _log.debug("Failed to get fact for %r. Error: %s", animal_str, e)
                pass

        # get image if not yet gotten
        if not image:
            try:
                image = await self.get_image(animal_str)  # type: ignore
            except Exception as e:
                _log.debug("Failed to get image for %r. Error: %s", animal_str, e)
                pass

        return AnimalImageOrFact(fact=fact, image=image)
