from app.models.model_support import SupportedSBERTModel, list_supported_models


def test_enum_is_iterable_and_nonempty():
    values = list(SupportedSBERTModel)
    assert len(values) >= 1
    assert all(isinstance(m.value, str) for m in values)


def test_list_supported_models_matches_enum():
    expected = ["all-mpnet-base-v2", "basel/ATTACK-BERT", "all-distilroberta-v1"]
    actual = list_supported_models()
    assert sorted(actual) == sorted(expected)
