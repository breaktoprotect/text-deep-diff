from sentence_transformers import SentenceTransformer, util

# Load a small but effective model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Load and chunk document
with open("./experimentals/sample_policy.txt", "r") as f:
    paragraphs = [p.strip() for p in f.readlines() if p.strip()]

# Embed all paragraphs
paragraph_embeddings = model.encode(paragraphs, convert_to_tensor=True)

# Sample query
query = "What do we do about service accounts?"
query = "What's the password policy?"


query_embedding = model.encode(query, convert_to_tensor=True)

# Search
cos_scores = util.cos_sim(query_embedding, paragraph_embeddings)[0]
# top_results = cos_scores.argsort(descending=True)[:3]
top_results = cos_scores.argsort(descending=True)

print(f"\nQuery: {query}\n")
for idx in top_results:
    print(f"Score: {cos_scores[idx]:.4f} - Match: {paragraphs[idx]}\n")
