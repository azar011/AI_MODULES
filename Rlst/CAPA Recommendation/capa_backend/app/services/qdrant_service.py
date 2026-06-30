from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct
)

from dotenv import load_dotenv

import os
import uuid


load_dotenv()


COLLECTION_NAME = "capa_cases"


# client = QdrantClient(
#     url=os.getenv("QDRANT_URL"),
#     api_key=os.getenv("QDRANT_API_KEY")
# )


QDRANT_HOST = os.getenv("QDRANT_HOST", "localhost")
QDRANT_PORT = int(os.getenv("QDRANT_PORT", 6333))

client = QdrantClient(
    host=QDRANT_HOST,
    port=QDRANT_PORT
)

# CREATE COLLECTION IF NOT EXISTS
collections = client.get_collections().collections

collection_names = [c.name for c in collections]


if COLLECTION_NAME not in collection_names:

    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(
            size=384,
            distance=Distance.COSINE
        )
    )


# ADD DATA
def add_case(embedding, case_data):

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=[
            PointStruct(
                id=str(uuid.uuid4()),
                vector=embedding.tolist(),
                payload=case_data
            )
        ]
    )


# SEARCH BEST MATCH
def search_case(query_embedding, top_k=1):

    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_embedding.tolist(),
        limit=top_k
    )

    formatted_results = []


    for item in results.points:

        # payload = item.payload
        # payload["score"] = float(item.score)

        payload = dict(item.payload)
        payload["score"] = float(item.score)

        formatted_results.append(payload)


    return formatted_results
