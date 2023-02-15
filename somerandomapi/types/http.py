from typing import Optional, TypedDict


class WithLink(TypedDict):
    link: str


class APIKeys(TypedDict):
    tier_1: Optional[str]
    tier_2: Optional[str]
    tier_3: Optional[str]
