from somerandomapi.models.animal_fact import AnimalImageFact, AnimalImageOrFact


def test_animal_image_fact_model() -> None:
    model = AnimalImageFact(fact="fox fact", image="https://example.com/fox.png")
    assert model.fact == "fox fact"
    assert model.image.startswith("https://")
    assert AnimalImageFact.from_dict(model.to_dict()).fact == "fox fact"


def test_animal_image_or_fact_model() -> None:
    model = AnimalImageOrFact(fact=None, image="https://example.com/fox.png")
    assert model.fact is None
    assert model.image is not None
    restored = AnimalImageOrFact.from_dict(model.to_dict())
    assert restored.image == model.image

