import os

from rag.embed import load_embedding_model, embed_texts
from rag.utils import chunk_text
from rag.indexer import QdrantVectorStore

model = load_embedding_model()

book_id = "153_ngu-van-10-tap-1"
docs_dir = f"data/{book_id}/text"

dim = 1024

# Step 3: Create Qdrant index
index = QdrantVectorStore(
    collection_name=book_id,
    dim=dim,
)

# # Step 2: Load and preprocess documents
# for doc_name in os.listdir(docs_dir):
#     print('Processing document:', doc_name)
#     if doc_name.endswith('.txt'):
#         with open(os.path.join(docs_dir, doc_name), 'r', encoding='utf-8') as f:
#             sample_doc = f.read()
#
#     chunks = chunk_text(sample_doc)
#     embeddings = embed_texts(model, chunks)
#
#     index.add(embeddings, chunks)

