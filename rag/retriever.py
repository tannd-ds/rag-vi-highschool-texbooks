def retrieve(index, model, query, top_k=3):
    query_embedding = model.encode([query])['dense_vecs']
    return index.search(query_embedding, top_k)