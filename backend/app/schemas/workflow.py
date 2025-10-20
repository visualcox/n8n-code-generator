"""
Pydantic schemas for workflow generation
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class UserRequirement(BaseModel):
    """User's initial requirement input"""
    requirement: str = Field(..., description="User's workflow requirement description")
    context: Optional[str] = Field(None, description="Additional context")


class Question(BaseModel):
    """Question to ask user for clarification"""
    id: str
    question: str
    question_type: str  # text, choice, multiple_choice
    options: Optional[List[str]] = None
    required: bool = True


class Answer(BaseModel):
    """User's answer to a question"""
    question_id: str
    answer: str


class AnalyzedRequirement(BaseModel):
    """Analyzed requirement with questions"""
    summary: str
    identified_components: List[str]
    missing_information: List[str]
    questions: List[Question]
    estimated_complexity: str  # simple, medium, complex


class DevelopmentSpec(BaseModel):
    """Development specification document"""
    title: str
    objective: str
    user_requirements: Dict[str, Any]
    workflow_steps: List[Dict[str, Any]]
    required_nodes: List[str]
    node_configurations: Dict[str, Any]
    data_flow: List[Dict[str, str]]
    error_handling: List[str]
    testing_criteria: List[str]
    estimated_cost: Optional[str] = None


class TestResult(BaseModel):
    """Test result for generated workflow"""
    passed: bool
    issues: List[str]
    suggestions: List[str]
    optimization_opportunities: List[str]


class WorkflowResponse(BaseModel):
    """Complete workflow generation response"""
    id: int
    status: str
    user_requirement: str
    analyzed_requirement: Optional[Dict[str, Any]] = None
    questions_asked: Optional[List[Question]] = None
    development_spec: Optional[str] = None
    generated_json: Optional[str] = None
    test_results: Optional[Dict[str, Any]] = None
    final_json: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class WorkflowListResponse(BaseModel):
    """List of workflow requests"""
    total: int
    items: List[WorkflowResponse]


class LLMConfigCreate(BaseModel):
    """Create LLM configuration"""
    name: str
    provider: str  # openai, anthropic, ollama, custom
    api_key: Optional[str] = None
    api_url: Optional[str] = None
    model_name: str
    temperature: int = Field(70, ge=0, le=100)
    max_tokens: int = Field(4000, ge=100, le=32000)
    is_default: bool = False


class LLMConfigResponse(BaseModel):
    """LLM configuration response"""
    id: int
    name: str
    provider: str
    api_url: Optional[str] = None
    model_name: str
    temperature: int
    max_tokens: int
    is_active: bool
    is_default: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class LearnedExampleResponse(BaseModel):
    """Learned example response"""
    id: int
    title: str
    description: Optional[str]
    source: str
    source_url: Optional[str]
    tags: Optional[List[str]]
    nodes_used: Optional[List[str]]
    complexity_level: Optional[str]
    stars: int
    learned_at: datetime
    
    class Config:
        from_attributes = True
