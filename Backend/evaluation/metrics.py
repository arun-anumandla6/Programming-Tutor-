from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

def semantic_similarity(answer, ground_truth):
    emb1 = model.encode([answer])
    emb2 = model.encode([ground_truth])
    score = cosine_similarity(emb1, emb2)[0][0]
    return float(score)
def retrieval_recall(retrieved_docs, relevant_docs):
    retrieved_set = set(retrieved_docs)
    relevant_set = set(relevant_docs)

    if len(relevant_set) == 0:
        return 0.0

    correct = retrieved_set.intersection(relevant_set)
    recall = len(correct) / len(relevant_set)

    return recall