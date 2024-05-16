from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any, Coroutine, Optional, Union, overload

from ..enums import Animal as AnimalEnum, FactAnimal as AnimalFactsEnum, ImgAnimal as AnimalImgEnum
from ..internals.endpoints import Animal as AnimalEndpoint, Facts as AnimalFactsEndpoint, Img as AnimalImgEndpoint
from ..models.animal_fact import AnimalImageFact, AnimalImageOrFact


if TYPE_CHECKING:
    from ..internals.http import HTTPClient
    from ..types.animal import Animals as AnimalsLiterals, Animal as AnimalPayload
    from ..types.facts import Animals as FactsAnimalsLiterals, Fact as FactPayload
    from ..types.img import Images as ImgAnimalsLiterals, Img as ImgPayload


__all__ = ("AnimalClient",)

_log = logging.getLogger(__name__)


class AnimalClient:
    """Represents the "Animal" endpoint.

    This class is not meant to be instantiated by the user. Instead, access it through the :attr:`~somerandomapi.Client.animal` attribute of the :class:`~somerandomapi.Client` class.
    """

    __slots__ = ("__http",)

    def __init__(self, http) -> None:
        self.__http: HTTPClient = http

    @overload
    def __handle_animal(
        self,
        _enum: type[AnimalEnum],
        _input: Union[AnimalEnum, AnimalsLiterals],
    ) -> Coroutine[Any, Any, AnimalPayload]: ...

    @overload
    def __handle_animal(
        self,
        _enum: type[AnimalImgEnum],
        _input: Union[AnimalImgEnum, ImgAnimalsLiterals],
    ) -> Coroutine[Any, Any, ImgPayload]: ...

    @overload
    def __handle_animal(
        self,
        _enum: type[AnimalFactsEnum],
        _input: Union[AnimalFactsEnum, FactsAnimalsLiterals],
    ) -> Coroutine[Any, Any, FactPayload]: ...

    def __handle_animal(
        self,
        _enum: Union[type[AnimalEnum], type[AnimalImgEnum], type[AnimalFactsEnum]],
        _input: Union[AnimalEnum, AnimalsLiterals, AnimalImgEnum, ImgAnimalsLiterals, AnimalFactsEnum, FactsAnimalsLiterals],
    ) -> Coroutine[Any, Any, Union[AnimalPayload, ImgPayload, FactPayload]]:
        endpoint_from_enum = {
            AnimalEnum: AnimalEndpoint,
            AnimalImgEnum: AnimalImgEndpoint,
            AnimalFactsEnum: AnimalFactsEndpoint,
        }

        valid_animals = list(map(str, list(_enum)))
        not_valid_error = f"'animal' must be an instance of 'somerandomapi.{_enum.__name__}' or one of {', '.join(valid_animals)}, not {_input!r}."

        if str(_input) not in valid_animals:
            raise ValueError(not_valid_error)

        try:
            _endpoint = endpoint_from_enum[_enum].from_enum(_enum(_input))
        except ValueError:
            raise ValueError(not_valid_error) from None

        return self.__http.request(_endpoint)

    async def get_image_and_fact(self, animal: Union[AnimalEnum, AnimalsLiterals]) -> AnimalImageFact:
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
        response = await self.__handle_animal(AnimalEnum, animal)
        return AnimalImageFact(**response)

    async def get_image(self, animal: Union[AnimalImgEnum, ImgAnimalsLiterals]) -> str:
        """Get a random image of an animal.

        Parameters
        ----------
        animal: Union[:class:`.ImgAnimal`, :class:`str`]
            The animal to get an image of.

        Returns
        -------
        :class:`str`
            The image URL.
        """
        response = await self.__handle_animal(AnimalImgEnum, animal)
        return response["link"]

    async def get_fact(self, animal: Union[AnimalFactsEnum, FactsAnimalsLiterals]) -> str:
        """Get a random fact about an animal.

        Parameters
        ----------
        animal: Union[:class:`.FactAnimal`, :class:`str`]
            The animal to get a fact about.

        Returns
        -------
        :class:`str`
            The fact.
        """
        response = await self.__handle_animal(AnimalFactsEnum, animal)
        return response["fact"]

    async def get_image_or_fact(
        self,
        animal: Union[AnimalEnum, AnimalsLiterals, AnimalImgEnum, ImgAnimalsLiterals, AnimalFactsEnum, FactsAnimalsLiterals],
    ) -> AnimalImageOrFact:
        """A helper method to get either an image or a fact or both about an animal since the API provides different endpoints for each.

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

        animal = str(animal.value) if not isinstance(animal, str) else animal.lower()  # type: ignore

        # try getting both image and fact
        try:
            res = await self.get_image_and_fact(animal)  # type: ignore
            fact = res.fact
            image = res.image
        except Exception as e:
            _log.debug("Failed to get image and fact for %r. Error: %s", animal, e)
            pass

        # get fact if not yet gotten
        if not fact:
            try:
                fact = await self.get_fact(animal)  # type: ignore
            except Exception as e:
                _log.debug("Failed to get fact for %r. Error: %s", animal, e)
                pass

        # get image if not yet gotten
        if not image:
            try:
                image = await self.get_image(animal)  # type: ignore
            except Exception as e:
                _log.debug("Failed to get image for %r. Error: %s", animal, e)
                pass

        return AnimalImageOrFact(fact=fact, image=image)
