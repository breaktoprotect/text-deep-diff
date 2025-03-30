import streamlit as st
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

# Example dataset
sentences_to_compare_dataset = [
    {
        "description": "Similar English text True",
        "first_sentence": "Regular exercise strengthens the heart and improves overall health.",
        "second_sentence": "Engaging in physical activities like jogging or swimming helps maintain cardiovascular fitness.",
    },
    {
        "description": "Similar English text False",
        "first_sentence": "Regular exercise strengthens the heart and improves overall health.",
        "second_sentence": "Watching movies is a great way to relax and unwind.",
    },
    {
        "description": "Matching configuration setting to MITRE ATT&CK technique True",
        "first_sentence": "T1557.001 - LLMNR/NBT-NS Poisoning and SMB Relay",
        "second_sentence": "Ensure 'Turn off multicast name resolution' is set to 'Enabled' to mitigate LLMNR and NetBIOS Name Service spoofing attacks.",
    },
    {
        "description": "Matching configuration setting to MITRE ATT&CK technique False",
        "first_sentence": "T1557.001 - LLMNR/NBT-NS Poisoning and SMB Relay",
        "second_sentence": "Ensure 'Guest account status' is set to 'Enabled' to facilitate easier access for shared resources.",
    },
    {
        "description": "Cyber Security GRC Subset True",
        "first_sentence": "Endpoint Protection and Threat Management",
        "second_sentence": "All endpoint devices and servers must be protected by enterprise-grade EDR and antivirus solutions, ensuring continuous threat monitoring, detection, and response in compliance with regulatory and internal security requirements.",
    },
    {
        "description": "Cyber Security GRC Subset False",
        "first_sentence": "Endpoint Protection and Threat Management",
        "second_sentence": "All privileged accounts must use multi-factor authentication (MFA) to prevent unauthorized access.",
    },
]

# Initialize the models
models = {
    "MiniLM": SentenceTransformer("all-MiniLM-L6-v2"),
    "ATTACK-BERT": SentenceTransformer("basel/ATTACK-BERT"),
    "All-MPNet": SentenceTransformer("all-MPNet-base-v2"),
    "Legal-BERT": SentenceTransformer("nlpaueb/legal-bert-base-uncased"),
    "SecBERT": SentenceTransformer("jackaduma/SecBERT"),
}


# Function to compute similarities (as before)
def compute_similarities(
    first_sentence, second_sentence, selected_model, selected_algo
):
    model = models[selected_model]
    embeddings = model.encode([first_sentence, second_sentence])

    results = {}

    # Cosine Similarity
    if selected_algo == "Cosine Similarity":
        similarity = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
        results["Cosine Similarity"] = similarity

    # Euclidean Distance
    elif selected_algo == "Euclidean Distance":
        distance_euc = euclidean_distances([embeddings[0]], [embeddings[1]])[0][0]
        results["Euclidean Distance"] = distance_euc

    # Manhattan Distance
    elif selected_algo == "Manhattan Distance":
        distance_man = manhattan_distances([embeddings[0]], [embeddings[1]])[0][0]
        results["Manhattan Distance"] = distance_man

    # Mahalanobis Distance
    elif selected_algo == "Mahalanobis Distance":
        try:
            mahalanobis_dist = distance.mahalanobis(
                embeddings[0],
                embeddings[1],
                np.linalg.inv(np.cov([embeddings[0], embeddings[1]], rowvar=False)),
            )
            results["Mahalanobis Distance"] = mahalanobis_dist
        except np.linalg.LinAlgError:
            results["Mahalanobis Distance"] = "Singular Matrix"

    # Jaccard Similarity
    elif selected_algo == "Jaccard Similarity":
        vectorizer = CountVectorizer().fit_transform([first_sentence, second_sentence])
        jaccard_sim = jaccard_similarity(vectorizer)
        results["Jaccard Similarity"] = jaccard_sim

    # Levenshtein Distance
    elif selected_algo == "Levenshtein Distance":
        lev_distance = Levenshtein.distance(first_sentence, second_sentence)
        results["Levenshtein Distance"] = lev_distance

    # Hamming Distance
    elif selected_algo == "Hamming Distance":
        hamming_dist = hamming_distance(first_sentence, second_sentence)
        results["Hamming Distance"] = hamming_dist

    return results


# Precompute all model-algo results only once and store in session_state
def precompute_all_results():
    precomputed_results = {}
    for model_name in models:
        for algo in [
            "Cosine Similarity",
            "Euclidean Distance",
            "Manhattan Distance",
            "Mahalanobis Distance",
            "Jaccard Similarity",
            "Levenshtein Distance",
            "Hamming Distance",
        ]:
            model_results = []
            for entry in sentences_to_compare_dataset:
                comparison_results = compute_similarities(
                    entry["first_sentence"],
                    entry["second_sentence"],
                    model_name,
                    algo,
                )
                row = {
                    "Description": entry["description"],
                    "First Sentence": (
                        entry["first_sentence"][:80] + "..."
                        if len(entry["first_sentence"]) > 80
                        else entry["first_sentence"]
                    ),
                    "Second Sentence": (
                        entry["second_sentence"][:80] + "..."
                        if len(entry["second_sentence"]) > 80
                        else entry["second_sentence"]
                    ),
                }
                row.update(comparison_results)
                model_results.append(row)

            precomputed_results[(model_name, algo)] = pd.DataFrame(model_results)
    return precomputed_results


# Jaccard Similarity function
def jaccard_similarity(vectorizer):
    set_1 = set(vectorizer[0].indices)
    set_2 = set(vectorizer[1].indices)
    intersection = len(set_1 & set_2)
    union = len(set_1 | set_2)
    return intersection / union if union != 0 else 0


# Hamming Distance function
def hamming_distance(str1, str2):
    if len(str1) != len(str2):
        return float("inf")
    return sum(el1 != el2 for el1, el2 in zip(str1, str2))


# Streamlit UI to select Model and Algorithm
st.title("Sentence Comparison")

# Check if precomputation has already been done (only once)
if "precomputed_results" not in st.session_state:
    with st.spinner("Precomputing all results..."):
        st.session_state.precomputed_results = precompute_all_results()

# Model selection
selected_model = st.selectbox(
    "Select Model", options=["MiniLM", "ATTACK-BERT", "All-MPNet"]
)

# Algorithm selection
selected_algo = st.selectbox(
    "Select Algorithm",
    options=[
        "Cosine Similarity",
        "Euclidean Distance",
        "Manhattan Distance",
        "Mahalanobis Distance",
        "Jaccard Similarity",
        "Levenshtein Distance",
        "Hamming Distance",
    ],
)

# Table display button
if st.button("Display Results"):
    # Fetch the precomputed results from session state
    selected_results = st.session_state.precomputed_results.get(
        (selected_model, selected_algo)
    )

    # Display the results if they exist
    if selected_results is not None:
        st.dataframe(selected_results, use_container_width=True)
    else:
        st.write(
            "No results available for the selected model and algorithm combination."
        )
