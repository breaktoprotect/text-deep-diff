from app.models.model_support import SupportedSBERTModel
from sentence_transformers import SentenceTransformer

_model_cache = {}


def get_sbert_model(model_name: str) -> SentenceTransformer:
    """
    Load or get cached SBERT model by name, if supported.
    """
    if model_name not in SupportedSBERTModel._value2member_map_:
        raise ValueError(f"Model '{model_name}' is not supported.")

    if model_name not in _model_cache:
        _model_cache[model_name] = SentenceTransformer(model_name)

    return _model_cache[model_name]
