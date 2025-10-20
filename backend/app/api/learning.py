"""
Learning System API endpoints
"""
from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.models.database import get_db, LearnedExample, LearningLog
from app.services.learning_service import LearningService
from app.schemas.workflow import LearnedExampleResponse

router = APIRouter(prefix="/api/learning", tags=["learning"])


@router.post("/run")
async def run_learning_cycle(
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
):
    """Trigger learning cycle manually"""
    
    async def run_learning():
        service = LearningService(db)
        await service.run_learning_cycle()
    
    background_tasks.add_task(run_learning)
    
    return {"message": "Learning cycle started in background"}


@router.get("/examples", response_model=List[LearnedExampleResponse])
async def list_examples(
    skip: int = 0,
    limit: int = 50,
    source: str = None,
    db: AsyncSession = Depends(get_db)
):
    """List learned examples"""
    
    stmt = select(LearnedExample)
    
    if source:
        stmt = stmt.where(LearnedExample.source == source)
    
    stmt = stmt.order_by(
        LearnedExample.stars.desc(),
        LearnedExample.learned_at.desc()
    ).offset(skip).limit(limit)
    
    result = await db.execute(stmt)
    examples = result.scalars().all()
    
    return list(examples)


@router.get("/examples/{example_id}")
async def get_example(
    example_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get learned example with full workflow JSON"""
    
    stmt = select(LearnedExample).where(LearnedExample.id == example_id)
    result = await db.execute(stmt)
    example = result.scalar_one_or_none()
    
    if not example:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Example not found")
    
    return {
        "id": example.id,
        "title": example.title,
        "description": example.description,
        "source": example.source,
        "source_url": example.source_url,
        "workflow_json": example.workflow_json,
        "tags": example.tags,
        "nodes_used": example.nodes_used,
        "complexity_level": example.complexity_level,
        "stars": example.stars,
        "learned_at": example.learned_at
    }


@router.get("/logs")
async def get_learning_logs(
    skip: int = 0,
    limit: int = 20,
    db: AsyncSession = Depends(get_db)
):
    """Get learning logs"""
    
    stmt = select(LearningLog).order_by(
        LearningLog.started_at.desc()
    ).offset(skip).limit(limit)
    
    result = await db.execute(stmt)
    logs = result.scalars().all()
    
    return [
        {
            "id": log.id,
            "learning_type": log.learning_type,
            "examples_found": log.examples_found,
            "examples_added": log.examples_added,
            "status": log.status,
            "error_message": log.error_message,
            "started_at": log.started_at,
            "completed_at": log.completed_at
        }
        for log in logs
    ]


@router.get("/stats")
async def get_learning_stats(
    db: AsyncSession = Depends(get_db)
):
    """Get learning system statistics"""
    
    # Count examples by source
    stmt = select(LearnedExample)
    result = await db.execute(stmt)
    all_examples = result.scalars().all()
    
    stats = {
        "total_examples": len(all_examples),
        "by_source": {},
        "by_complexity": {},
        "top_nodes": {}
    }
    
    # Group by source
    for example in all_examples:
        source = example.source
        stats["by_source"][source] = stats["by_source"].get(source, 0) + 1
        
        complexity = example.complexity_level or "unknown"
        stats["by_complexity"][complexity] = stats["by_complexity"].get(complexity, 0) + 1
        
        # Count node usage
        if example.nodes_used:
            for node in example.nodes_used:
                stats["top_nodes"][node] = stats["top_nodes"].get(node, 0) + 1
    
    # Get top 20 nodes
    stats["top_nodes"] = dict(
        sorted(stats["top_nodes"].items(), key=lambda x: x[1], reverse=True)[:20]
    )
    
    return stats
