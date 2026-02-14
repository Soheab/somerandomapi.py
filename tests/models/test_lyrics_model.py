from somerandomapi.models.lyrics import Lyrics


def test_lyrics_model() -> None:
    model = Lyrics(
        title="Imagine",
        artist="John Lennon",
        lyrics="Imagine all the people",
        url="https://example.com",
        thumbnail="https://example.com/thumb.png",
    )
    assert model.title == "Imagine"
    assert str(model) == "Imagine all the people"
    assert Lyrics.from_dict(model.to_dict()).artist == "John Lennon"

