import re

def chunk_text(text, chunk_size=512, overlap=50, by_sentence=False):
    if by_sentence:
        sentences = re.split(r'(?<=[.!?]) +', text.strip())
        return sentences
    else:
        words = text.split()
        chunks = []
        for i in range(0, len(words), chunk_size - overlap):
            chunk = " ".join(words[i:i + chunk_size])
            chunks.append(chunk)
        return chunks