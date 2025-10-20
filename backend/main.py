"""
Main FastAPI application
"""
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.core.config import settings
from app.models.database import init_db
from app.api import workflow, llm_config, learning


# Scheduler for periodic learning
scheduler = AsyncIOScheduler()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    print("🚀 Starting n8n JSON Code Generator...")
    
    # Initialize database
    await init_db()
    print("✅ Database initialized")
    
    # Start scheduler for learning
    if settings.LEARNING_ENABLED:
        from app.services.learning_service import LearningService
        from app.models.database import AsyncSessionLocal
        
        async def scheduled_learning():
            async with AsyncSessionLocal() as db:
                service = LearningService(db)
                await service.run_learning_cycle()
                print("✅ Scheduled learning cycle completed")
        
        # Schedule weekly learning
        scheduler.add_job(
            scheduled_learning,
            'cron',
            day_of_week=0,  # Sunday
            hour=0,
            minute=0
        )
        scheduler.start()
        print("✅ Learning scheduler started (weekly on Sundays)")
    
    print(f"🌐 Server running on {settings.HOST}:{settings.PORT}")
    
    yield
    
    # Shutdown
    if scheduler.running:
        scheduler.shutdown()
    print("👋 Shutting down...")


# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(workflow.router)
app.include_router(llm_config.router)
app.include_router(learning.router)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )
