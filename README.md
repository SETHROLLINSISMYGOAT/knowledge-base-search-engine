# knowledge-base-search-engine

The RAG Knowledge Base Search Engine is a Retrieval-Augmented Generation (RAG) application that allows users to query uploaded PDF documents and receive accurate, AI-generated answers. It leverages OpenAI embeddings to convert documents into vector representations and FAISS for efficient similarity search.

Users can:

Upload PDF documents into the system.

Ingest and index the documents for fast retrieval.

Ask natural language questions and receive synthesized answers based on the document content.

The backend is built with FastAPI, providing a simple API interface for querying and health checks. This project is ideal for organizations or individuals looking to create a searchable knowledge base over large sets of documents.
