from sentence_transformers import SentenceTransformer

model = SentenceTransformer("BAAI/bge-small-en")

def create_embedding(text):

    embedding = model.encode(text)

    return embedding