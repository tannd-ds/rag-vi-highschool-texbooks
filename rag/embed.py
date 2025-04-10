from FlagEmbedding import BGEM3FlagModel

def load_embedding_model():
    model = BGEM3FlagModel('BAAI/bge-m3', use_fp16=True)
    return model


def embed_texts(model, texts):
    embeddings = model.encode(texts,
                              batch_size=12,
                              max_length=4096,
                              )['dense_vecs']
    return embeddings