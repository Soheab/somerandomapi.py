from dataclasses import dataclass


__all__ = ("ChatbotResult",)


@dataclass(frozen=True)
class ChatbotResult:
    message: str
    """The input message"""
    response: str
    """The response message"""

    def __str__(self) -> str:
        return self.response

    def __len__(self) -> int:
        return len(self.response)
