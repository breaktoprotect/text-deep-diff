import pytest
from app.services.model_loader import get_sbert_model
from app.models.model_support import SupportedSBERTModel
from sentence_transformers import SentenceTransformer


def test_load_supported_model():
    model = get_sbert_model(SupportedSBERTModel.ALL_MP_NET_BASE_V2.value)
    assert model is not None
    assert isinstance(model, SentenceTransformer)
    assert hasattr(model, "encode")


def test_model_is_cached():
    model1 = get_sbert_model(SupportedSBERTModel.ALL_MP_NET_BASE_V2.value)
    model2 = get_sbert_model(SupportedSBERTModel.ALL_MP_NET_BASE_V2.value)
    assert model1 is model2  # same object from cache


def test_invalid_model_raises():
    with pytest.raises(ValueError) as exc_info:
        get_sbert_model("not-a-real-model-name")
    assert "not supported" in str(exc_info.value)
