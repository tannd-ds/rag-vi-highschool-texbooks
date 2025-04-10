import numpy as np

from abc import ABC, abstractmethod
from typing import List
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
import numpy as np

class BaseVectorStore(ABC):
    @abstractmethod
    def add(self, embeddings, docs):
        pass

    @abstractmethod
    def search(self, query_embedding, top_k):
        pass


class QdrantVectorStore(BaseVectorStore):
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(QdrantVectorStore, cls).__new__(cls)
        return cls._instance

    def __init__(self, collection_name="rag_collection", dim=1024, host="localhost", port=6333):
        self.client = QdrantClient(host=host, port=port)
        self.collection_name = collection_name

        if not self.client.collection_exists(collection_name):
            print(f"Collection {collection_name} does not exist. Creating a new one.")
            self.client.create_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(size=dim, distance=Distance.COSINE),
            )
        self.id_counter = 0
        self.doc_store = {}

    def add(self, embeddings, docs):
        points = []
        for i, (vec, doc) in enumerate(zip(embeddings, docs)):
            points.append(PointStruct(id=self.id_counter, vector=vec.tolist(), payload={"text": doc}))
            self.doc_store[self.id_counter] = doc
            self.id_counter += 1
        self.client.upsert(collection_name=self.collection_name, points=points)

    def search(self, query_embedding, top_k):
        results = self.client.query_points(
            collection_name=self.collection_name,
            query=query_embedding[0].tolist(),
            limit=top_k,
        )
        return [hit.payload["text"] for hit in results.points]

    def reset(self):
        print(f"Deleting collection {self.collection_name}")
        self.client.delete_collection(self.collection_name)
