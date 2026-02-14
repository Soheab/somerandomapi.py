import asyncio
import io

from somerandomapi.models.image import Image


class DummyHTTP:
    async def _get_image_url(self, url: str) -> bytes:
        assert url == "https://img"
        return b"data"


def _run(coro):
    return asyncio.run(coro)


def test_image_construct_read_and_file() -> None:
    img = Image.construct("https://img", DummyHTTP())
    assert str(img) == "https://img"

    raw = _run(img.read(bytesio=False))
    assert raw == b"data"

    buf = _run(img.read(bytesio=True))
    assert isinstance(buf, io.BytesIO)
    assert buf.getvalue() == b"data"

    class FakeFile:
        def __init__(self, fp, filename=None, **kwargs):
            self.fp = fp
            self.filename = filename
            self.kwargs = kwargs

    file_obj = _run(img.file(FakeFile, filename="x.png", spoiler=True))
    assert file_obj.filename == "x.png"
    assert file_obj.kwargs["spoiler"] is True
