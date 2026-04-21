import argparse
import json
import time
from ingestion.medical_pdf_preprocessing import extract_pdf_structure
from rag.FAISS_tools import build_faiss_index, save_index, load_index, search
from llm.extractor import extract_structured_data

def main():

    total_start = time.time()

    parser = argparse.ArgumentParser()
    parser.add_argument("pdf", help="Path to PDF file")
    parser.add_argument("pdfType", help="1col 2col or auto")
    parser.add_argument("llmmode", help="local openai or mock")

    args = parser.parse_args()

    #This is the ingestion part. We retrieve chunks from pdf in a json format with section structure
    # information each section is divided in chunks of 350 words and they have a 50 words overlap for
    # context retrieval. Each chunk has this format {"section": str,"chunk_id": int,"text":str}

    print("\n[STEP 1] PDF ingestion started...")
    step_start = time.time()

    results = extract_pdf_structure(args.pdf, args.pdfType)
    print(json.dumps(results, indent=2, ensure_ascii=False))

    step_end = time.time()
    print(f"[STEP 1 DONE] ingestion time: {step_end - step_start:.2f}s\n")


    #This is the rag part. Out of chunk we build faiss index on embedded texts of each chunk
    #we then save both to map them and ease query retrieval and junction between FAISS and LLM

    print("[STEP 2] FAISS index building started...")
    step_start = time.time()

    index, _, resultList = build_faiss_index(results)

    step_end = time.time()
    print(f"[STEP 2 DONE] FAISS build time: {step_end - step_start:.2f}s\n")


    print("[STEP 3] Saving index started...")
    step_start = time.time()

    save_index(index, resultList)

    step_end = time.time()
    print(f"[STEP 3 DONE] saving time: {step_end - step_start:.2f}s\n")

    #search relevant chunks according to our purpose here we will design an adequate query
    print("[STEP 4] Getting relevant chunks...")
    step_start = time.time()

    query = "clinical case report patient age sex male female year year-old old diagnosis treatment findings"
    relevant_chunks = search(query, index,resultList)
    step_end = time.time()
    print(f"[STEP 4 DONE] Getting relevant chunks time: {step_end - step_start:.2f}s\n")
    print(relevant_chunks)

    context = "\n\n".join([c for c in relevant_chunks])

    print("[PIPELINE] Running extraction...")
    result = extract_structured_data(context, args.llmmode)


    total_end = time.time()

    print("=====================================")
    print(f"TOTAL PIPELINE TIME: {total_end - total_start:.2f}s")
    print("=====================================")


if __name__ == "__main__":
    main()