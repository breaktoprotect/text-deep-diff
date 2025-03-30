import pytest
from sentence_transformers import SentenceTransformer
from app.services.similarity_engine import compute_cosine_similarity


@pytest.fixture(scope="module")
def sbert_model() -> SentenceTransformer:
    """
    Loads a lightweight SBERT model once for all tests.
    """
    return SentenceTransformer("all-MiniLM-L6-v2")


def test_cosine_similarity_basic(sbert_model):
    sents1 = ["User access control", "Data encryption"]
    sents2 = ["Access management", "Encrypt data at rest"]

    results = compute_cosine_similarity(sbert_model, sents1, sents2)

    assert isinstance(results, list)
    assert len(results) == 2
    for score in results:
        assert 0.0 <= score <= 1.0


def test_cosine_similarity_identical_sentences(sbert_model):
    sents = ["This is the same", "Identical sentence"]
    results = compute_cosine_similarity(sbert_model, sents, sents)

    assert all(round(score, 4) == pytest.approx(1.0, rel=1e-2) for score in results)


def test_cosine_similarity_empty_input(sbert_model):
    with pytest.raises(ValueError):
        compute_cosine_similarity(sbert_model, [], [])
