from ..enums import TweetTheme
from ..internals.endpoints import CanvasMisc
from .abc import BaseImageModel, attribute

__all__ = ("Tweet",)


class Tweet(BaseImageModel):
    """Represents a tweet."""

    __endpoint__ = CanvasMisc.TWEET

    display_name: str = attribute(data_name="displayname", max_length=32)
    """:class:`str`: The display name of the user. Max 32 characters."""
    username: str = attribute(data_name="username", max_length=15)
    """:class:`str`: The username of the user. Max 15 characters."""
    avatar_url: str = attribute(data_name="avatar")
    """:class:`str`: The avatar URL of the user. Must be .png or .jpg."""
    text: str = attribute(data_name="comment", max_length=1000)
    """:class:`str`: The text of the tweet. Max 1000 characters."""
    replies: int | None = None
    """Optional[:class:`int`]: The amount of replies the tweet is supposed to have."""
    likes: int | None = None
    """Optional[:class:`int`]: The amount of likes the tweet is supposed to have."""
    retweets: int | None = None
    """Optional[:class:`int`]: The amount of retweets the tweet is supposed to have."""
    theme: TweetTheme | None = TweetTheme.LIGHT
    """:class:`~somerandomapi.enums.TweetTheme`: The theme of the tweet. 
    Defaults to :attr:`~somerandomapi.enums.TweetTheme.LIGHT`."""
