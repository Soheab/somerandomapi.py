from somerandomapi.models.animu import AnimuQuote


def test_animu_quote_model() -> None:
    model = AnimuQuote(quote="Believe it!", anime="Naruto", id=1, name="Naruto")
    assert model.quote == "Believe it!"
    assert model.anime == "Naruto"


def test_animu_quote_from_dict() -> None:
    model = AnimuQuote.from_dict(quote="q", anime="a", id=1, name="n")
    assert model.name == "n"
    assert model.to_dict()["quote"] == "q"

