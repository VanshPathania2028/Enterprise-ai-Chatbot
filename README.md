# Enterprise AI Chatbot

An enterprise-level AI chatbot built using FastAPI, Ollama, RAG, GraphRAG, LangGraph, LlamaIndex, MCP, ChromaDB, and Neo4j.

## Features

- AI chat using Ollama
- Retrieval-Augmented Generation
- GraphRAG using Neo4j
- Hybrid retrieval
- Conversation memory
- LlamaIndex integration
- LangGraph workflow
- MCP integration
- FastAPI REST API
- Logging and error handling
- Unit and integration testing
- Docker support

## Technology Stack

- Python
- FastAPI
- Ollama
- ChromaDB
- Neo4j
- LangGraph
- LlamaIndex
- MCP SDK
- Pytest
- Locust
- Docker

## Project Structure

```text
ENTERPRISE-AI-CHATBOT/
│
├── agents/
├── app/
├── chatbot/
├── documents/
├── graphrag/
├── hybrid/
├── langgraph/
├── llama_index/
├── llm/
├── logs/
├── mcp/
├── memory/
├── rag/
├── reranker/
├── tests/
├── vectorstore/
│
├── main.py
├── config.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .env
└── README.md


## Application Screenshots

### Welcome Dashboard

![Welcome Dashboard](screenshots/welcome-dashboard.png)

### Chat Interface

![Chat Interface](screenshots/chat-interface.png)

### Document Upload

![Document Upload](screenshots/pdf-upload.png)

### Analytics Dashboard

![Analytics Dashboard](screenshots/analytics-dashboard.png)