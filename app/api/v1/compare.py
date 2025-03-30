from fastapi import APIRouter, HTTPException

from app.models.model_support import SupportedSBERTModel
from app.models.compare_models import CompareRequest
from app.services.model_loader import get_sbert_model
from app.services.similarity_engine import compute_cosine_similarity

router = APIRouter()


@router.get("/models", tags=["Models"])
def list_models() -> list[str]:
    return [m.value for m in SupportedSBERTModel]


@router.post("/compare", tags=["Compare"])
def compare_sentences(request: CompareRequest):
    if len(request.sentences1) != len(request.sentences2):
        raise HTTPException(
            status_code=400, detail="Sentence lists must be the same length."
        )

    model = get_sbert_model(request.model_name.value)
    scores = compute_cosine_similarity(model, request.sentences1, request.sentences2)

    return {"similarity_scores": scores}
