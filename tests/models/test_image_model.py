import asyncio
import io

from somerandomapi.models.image import Image


def _run(coro):
    return asyncio.run(coro)


class DummyHTTP:
    async def _get_image_url(self, _url: str) -> bytes:
        return b"image-bytes"


def test_image_model_construct_and_read() -> None:
    image = Image.construct("https://example.com/image.png", DummyHTTP())
    assert image.url.endswith(".png")
    assert str(image) == image.url
    assert _run(image.read(bytesio=False)) == b"image-bytes"
    assert isinstance(_run(image.read(bytesio=True)), io.BytesIO)


def test_image_model_file() -> None:
    image = Image.construct("https://example.com/image.png", DummyHTTP())

    class DummyFile:
        def __init__(self, fp, filename=None, **kwargs):
            self.fp = fp
            self.filename = filename
            self.kwargs = kwargs

    file_obj = _run(image.file(DummyFile, filename="x.png", spoiler=True))
    assert file_obj.filename == "x.png"
    assert file_obj.kwargs["spoiler"] is True

