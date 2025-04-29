from .abc import BaseModel

__all__ = ("ChatbotResult",)


class ChatbotResult(BaseModel, frozen=True, validate_types=False):
    message: str
    """The input message"""
    response: str
    """The response message"""

    def __str__(self) -> str:
        return self.response

    def __len__(self) -> int:
        return len(self.response)
