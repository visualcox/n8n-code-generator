"""
Workflow Service for managing workflow generation process
"""
from typing import Dict, Any, List, Optional
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

from app.models.database import WorkflowRequest, LLMConfig
from app.services.llm_service import LLMService
from app.services.learning_service import LearningService
from app.schemas.workflow import (
    UserRequirement,
    Answer,
    DevelopmentSpec,
    WorkflowResponse
)


class WorkflowService:
    """Service for workflow generation"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.learning_service = LearningService(db)
    
    async def _get_active_llm_config(self) -> Optional[Dict[str, Any]]:
        """Get active LLM configuration"""
        stmt = select(LLMConfig).where(LLMConfig.is_active == True).limit(1)
        result = await self.db.execute(stmt)
        config = result.scalar_one_or_none()
        
        if config:
            return {
                "provider": config.provider,
                "api_key": config.api_key,
                "api_url": config.api_url,
                "model_name": config.model_name,
                "temperature": config.temperature,
                "max_tokens": config.max_tokens
            }
        return None
    
    async def create_workflow_request(
        self,
        user_req: UserRequirement
    ) -> WorkflowResponse:
        """Create new workflow generation request"""
        
        # Create request record
        request = WorkflowRequest(
            user_requirement=user_req.requirement,
            status="pending",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        self.db.add(request)
        await self.db.commit()
        await self.db.refresh(request)
        
        return WorkflowResponse.model_validate(request)
    
    async def analyze_requirement(
        self,
        request_id: int
    ) -> Dict[str, Any]:
        """Analyze user requirement and generate questions"""
        
        # Get request
        stmt = select(WorkflowRequest).where(WorkflowRequest.id == request_id)
        result = await self.db.execute(stmt)
        request = result.scalar_one_or_none()
        
        if not request:
            raise ValueError("Request not found")
        
        # Update status
        request.status = "analyzing"
        await self.db.commit()
        
        # Get LLM config and initialize service
        llm_config = await self._get_active_llm_config()
        llm_service = LLMService(
            provider=llm_config.get("provider") if llm_config else None,
            config=llm_config
        )
        
        # Analyze requirement
        analysis = await llm_service.analyze_requirement(
            request.user_requirement,
            context=None
        )
        
        # Save analysis
        request.analyzed_requirement = analysis
        request.questions_asked = analysis.get("questions", [])
        request.status = "awaiting_answers"
        request.updated_at = datetime.utcnow()
        await self.db.commit()
        
        return analysis
    
    async def submit_answers(
        self,
        request_id: int,
        answers: List[Answer]
    ) -> Dict[str, Any]:
        """Submit answers to questions"""
        
        # Get request
        stmt = select(WorkflowRequest).where(WorkflowRequest.id == request_id)
        result = await self.db.execute(stmt)
        request = result.scalar_one_or_none()
        
        if not request:
            raise ValueError("Request not found")
        
        # Save answers
        answers_data = [
            {
                "question_id": ans.question_id,
                "answer": ans.answer,
                "question": next(
                    (q["question"] for q in request.questions_asked if q["id"] == ans.question_id),
                    ""
                )
            }
            for ans in answers
        ]
        
        request.user_answers = answers_data
        request.status = "generating_spec"
        request.updated_at = datetime.utcnow()
        await self.db.commit()
        
        return {"message": "Answers submitted successfully"}
    
    async def generate_development_spec(
        self,
        request_id: int
    ) -> str:
        """Generate development specification"""
        
        # Get request
        stmt = select(WorkflowRequest).where(WorkflowRequest.id == request_id)
        result = await self.db.execute(stmt)
        request = result.scalar_one_or_none()
        
        if not request:
            raise ValueError("Request not found")
        
        # Get relevant examples
        examples = await self.learning_service.get_relevant_examples(
            request.user_requirement,
            limit=10
        )
        
        examples_data = [
            {
                "title": ex.title,
                "description": ex.description,
                "nodes_used": ex.nodes_used,
                "complexity_level": ex.complexity_level,
                "workflow_json": ex.workflow_json
            }
            for ex in examples
        ]
        
        # Get LLM config
        llm_config = await self._get_active_llm_config()
        llm_service = LLMService(
            provider=llm_config.get("provider") if llm_config else None,
            config=llm_config
        )
        
        # Generate spec
        spec = await llm_service.generate_development_spec(
            request.user_requirement,
            request.user_answers or [],
            examples_data
        )
        
        # Save spec
        request.development_spec = spec
        request.status = "spec_review"
        request.updated_at = datetime.utcnow()
        await self.db.commit()
        
        return spec
    
    async def update_development_spec(
        self,
        request_id: int,
        updated_spec: str
    ) -> Dict[str, Any]:
        """Update development specification after user review"""
        
        # Get request
        stmt = select(WorkflowRequest).where(WorkflowRequest.id == request_id)
        result = await self.db.execute(stmt)
        request = result.scalar_one_or_none()
        
        if not request:
            raise ValueError("Request not found")
        
        request.development_spec = updated_spec
        request.status = "spec_approved"
        request.updated_at = datetime.utcnow()
        await self.db.commit()
        
        return {"message": "Development spec updated successfully"}
    
    async def generate_workflow_json(
        self,
        request_id: int
    ) -> str:
        """Generate n8n workflow JSON"""
        
        # Get request
        stmt = select(WorkflowRequest).where(WorkflowRequest.id == request_id)
        result = await self.db.execute(stmt)
        request = result.scalar_one_or_none()
        
        if not request:
            raise ValueError("Request not found")
        
        request.status = "generating_json"
        await self.db.commit()
        
        # Get relevant examples
        examples = await self.learning_service.get_relevant_examples(
            request.user_requirement,
            limit=5
        )
        
        examples_data = [
            {
                "title": ex.title,
                "workflow_json": ex.workflow_json
            }
            for ex in examples
        ]
        
        # Get LLM config
        llm_config = await self._get_active_llm_config()
        llm_service = LLMService(
            provider=llm_config.get("provider") if llm_config else None,
            config=llm_config
        )
        
        # Generate JSON
        workflow_json = await llm_service.generate_n8n_json(
            request.development_spec,
            examples_data
        )
        
        # Save generated JSON
        request.generated_json = workflow_json
        request.status = "testing"
        request.updated_at = datetime.utcnow()
        await self.db.commit()
        
        return workflow_json
    
    async def test_and_optimize(
        self,
        request_id: int
    ) -> Dict[str, Any]:
        """Test and optimize generated workflow"""
        
        # Get request
        stmt = select(WorkflowRequest).where(WorkflowRequest.id == request_id)
        result = await self.db.execute(stmt)
        request = result.scalar_one_or_none()
        
        if not request:
            raise ValueError("Request not found")
        
        # Get LLM config
        llm_config = await self._get_active_llm_config()
        llm_service = LLMService(
            provider=llm_config.get("provider") if llm_config else None,
            config=llm_config
        )
        
        # Test and optimize
        test_result = await llm_service.test_and_optimize_workflow(
            request.generated_json,
            request.development_spec
        )
        
        # Save results
        request.test_results = test_result
        
        # Use optimized JSON if available
        if test_result.get("optimized_json"):
            request.final_json = test_result["optimized_json"]
        else:
            request.final_json = request.generated_json
        
        request.status = "completed"
        request.updated_at = datetime.utcnow()
        await self.db.commit()
        
        return test_result
    
    async def get_workflow_request(
        self,
        request_id: int
    ) -> Optional[WorkflowResponse]:
        """Get workflow request by ID"""
        
        stmt = select(WorkflowRequest).where(WorkflowRequest.id == request_id)
        result = await self.db.execute(stmt)
        request = result.scalar_one_or_none()
        
        if request:
            return WorkflowResponse.model_validate(request)
        return None
    
    async def list_workflow_requests(
        self,
        skip: int = 0,
        limit: int = 20
    ) -> Dict[str, Any]:
        """List workflow requests"""
        
        # Get total count
        count_stmt = select(WorkflowRequest)
        count_result = await self.db.execute(count_stmt)
        total = len(count_result.scalars().all())
        
        # Get paginated results
        stmt = select(WorkflowRequest).order_by(
            desc(WorkflowRequest.created_at)
        ).offset(skip).limit(limit)
        
        result = await self.db.execute(stmt)
        requests = result.scalars().all()
        
        return {
            "total": total,
            "items": [WorkflowResponse.model_validate(req) for req in requests]
        }
