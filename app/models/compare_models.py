from pydantic import BaseModel
from typing import List
from app.models.model_support import SupportedSBERTModel


class CompareRequest(BaseModel):
    model_name: SupportedSBERTModel
    sentences1: List[str]
    sentences2: List[str]
