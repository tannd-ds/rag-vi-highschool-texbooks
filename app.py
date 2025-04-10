from rag.embed import load_embedding_model, embed_texts
from rag.indexer import QdrantVectorStore
from rag.retriever import retrieve
from rag.generator import format_prompt, GeminiClient

# Step 1: Load model
model = load_embedding_model()
answer_model = GeminiClient()

# Step 3: Create Qdrant index
book_id = "153_ngu-van-10-tap-1"
docs_dir = f"data/{book_id}/text"
dim = 1024

# Step 3: Create Qdrant index
index = QdrantVectorStore(
    collection_name=book_id,
    dim=dim,
)

while True:
    question = input("Enter your question (or 'exit' to quit): ")
    if question.lower() == 'exit':
        break

    question = question.strip()
    contexts = retrieve(index, model, question)
    prompt = format_prompt(contexts, question)

    print("\nGenerated Prompt:\n")
    print(prompt)

    answer = answer_model.generate_answer(prompt)
    print("\nGenerated Answer:\n", answer)
