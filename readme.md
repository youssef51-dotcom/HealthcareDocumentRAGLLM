# Medical PDF Information Extraction Pipeline

This project provides an end to end pipeline for extracting structured clinical information from medical PDF documents. It combines document parsing, semantic chunking, vector search using FAISS, and large language models to produce reliable structured outputs.

## Overview

The system processes medical PDFs such as clinical case reports and reviews. It extracts relevant sections, builds semantic embeddings, retrieves the most relevant content, and uses a language model to convert that content into structured JSON.

The goal is to enable accurate retrieval of patient level information such as demographics, diagnosis, findings, and treatment.

## Features

PDF parsing with support for one column and two column layouts
Section and heading detection
Chunking with overlap for contextual continuity
Semantic embedding using sentence transformers
FAISS vector index for fast similarity search
Retrieval augmented generation pipeline
Structured information extraction using a language model
Pydantic validation with repair loop
Modular and extensible architecture

## Project Structure

data
Contains input PDF files

ingestion
Handles PDF reading, layout detection, heading extraction, and chunking

llm
Handles prompt construction, provider abstraction, and extraction logic

models
Defines Pydantic schemas for structured output

rag
Contains embedding logic and FAISS index utilities

utils
Logging and validation helpers

pipeline.py
Main entry point for running the full pipeline

requirements.txt
Project dependencies

## Pipeline Description

The pipeline consists of the following steps:

1. PDF ingestion
   The document is parsed and text is extracted with layout awareness. Headings and sections are detected and the content is split into chunks with overlap.

2. Embedding and indexing
   Each chunk is converted into a vector embedding. These embeddings are stored in a FAISS index for efficient similarity search.

3. Retrieval
   A semantic query is embedded and used to retrieve the most relevant chunks from the FAISS index.

4. Structured extraction
   The retrieved content is passed to a language model with a strict prompt. The model extracts structured clinical data in JSON format.

5. Validation and repair
   The output is validated using a Pydantic schema. If validation fails, a repair prompt is triggered to correct the output.

## Installation

Create a virtual environment and install dependencies:

pip install -r requirements.txt

Install and run Ollama if using local models:

ollama pull mistral

## Usage

Run the pipeline from the command line:

python pipeline.py path_to_pdf columnType llmMode

Arguments:

path_to_pdf
Path to the input PDF file

columnType 
1col, 2col, or auto : 1 column per page pdf file or 2 columns per page or automatic choice 

llmMode
local, openai, mock: local model chosen (I worked with ollama and mistral), openai or mock dummy json sent

## Output Format

The system outputs structured JSON in the following schema:

{
"patient": {
"age": int or null,
"sex": "male" or "female" or null
},
"diagnosis": string or null,
"findings": [string],
"treatment": string or null
}

## Configuration

The language model provider can be configured in the provider factory. The system currently supports local models via Ollama and can be extended to other providers.

Chunk size, overlap, and retrieval parameters can be adjusted in the ingestion and RAG modules.

## Notes

FAISS stores only vector embeddings. The original chunks are stored separately and mapped by index during retrieval.

The quality of extraction depends heavily on chunk quality and retrieval accuracy. Filtering non clinical sections such as references improves results.

## Future Improvements

Improved section classification for clinical relevance
Hybrid retrieval combining keyword and vector search
Better validation with semantic checks
Support for multi document indexing
Evaluation metrics for extraction quality

## License

This project is provided for research and educational purposes.
