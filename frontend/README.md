# Enterprise AI Chatbot

An enterprise-level AI assistant built using FastAPI, React, Ollama, Hybrid RAG, GraphRAG, Neo4j, ChromaDB, LlamaIndex, LangGraph and MCP.

The application allows users to upload PDF documents, index document content, ask questions using natural language and receive AI-generated answers with document sources.

---

## Project Overview

The Enterprise AI Chatbot is designed to provide intelligent question answering over enterprise documents.

It combines multiple AI retrieval and orchestration technologies:

- Standard RAG
- Hybrid RAG
- GraphRAG
- Vector search
- Knowledge graph search
- LLM-based response generation
- Tool integration through MCP
- Workflow orchestration through LangGraph

The chatbot runs locally using Ollama, which avoids dependency on paid cloud-based AI APIs.

---

## Main Features

- AI-powered enterprise chatbot
- Local LLM using Ollama
- PDF document upload
- Automatic PDF text extraction
- Text chunking and document indexing
- ChromaDB vector storage
- Neo4j knowledge graph
- Hybrid document retrieval
- GraphRAG relationship retrieval
- Source citations in chatbot responses
- Document management
- Delete indexed documents
- Backend health monitoring
- Analytics dashboard
- Chat history using local storage
- Export chat as TXT
- Export chat as Markdown
- Responsive React interface
- Markdown answer rendering
- Copy chatbot responses
- Drag-and-drop file upload

---

## Technology Stack

### Frontend

- React
- Vite
- JavaScript
- Tailwind CSS
- Axios
- Lucide React
- React Markdown

### Backend

- Python
- FastAPI
- Uvicorn
- Pydantic
- SQLAlchemy

### Artificial Intelligence

- Ollama
- Llama 3.2
- LlamaIndex
- LangGraph
- RAG
- Hybrid RAG
- GraphRAG
- Embedding models

### Databases

- ChromaDB
- Neo4j
- SQLite

### Integration

- MCP Server
- MCP Client
- REST API

---

## System Architecture

```text
User
  |
  v
React Frontend
  |
  v
FastAPI REST API
  |
  +-----------------------------+
  |                             |
  v                             v
Hybrid RAG Pipeline        LangGraph Workflow
  |                             |
  +-------------+---------------+
                |
                v
       Retrieval Components
                |
       +--------+--------+
       |                 |
       v                 v
   ChromaDB          Neo4j Graph
       |                 |
       +--------+--------+
                |
                v
            Ollama LLM
                |
                v
        Generated Response
                |
                v
      Answer with Sources


## Application Screenshots

### Welcome Dashboard

![Welcome Dashboard](screenshots/welcome-dashboard.png)

### Chat Interface

![Chat Interface](screenshots/chat-interface.png)

### Document Upload

![Document Upload](screenshots/pdf-upload.png)

### Analytics Dashboard

![Analytics Dashboard](screenshots/analytics-dashboard.png)