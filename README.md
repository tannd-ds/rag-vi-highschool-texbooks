# High school Textbook End-to-End Retrieval Augmented Generation

- Crawl all the textbooks from the website: https://www.hoc10.vn/
- ORC all the textbooks
- Index all the textbooks

ORC: https://huggingface.co/5CD-AI/Vintern-1B-v2

# High School Textbook RAG: Question Answering System

## Overview

This project implements an end-to-end Retrieval-Augmented Generation (RAG) system capable of answering questions based on the content of Vietnamese high school textbooks. The system leverages state-of-the-art AI models for document processing, text embedding, vector storage, retrieval, and answer generation, demonstrating proficiency in building complex AI pipelines.

The primary goal is to create an intelligent assistant that can understand and respond to user queries by referencing specific information within a corpus of digitized high school textbooks.

## Features

* **Web Crawling:** Extracts textbook data (images and metadata) directly from online sources (e.g., hoc10.vn) [cite: highschool_textbook_rag/extract_book.py].
* **Optical Character Recognition (OCR):** Employs a powerful Vision-Language Model (`5CD-AI/Vintern-1B-v2`) to accurately extract text content, including titles and formatting, from textbook images [cite: highschool_textbook_rag/orc.py].
* **Text Processing:** Implements text chunking strategies (e.g., by sentence or fixed size with overlap) to prepare text for embedding [cite: highschool_textbook_rag/rag/utils.py].
* **Dense Text Embedding:** Utilizes the `BAAI/bge-m3` model via the `FlagEmbedding` library to generate high-dimensional vector representations (embeddings) of text chunks, capturing semantic meaning [cite: highschool_textbook_rag/rag/embed.py].
* **Vector Indexing & Storage:** Leverages Qdrant, an efficient vector database, to store and index text embeddings for fast retrieval, using Cosine similarity for distance measurement [cite: highschool_textbook_rag/rag/indexer.py, highschool_textbook_rag/data/qdrant_storage/collections/153_ngu-van-10-tap-1/config.json, highschool_textbook_rag/data/qdrant_storage/collections/embeddings/config.json].
* **Semantic Retrieval:** Implements a retrieval mechanism that finds the most relevant text chunks (contexts) from the vector store based on the semantic similarity of the user's query embedding [cite: highschool_textbook_rag/rag/retriever.py].
* **Large Language Model (LLM) Integration:** Integrates with Google's Gemini API (`gemini-2.0-flash` model) for generative question answering [cite: highschool_textbook_rag/rag/generator.py].
* **Prompt Engineering:** Formats retrieved contexts and the user's question into an effective prompt to guide the LLM in generating accurate and contextually relevant answers [cite: highschool_textbook_rag/rag/generator.py].
* **End-to-End Application:** Provides an interactive command-line interface (`app.py`) demonstrating the complete RAG workflow from question input to answer output [cite: highschool_textbook_rag/app.py].

## Technical Stack

* **Programming Language:** Python
* **Core Libraries:**
    * `transformers`: For loading and using the Vintern-1B-v2 OCR model [cite: highschool_textbook_rag/orc.py].
    * `FlagEmbedding`: For loading and using the BAAI/bge-m3 embedding model [cite: highschool_textbook_rag/rag/embed.py, highschool_textbook_rag/requirements.txt].
    * `qdrant-client`: For interacting with the Qdrant vector database [cite: highschool_textbook_rag/rag/indexer.py, highschool_textbook_rag/requirements.txt].
    * `google-genai`: For interacting with the Gemini LLM API [cite: highschool_textbook_rag/rag/generator.py].
    * `requests`: For web crawling [cite: highschool_textbook_rag/extract_book.py, highschool_textbook_rag/requirements.txt].
    * `Pillow (PIL)`: For image processing in the OCR pipeline [cite: highschool_textbook_rag/orc.py].
    * `torch`, `torchvision`, `timm`, `flash-attn`, `einops`: Dependencies for the OCR and potentially embedding models [cite: highschool_textbook_rag/requirements.txt, highschool_textbook_rag/orc.py].
    * `dotenv`: For managing API keys [cite: highschool_textbook_rag/rag/generator.py].
* **Models:**
    * OCR: `5CD-AI/Vintern-1B-v2` [cite: highschool_textbook_rag/orc.py]
    * Embedding: `BAAI/bge-m3` [cite: highschool_textbook_rag/rag/embed.py]
    * Generation: `gemini-2.0-flash` (via Google GenAI API) [cite: highschool_textbook_rag/rag/generator.py]
* **Vector Database:** Qdrant [cite: highschool_textbook_rag/rag/indexer.py]

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
    * Add your Google Gemini API key: `GEMINI_API_KEY='YOUR_API_KEY'` [cite: highschool_textbook_rag/rag/generator.py].
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

* **AI Pipeline Development:** Designing and implementing a multi-stage AI workflow involving data extraction, preprocessing, OCR, embedding, indexing, retrieval, and generation.
* **NLP & Information Retrieval:** Applying text chunking techniques, utilizing state-of-the-art embedding models (BGE-M3) for semantic understanding, and implementing vector-based retrieval using Qdrant.
* **Computer Vision (OCR):** Integrating and utilizing advanced Vision-Language Models (Vintern-1B-v2) for accurate text extraction from images.
* **LLM Integration & Prompt Engineering:** Interfacing with large language models (Gemini) via APIs and crafting effective prompts for RAG tasks.
* **Vector Databases:** Experience with setting up and using Qdrant for efficient similarity search on high-dimensional data.
* **Software Engineering:** Structuring code into modular components (data extraction, OCR, RAG modules), managing dependencies (`requirements.txt`), and building a functional application (`app.py`).
* **Problem Solving:** Addressing the challenge of building a question-answering system for a specific domain (high school textbooks) using modern AI techniques.
* **Web Crawling:** Developing scripts to automate data collection from web sources.

## Future Improvements (Optional)

* Implement a web interface (e.g., using Flask/Streamlit) for easier user interaction.
* Expand the textbook corpus and implement multi-collection search.
* Experiment with different embedding models, LLMs, or vector databases.
* Incorporate techniques for handling tables, charts, and complex layouts within textbooks.
* Add evaluation metrics to assess retrieval and generation quality.
* Optimize indexing and retrieval performance for larger datasets.