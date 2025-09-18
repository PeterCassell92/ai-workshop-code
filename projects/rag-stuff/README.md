# RAG Stuff - Document Retrieval and Reranking System

A Retrieval-Augmented Generation (RAG) implementation that demonstrates document retrieval and reranking capabilities for question-answering about Star Wars characters and storylines. The system uses Vectorize for vector storage and supports multiple reranking strategies including Cohere and built-in Vectorize reranking.

## Features

- **Vector-based document retrieval** using Vectorize API
- **Multiple reranking strategies**:
  - Manual reranking with Cohere API
  - Built-in Vectorize reranking
- **LLM integration** via Anthropic Claude API
- **Hallucination detection** using Quotient AI
- **Modular architecture** with Pydantic models for data validation

## Prerequisites

- Python 3.12 or higher
- Virtual environment (recommended)

## Installation

1. Clone the repository
2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Linux/Mac
# or
.venv\Scripts\activate  # On Windows
```

3. Install dependencies:
```bash
pip install -e .
# or if using uv:
uv sync
```

4. Copy `.env.example` to `.env` and configure your API keys:
```bash
cp .env.example .env
```

## Environment Variables

The following environment variables are required:

| Variable | Description | Used In |
|----------|-------------|---------|
| `ANTHROPIC_API_KEY` | Anthropic API key for Claude LLM queries | llm.py |
| `VECTORIZE_ENDPOINT` | Vectorize API endpoint URL | retrieval.py |
| `VECTORIZE_TOKEN` | Authentication token for Vectorize | retrieval.py |
| `COHERE_API_KEY` | Cohere API key for reranking service | rerank_wrapper.py |
| `QUOTIENT_API_KEY` | Quotient AI API key for hallucination detection | eval.py |
| `OPENAI_API_KEY` | OpenAI API key (optional, for OpenAI models) | Not currently used |

## Usage

### Manual Reranking with Cohere
```bash
python manual-reranking.py
```
Retrieves documents from Vectorize and then reranks them using Cohere's API.

### Built-in Vectorize Reranking
```bash
python built-in-reranking.py
```
Uses Vectorize's built-in reranking capability in a single API call.

### Test Cohere Reranker
```bash
python rerank_wrapper.py
```
Tests the Cohere reranker wrapper implementation.

## Project Structure

- `retrieval.py` - Vectorize API interface for document retrieval
- `rerank_wrapper.py` - Cohere reranking API wrapper
- `llm.py` - LLM query handling via Anthropic Claude API
- `eval.py` - Quotient AI integration for hallucination detection
- `models.py` - Pydantic models for data structures
- `manual-reranking.py` - Example of manual reranking workflow
- `built-in-reranking.py` - Example using Vectorize's built-in reranking

## Workflow

1. **Query** - Send a question to the system
2. **Retrieve** - Fetch relevant documents from Vectorize vector store
3. **Rerank** (optional) - Reorder documents by relevance using Cohere or built-in methods
4. **Generate** - Build prompt with context and query LLM
5. **Evaluate** (optional) - Check for hallucinations using Quotient AI