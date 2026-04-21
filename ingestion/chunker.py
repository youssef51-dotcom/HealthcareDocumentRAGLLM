def chunk_text(text, chunk_size=250, overlap=50):
    """
    Split text into overlapping chunks.

    chunk_size: number of words per chunk
    overlap: number of words shared between chunks
    """

    words = text.split()
    chunks = []

    start = 0

    while start < len(words):
        end = start + chunk_size
        chunk = words[start:end]

        if not chunk:
            break

        chunks.append(" ".join(chunk))

        start += chunk_size - overlap

    return chunks

def build_rag_chunks(sections):
    all_chunks = []

    for sec in sections:
        text = sec["heading"] + ". " + sec["content"]

        chunks = chunk_text(text)

        for i, c in enumerate(chunks):
            all_chunks.append({
                "section": sec["heading"],
                "chunk_id": i,
                "text": c
            })

    return all_chunks