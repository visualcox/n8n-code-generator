"""
Database models and connection
"""
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer, String, Text, DateTime, JSON, Boolean
from datetime import datetime
from app.core.config import settings


class Base(DeclarativeBase):
    """Base class for all models"""
    pass


# Create async engine
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    future=True
)

# Create async session factory
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)


class WorkflowRequest(Base):
    """Workflow generation request model"""
    __tablename__ = "workflow_requests"
    
    id = Column(Integer, primary_key=True, index=True)
    user_requirement = Column(Text, nullable=False)
    analyzed_requirement = Column(JSON, nullable=True)
    questions_asked = Column(JSON, nullable=True)
    user_answers = Column(JSON, nullable=True)
    development_spec = Column(Text, nullable=True)
    generated_json = Column(Text, nullable=True)
    test_results = Column(JSON, nullable=True)
    final_json = Column(Text, nullable=True)
    status = Column(String(50), default="pending")  # pending, analyzing, generating, testing, completed, failed
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class LearnedExample(Base):
    """Learned n8n workflow examples"""
    __tablename__ = "learned_examples"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    source = Column(String(255), nullable=False)  # official_docs, github, template
    source_url = Column(String(512), nullable=True)
    workflow_json = Column(Text, nullable=False)
    tags = Column(JSON, nullable=True)
    nodes_used = Column(JSON, nullable=True)
    complexity_level = Column(String(50), nullable=True)  # simple, medium, complex
    stars = Column(Integer, default=0)
    learned_at = Column(DateTime, default=datetime.utcnow)


class LLMConfig(Base):
    """LLM configuration model"""
    __tablename__ = "llm_configs"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    provider = Column(String(50), nullable=False)  # openai, anthropic, ollama, custom
    api_key = Column(String(255), nullable=True)
    api_url = Column(String(512), nullable=True)
    model_name = Column(String(100), nullable=False)
    temperature = Column(Integer, default=70)  # 0-100
    max_tokens = Column(Integer, default=4000)
    is_active = Column(Boolean, default=False)
    is_default = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class LearningLog(Base):
    """Learning system execution log"""
    __tablename__ = "learning_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    learning_type = Column(String(50), nullable=False)  # docs, github, templates
    examples_found = Column(Integer, default=0)
    examples_added = Column(Integer, default=0)
    status = Column(String(50), default="running")  # running, completed, failed
    error_message = Column(Text, nullable=True)
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)


# Dependency to get DB session
async def get_db():
    """Get database session"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


# Initialize database
async def init_db():
    """Initialize database tables"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
