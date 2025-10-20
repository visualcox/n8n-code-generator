"""
Workflow API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.models.database import get_db
from app.services.workflow_service import WorkflowService
from app.schemas.workflow import (
    UserRequirement,
    Answer,
    WorkflowResponse,
    WorkflowListResponse
)

router = APIRouter(prefix="/api/workflow", tags=["workflow"])


@router.post("/create", response_model=WorkflowResponse)
async def create_workflow(
    requirement: UserRequirement,
    db: AsyncSession = Depends(get_db)
):
    """Create new workflow generation request"""
    service = WorkflowService(db)
    return await service.create_workflow_request(requirement)


@router.post("/{request_id}/analyze")
async def analyze_requirement(
    request_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Analyze requirement and generate clarifying questions"""
    service = WorkflowService(db)
    try:
        result = await service.analyze_requirement(request_id)
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/{request_id}/answers")
async def submit_answers(
    request_id: int,
    answers: List[Answer],
    db: AsyncSession = Depends(get_db)
):
    """Submit answers to clarifying questions"""
    service = WorkflowService(db)
    try:
        result = await service.submit_answers(request_id, answers)
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/{request_id}/generate-spec")
async def generate_spec(
    request_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Generate development specification"""
    service = WorkflowService(db)
    try:
        spec = await service.generate_development_spec(request_id)
        return {"development_spec": spec}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/{request_id}/update-spec")
async def update_spec(
    request_id: int,
    spec: dict,
    db: AsyncSession = Depends(get_db)
):
    """Update development specification after user review"""
    service = WorkflowService(db)
    try:
        result = await service.update_development_spec(
            request_id,
            spec.get("development_spec", "")
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/{request_id}/generate-json")
async def generate_json(
    request_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Generate n8n workflow JSON"""
    service = WorkflowService(db)
    try:
        workflow_json = await service.generate_workflow_json(request_id)
        return {"workflow_json": workflow_json}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/{request_id}/test-optimize")
async def test_optimize(
    request_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Test and optimize generated workflow"""
    service = WorkflowService(db)
    try:
        result = await service.test_and_optimize(request_id)
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/{request_id}", response_model=WorkflowResponse)
async def get_workflow(
    request_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get workflow request by ID"""
    service = WorkflowService(db)
    result = await service.get_workflow_request(request_id)
    if not result:
        raise HTTPException(status_code=404, detail="Workflow request not found")
    return result


@router.get("/", response_model=WorkflowListResponse)
async def list_workflows(
    skip: int = 0,
    limit: int = 20,
    db: AsyncSession = Depends(get_db)
):
    """List workflow requests"""
    service = WorkflowService(db)
    result = await service.list_workflow_requests(skip, limit)
    return result
