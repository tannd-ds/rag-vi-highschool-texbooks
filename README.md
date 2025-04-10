# High School Textbook RAG: Question Answering System

<div style="text-align: center;">
    <img alt="pytorch" src="https://img.shields.io/badge/PyTorch-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white"/>
    <img alt="gemini" src="https://img.shields.io/badge/Google%20Gemini-8E75B2?style=for-the-badge&logo=googlegemini&logoColor=white"/>
    <img alt="openai" src="https://img.shields.io/badge/ChatGPT-74aa9c?style=for-the-badge&logo=openai&logoColor=white" />
    <img alt="langchain" src="https://img.shields.io/badge/langchain-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white"/>
    <img alt="huggingface" src="https://img.shields.io/badge/-HuggingFace-FDEE21?style=for-the-badge&logo=HuggingFace&logoColor=black"/>
</div>

<div style="text-align: center;">
    <img alt="rag" src="https://img.shields.io/badge/Retrieval_Augmented_Generation_%28RAG%29-EE4C2C?style=for-the-badge&logoColor=red"/>
    <img alt="qdrant" src="https://img.shields.io/badge/Qdrant-dc244c?style=for-the-badge&logoColor=red"/>
    <img alt="docker" src="https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white"/>
</div>

## Overview

This project implements an end-to-end Retrieval-Augmented Generation (RAG) system capable of answering questions based on the content of Vietnamese high school textbooks. The system leverages state-of-the-art AI models for document processing, text embedding, vector storage, retrieval, and answer generation, demonstrating proficiency in building complex AI pipelines.

The primary goal is to create an intelligent assistant that can understand and respond to user queries by referencing specific information within a corpus of digitized high school textbooks.

## Features


* **Web Crawling:** Extracts textbook data (images and metadata) directly from online sources (e.g., hoc10.vn).
* **Automated Data Extraction:** Crawls and retrieves textbook images and metadata from online sources.
* **Advanced OCR:** Utilizes a Vision-Language Model to accurately extract text from textbook images.
* **Semantic Text Processing:** Chunks text and generates meaningful vector embeddings using a state-of-the-art model (`BAAI/bge-m3`).
* **Efficient Vector Storage:** Employs *Qdrant* vector database for fast indexing and retrieval of text embeddings.
* **Context-Aware Retrieval:** Finds the most relevant text passages based on semantic similarity to the user's query.
* **LLM-Powered Generation:** Integrates with Google's Gemini/OpenAI GPT API to generate answers based on retrieved context.
* **Interactive QA:** Provides a command-line interface for users to ask questions and receive answers.

## Technical Stack

* **Language:** Python
* **Key Libraries:** `transformers`, `FlagEmbedding`, `qdrant-client`, `google-genai`, `requests`, `Pillow`
* **AI Models:**
    * OCR: `5CD-AI/Vintern-1B-v2`
    * Embedding: `BAAI/bge-m3`
    * Generation: Google Gemini (`gemini-2.0-flash`), OpenAI GPT (`gpt-4o-mini`)
* **Database:** Qdrant (Vector DB)

## Architecture / Pipeline

1.  **Data Acquisition:** Textbook images and metadata are crawled from `hoc10.vn` using `extract_book.py`.
2.  **OCR Processing:** Images are processed by `orc.py` using the Vintern-1B-v2 model to extract text content, saved as `.txt` files [cite: highschool_textbook_rag/orc.py].
3.  **Indexing (Offline):**
    * Text files are read and chunked using `rag/utils.py` [cite: highschool_textbook_rag/one_time_indexing.py].
    * Text chunks are embedded using the BGE-M3 model (`rag/embed.py`) [cite: highschool_textbook_rag/one_time_indexing.py].
    * Embeddings and corresponding text chunks are indexed and stored in a Qdrant collection (`rag/indexer.py`) [cite: highschool_textbook_rag/one_time_indexing.py].
4.  **Querying (Online - `app.py`):**
    * User enters a question.
    * The question is embedded using the BGE-M3 model (`rag/embed.py`, `rag/retriever.py`).
    * The query embedding is used to search the Qdrant index (`rag/indexer.py`, `rag/retriever.py`) for the top-k most similar text chunks (contexts).
    * Contexts and the original question are formatted into a prompt (`rag/generator.py`).
    * The prompt is sent to the Gemini API (`rag/generator.py`) to generate an answer.
    * The generated answer is displayed to the user.

## Setup & Usage

1.  **Prerequisites:**
    * Python 3.x
    * Qdrant instance running (locally or remotely - adjust `host` and `port` in `rag/indexer.py` if needed) [cite: highschool_textbook_rag/rag/indexer.py].
    * GPU recommended for OCR (`orc.py`) and potentially embedding (`rag/embed.py`).
2.  **Installation:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **API Keys:**
    * Create a `.env` file in the project root.
    * Add your Google Gemini API key: `GEMINI_API_KEY='YOUR_API_KEY'`
4.  **Data Preparation:**
    * Run `extract_book.py` to download textbook data (e.g., `python extract_book.py`). This will create image files in `data/{book_id}_{book_name}/pages/`.
    * Run `orc.py` to perform OCR on the downloaded images (e.g., `python orc.py`). This will create text files in `data/{book_id}_{book_name}/text/`. Ensure the correct `pages_dir` is set in `orc.py`.
5.  **Indexing:**
    * Modify `one_time_indexing.py` to specify the correct `book_id` and `docs_dir` for the textbook you want to index [cite: highschool_textbook_rag/one_time_indexing.py].
    * Uncomment the indexing loop in `one_time_indexing.py`.
    * Run the script (e.g., `python one_time_indexing.py`) to embed and index the text data into Qdrant. *Note: This only needs to be done once per textbook.*
6.  **Running the Application:**
    * Modify `app.py` to set the correct `book_id` corresponding to the indexed collection in Qdrant [cite: highschool_textbook_rag/app.py].
    * Run the application: `python app.py`.
    * Enter your questions when prompted. Type 'exit' to quit.

## Skills Demonstrated

This project showcases a range of skills crucial for Data Science and AI Engineering roles:


* **AI/ML Pipeline Construction:** End-to-end design and implementation (Data ingestion, OCR, NLP, Vector DB, LLM).
* **NLP & Information Retrieval:** Text embedding, chunking, semantic search, RAG architecture.
* **Computer Vision:** Application of OCR models for text extraction.
* **LLM Integration:** API usage, prompt engineering for generative tasks.
* **Vector Databases:** Practical experience with Qdrant for similarity search.
* **Software Engineering:** Modular Python code, dependency management.
* **Data Acquisition:** Web crawling techniques.
* **Problem Solving:** Addressing the challenge of building a question-answering system for a specific domain (high school textbooks) using modern AI techniques.

## Future Improvements (Optional)

* Implement a web interface (e.g., using Flask/Streamlit) for easier user interaction.
* Expand the textbook corpus and implement multi-collection search.
* Experiment with different embedding models, LLMs, or vector databases.
* Incorporate techniques for handling tables, charts, and complex layouts within textbooks.
* Add evaluation metrics to assess retrieval and generation quality.
* Optimize indexing and retrieval performance for larger datasets.