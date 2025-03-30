from enum import Enum


class SupportedSBERTModel(str, Enum):
    ALL_MP_NET_BASE_V2 = "all-mpnet-base-v2"
    ATTACK_BERT = "basel/ATTACK-BERT"
    ALL_DISTILROBERTA_V1 = "all-distilroberta-v1"


def list_supported_models() -> list[str]:
    """
    Returns all supported model identifiers as a list of strings.
    """
    supported_models = []
    for model in SupportedSBERTModel:
        supported_models.append(model.value)
    return supported_models
