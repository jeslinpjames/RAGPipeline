# RAG Pipeline with PDF and Web Scraping

This repository demonstrates a Retrieval-Augmented Generation (RAG) pipeline that integrates content from both PDFs and websites into a vector store. The system then allows querying this vector store using natural language questions.

## Features

- **PDF Processing**: Extracts and processes text and tables from PDF documents.
- **Web Scraping**: Scrapes text and tables from websites, then chunks and adds them to the same vector store as the PDFs.
- **Retrieval-Augmented Generation**: Allows querying of the vector store to retrieve and generate responses based on the combined content from PDFs and websites.
