from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from scipy.spatial.distance import euclidean, cityblock, mahalanobis, hamming
from sklearn.metrics import jaccard_score
from Levenshtein import distance as levenshtein_distance
import numpy as np
from tabulate import tabulate  # Import the tabulate library


# Function to truncate sentences for display
def truncate_sentence(sentence, max_length=50):
    return sentence[:max_length] + "..." if len(sentence) > max_length else sentence


# Updated dataset
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

# List of models to test
models = {
    "ATTACK-BERT": "basel/ATTACK-BERT",
    "MiniLM": "sentence-transformers/all-MiniLM-L6-v2",
    "all-mpnet-base-v2": "sentence-transformers/all-mpnet-base-v2",
}


# Function to compute and store similarity/distance measures for each pair of sentences
def compare_sentences(
    description, first_sentence, second_sentence, model_name, model_path
):
    model = SentenceTransformer(model_path)
    embeddings = model.encode([first_sentence, second_sentence])

    # Cosine Similarity
    cos_sim = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]

    # Euclidean Distance
    euclidean_dist = euclidean(embeddings[0], embeddings[1])

    # Manhattan Distance (L1)
    manhattan_dist = cityblock(embeddings[0], embeddings[1])

    # Jaccard Similarity (Token-based)
    jaccard_sim = jaccard_score(
        np.array(embeddings[0] > 0, dtype=int), np.array(embeddings[1] > 0, dtype=int)
    )

    # Mahalanobis Distance
    cov_matrix = np.cov(np.array([embeddings[0], embeddings[1]]).T)
    inv_cov_matrix = np.linalg.pinv(cov_matrix)  # Use pseudo-inverse for stability
    mahalanobis_dist = mahalanobis(embeddings[0], embeddings[1], inv_cov_matrix)

    # Levenshtein Distance (on raw text, not embeddings)
    lev_dist = levenshtein_distance(first_sentence, second_sentence)

    # Hamming Distance (binary comparison of sign bit)
    hamming_dist = hamming(
        np.sign(embeddings[0]).astype(int), np.sign(embeddings[1]).astype(int)
    ) * len(
        embeddings[0]
    )  # Normalize

    return {
        "description": description,
        "cosine_similarity": cos_sim,
        "euclidean_distance": euclidean_dist,
        "manhattan_distance": manhattan_dist,
        "jaccard_similarity": jaccard_sim,
        "mahalanobis_distance": mahalanobis_dist,
        "levenshtein_distance": lev_dist,
        "hamming_distance": hamming_dist,
        "first_sentence_truncated": truncate_sentence(first_sentence),
        "second_sentence_truncated": truncate_sentence(second_sentence),
    }


# Prepare data for table
table_data = []

# Loop through the dataset and run comparison for each sentence pair in each record
for data in sentences_to_compare_dataset:
    for model_name, model_path in models.items():
        result = compare_sentences(
            data["description"],
            data["first_sentence"],
            data["second_sentence"],
            model_name,
            model_path,
        )
        # Add the result to the table data
        table_data.append(
            [
                result["description"],
                result["first_sentence_truncated"],
                result["second_sentence_truncated"],
                f"{result['cosine_similarity']:.4f}",
                f"{result['euclidean_distance']:.4f}",
                f"{result['manhattan_distance']:.4f}",
                f"{result['jaccard_similarity']:.4f}",
                f"{result['mahalanobis_distance']:.4f}",
                f"{result['levenshtein_distance']}",
                f"{result['hamming_distance']:.4f}",
            ]
        )

# Define table headers
headers = [
    "Description",
    "First Sentence (Truncated)",
    "Second Sentence (Truncated)",
    "Cosine Similarity",
    "Euclidean Distance",
    "Manhattan Distance",
    "Jaccard Similarity",
    "Mahalanobis Distance",
    "Levenshtein Distance",
    "Hamming Distance",
]

# Print the table
print(tabulate(table_data, headers=headers, tablefmt="grid"))
