# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a RAG (Retrieval-Augmented Generation) project that implements document retrieval and reranking capabilities for question-answering about Jeff Bezos. It uses a vector store (Vectorize) for document retrieval and supports multiple reranking strategies.

## Environment Setup

### Required Environment Variables
```bash
VECTORIZE_ENDPOINT   # Endpoint for the Vectorize vector store API
VECTORIZE_TOKEN      # Authentication token for Vectorize
COHERE_API_KEY       # API key for Cohere reranking service
QUOTIENT_API_KEY     # API key for Quotient AI hallucination detection
```

### Python Environment
- Uses Python 3.12+ (specified in `.python-version`)
- Virtual environment expected at `.venv/`
- Dependencies managed via `pyproject.toml` with `uv.lock` lockfile

## Key Commands

### Setup Virtual Environment
```bash
python -m venv .venv
source .venv/bin/activate  # On Linux/Mac
# or
.venv\Scripts\activate  # On Windows
```

### Install Dependencies
```bash
pip install -e .
# or if using uv:
uv sync
```

### Run Examples
```bash
# Run manual reranking with Cohere
python manual-reranking.py

# Run built-in Vectorize reranking
python built-in-reranking.py

# Test the Cohere reranker wrapper
python rerank_wrapper.py
```

## Architecture

### Core Components

1. **retrieval.py**: Interfaces with Vectorize API to retrieve documents from the vector store. Supports optional built-in reranking.

2. **rerank_wrapper.py**: Implements Cohere's reranking API wrapper (`CohereReranker` class) for reordering documents by relevance.

3. **llm.py**: Handles LLM queries via LiteLLM, supporting multiple model providers. Builds prompts with retrieved context.

4. **eval.py**: Integrates Quotient AI for hallucination detection and provides formatted output of evaluation results.

5. **models.py**: Pydantic models defining data structures for documents, questions, and API responses.

### Workflow Patterns

**Basic RAG Pipeline:**
1. Query Vectorize for relevant documents
2. Optionally rerank documents (Cohere or built-in)
3. Build prompt with question + context
4. Query LLM model(s)
5. Evaluate for hallucinations (optional)

**Two Main Approaches:**
- **manual-reranking.py**: Retrieves documents, then uses Cohere API for reranking
- **built-in-reranking.py**: Uses Vectorize's built-in reranking in a single API call

### Key Design Decisions

- Uses Pydantic for data validation across all API interactions
- Supports multiple LLM providers through LiteLLM abstraction
- Modular design allows swapping reranking strategies
- Document texts are passed as raw strings to evaluation services
- All document IDs are optional and handled gracefully