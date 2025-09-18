from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

# List of models to query
MODELS = [
    "claude-sonnet-4-20250514",  # Using Claude Sonnet 4 model
]


class BaseDocument(BaseModel):
    """Base document properties without score"""

    text: str
    id: Optional[str] = None


class Document(BaseDocument):
    """Document with optional score"""

    score: Optional[float] = None


class RerankedDocument(BaseDocument):
    """Document that has been reranked with a required score"""

    text: str
    id: Optional[str] = None
    score: float


class QuestionContext(BaseModel):
    """Contains all context and content for a processed question"""

    question: str
    documents: List[Document]
    context: str
    prompt: str
    raw_documents: List[str]


class ModelResponse(BaseModel):
    """Response from a single model"""

    model: str
    response: str
    evaluation: Optional[Any] = None


class QuestionResult(BaseModel):
    """Final result for a question with all model responses"""

    question: str
    documents: List[Document]
    model_responses: Dict[str, str]


class RerankRequest(BaseModel):
    """Request payload for reranking API"""

    query: str
    documents: List[Dict[str, Any]]
    top_n: int
    model: str
