from typing import List
from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim


def compute_cosine_similarity(
    model: SentenceTransformer,
    sentences1: List[str],
    sentences2: List[str],
) -> List[float]:
    """
    Computes cosine similarity between each pair of sentences (zip-wise).
    Returns a list of similarity scores between 0 and 1.
    """
    if not sentences1 or not sentences2:
        raise ValueError("Input sentence lists must not be empty.")

    embeddings1 = model.encode(sentences1, convert_to_tensor=True)
    embeddings2 = model.encode(sentences2, convert_to_tensor=True)

    # Compute cosine similarity for aligned pairs (zip-wise)
    similarity_matrix = cos_sim(embeddings1, embeddings2)

    # Extract diagonal (assumes 1:1 comparison)
    return [float(score.item()) for score in similarity_matrix.diag()]
