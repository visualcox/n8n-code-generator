"""
LLM Configuration API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from typing import List

from app.models.database import get_db, LLMConfig
from app.schemas.workflow import LLMConfigCreate, LLMConfigResponse

router = APIRouter(prefix="/api/llm", tags=["llm"])


@router.post("/config", response_model=LLMConfigResponse)
async def create_llm_config(
    config: LLMConfigCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create new LLM configuration"""
    
    # If set as default, unset other defaults
    if config.is_default:
        stmt = update(LLMConfig).values(is_default=False)
        await db.execute(stmt)
    
    llm_config = LLMConfig(
        name=config.name,
        provider=config.provider,
        api_key=config.api_key,
        api_url=config.api_url,
        model_name=config.model_name,
        temperature=config.temperature,
        max_tokens=config.max_tokens,
        is_default=config.is_default,
        is_active=config.is_default  # Auto-activate if default
    )
    
    db.add(llm_config)
    await db.commit()
    await db.refresh(llm_config)
    
    return llm_config


@router.get("/config", response_model=List[LLMConfigResponse])
async def list_llm_configs(
    db: AsyncSession = Depends(get_db)
):
    """List all LLM configurations"""
    stmt = select(LLMConfig)
    result = await db.execute(stmt)
    configs = result.scalars().all()
    return list(configs)


@router.get("/config/{config_id}", response_model=LLMConfigResponse)
async def get_llm_config(
    config_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get LLM configuration by ID"""
    stmt = select(LLMConfig).where(LLMConfig.id == config_id)
    result = await db.execute(stmt)
    config = result.scalar_one_or_none()
    
    if not config:
        raise HTTPException(status_code=404, detail="Configuration not found")
    
    return config


@router.put("/config/{config_id}/activate")
async def activate_llm_config(
    config_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Activate LLM configuration"""
    
    # Deactivate all configs
    stmt = update(LLMConfig).values(is_active=False)
    await db.execute(stmt)
    
    # Activate selected config
    stmt = select(LLMConfig).where(LLMConfig.id == config_id)
    result = await db.execute(stmt)
    config = result.scalar_one_or_none()
    
    if not config:
        raise HTTPException(status_code=404, detail="Configuration not found")
    
    config.is_active = True
    await db.commit()
    
    return {"message": f"Configuration '{config.name}' activated"}


@router.delete("/config/{config_id}")
async def delete_llm_config(
    config_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Delete LLM configuration"""
    stmt = select(LLMConfig).where(LLMConfig.id == config_id)
    result = await db.execute(stmt)
    config = result.scalar_one_or_none()
    
    if not config:
        raise HTTPException(status_code=404, detail="Configuration not found")
    
    await db.delete(config)
    await db.commit()
    
    return {"message": "Configuration deleted"}
