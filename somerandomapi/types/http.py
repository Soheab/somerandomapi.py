from typing import Literal, TypedDict


class WithLink(TypedDict):
    link: str


ValidPaths = Literal[
    "animal/",
    "animu/",
    "canvas/",
    "canvas/filter/",
    "canvas/misc/",
    "canvas/overlay/",
    "facts/",
    "img/",
    "others/",
    "pokemon",
    "premium/",
    "chatbot",
    "welcome/img/",
]
