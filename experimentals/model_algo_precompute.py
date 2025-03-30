import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import (
    cosine_similarity,
    euclidean_distances,
    manhattan_distances,
)
from scipy.spatial import distance
import Levenshtein
from sklearn.feature_extraction.text import CountVectorizer

from pocs.model_algo_data import sentences_to_compare_dataset

# Initialize all models you specified
models = {
    "MiniLM": SentenceTransformer("all-MiniLM-L6-v2"),
    "ATTACK-BERT": SentenceTransformer("basel/ATTACK-BERT"),
    "All-MPNet": SentenceTransformer("all-MPNet-base-v2"),
    "SecBERT": SentenceTransformer("jackaduma/SecBERT"),
    "STAR-QA": SentenceTransformer("dptrsa/STAR-QA"),
    "Legal-XLM": SentenceTransformer("Stern5497/sbert-legal-xlm-roberta-base"),
}


# Function to compute similarities
def compute_similarities(first_sentence, second_sentence, selected_model):
    model = models[selected_model]
    embeddings = model.encode([first_sentence, second_sentence])

    results = {
        "Cosine Similarity": cosine_similarity([embeddings[0]], [embeddings[1]])[0][0],
        "Euclidean Distance": euclidean_distances([embeddings[0]], [embeddings[1]])[0][
            0
        ],
        "Manhattan Distance": manhattan_distances([embeddings[0]], [embeddings[1]])[0][
            0
        ],
    }

    # Mahalanobis Distance (Handles singular matrix issues)
    try:
        cov_matrix = np.cov(np.array([embeddings[0], embeddings[1]]), rowvar=False)
        inv_cov_matrix = np.linalg.inv(cov_matrix)
        results["Mahalanobis Distance"] = distance.mahalanobis(
            embeddings[0], embeddings[1], inv_cov_matrix
        )
    except np.linalg.LinAlgError:
        results["Mahalanobis Distance"] = "Singular Matrix"

    # Jaccard Similarity
    vectorizer = CountVectorizer().fit_transform([first_sentence, second_sentence])
    results["Jaccard Similarity"] = jaccard_similarity(vectorizer)

    # Levenshtein Distance
    results["Levenshtein Distance"] = Levenshtein.distance(
        first_sentence, second_sentence
    )

    # Hamming Distance (Only if lengths match)
    if len(first_sentence) == len(second_sentence):
        results["Hamming Distance"] = sum(
            c1 != c2 for c1, c2 in zip(first_sentence, second_sentence)
        )
    else:
        results["Hamming Distance"] = "N/A (Different Lengths)"

    return results


# Jaccard Similarity function
def jaccard_similarity(vectorizer):
    set_1 = set(vectorizer[0].indices)
    set_2 = set(vectorizer[1].indices)
    intersection = len(set_1 & set_2)
    union = len(set_1 | set_2)
    return intersection / union if union != 0 else 0


# Precompute all model-algo results and save to CSV
def precompute_all_results():
    precomputed_results = []

    for model_name in models:
        for entry in sentences_to_compare_dataset:
            print(f"Computing for {model_name} on '{entry['description']}'")
            comparison_results = compute_similarities(
                entry["first_sentence"], entry["second_sentence"], model_name
            )

            row = {
                "Description": entry["description"],
                "First Sentence": entry["first_sentence"],
                "Second Sentence": entry["second_sentence"],
                "Model": model_name,
            }
            row.update(comparison_results)

            precomputed_results.append(row)

    df = pd.DataFrame(precomputed_results)
    df.to_csv("./experimentals/cached_data.csv", index=False)
    print(
        f"✅ Precomputed results saved to cached_data.csv with {len(precomputed_results)} entries."
    )


# Run the precomputation and save to a file
precompute_all_results()
