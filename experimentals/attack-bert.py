from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

sentences = ["Attacker takes a screenshot", "Attacker captures the screen"]

# Model: ATTACK-BERT
model = SentenceTransformer("basel/ATTACK-BERT")
embeddings = model.encode(sentences)
print("ATTACK-BERT Similarity:", cosine_similarity([embeddings[0]], [embeddings[1]]))

# Model: MiniLM
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
embeddings = model.encode(sentences)
print("MiniLM Similarity:", cosine_similarity([embeddings[0]], [embeddings[1]]))

# Model: all-mpnet-base-v2
model = SentenceTransformer("sentence-transformers/all-mpnet-base-v2")
embeddings = model.encode(sentences)
print(
    "all-mpnet-base-v2 Similarity:", cosine_similarity([embeddings[0]], [embeddings[1]])
)
