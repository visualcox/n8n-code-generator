"""
Learning Service for collecting and learning from n8n examples
"""
import asyncio
import json
from typing import List, Dict, Any
from datetime import datetime
import httpx
from bs4 import BeautifulSoup
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.database import LearnedExample, LearningLog
from app.core.config import settings


class LearningService:
    """Service for learning from n8n examples"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def run_learning_cycle(self) -> Dict[str, Any]:
        """Run complete learning cycle"""
        results = {
            "started_at": datetime.utcnow().isoformat(),
            "sources": {}
        }
        
        # Learn from official docs
        if settings.LEARNING_ENABLED:
            try:
                docs_result = await self.learn_from_official_docs()
                results["sources"]["official_docs"] = docs_result
            except Exception as e:
                results["sources"]["official_docs"] = {"error": str(e)}
            
            # Learn from templates
            try:
                templates_result = await self.learn_from_templates()
                results["sources"]["templates"] = templates_result
            except Exception as e:
                results["sources"]["templates"] = {"error": str(e)}
            
            # Learn from GitHub
            if settings.GITHUB_TOKEN:
                try:
                    github_result = await self.learn_from_github()
                    results["sources"]["github"] = github_result
                except Exception as e:
                    results["sources"]["github"] = {"error": str(e)}
        
        results["completed_at"] = datetime.utcnow().isoformat()
        return results
    
    async def learn_from_official_docs(self) -> Dict[str, Any]:
        """Learn from n8n official documentation"""
        log = LearningLog(
            learning_type="docs",
            status="running",
            started_at=datetime.utcnow()
        )
        self.db.add(log)
        await self.db.commit()
        
        examples_found = 0
        examples_added = 0
        
        try:
            # Crawl n8n docs for workflow examples
            async with httpx.AsyncClient(timeout=30.0) as client:
                # Example: Crawl workflow examples page
                urls_to_crawl = [
                    f"{settings.N8N_DOCS_URL}/workflows/",
                    f"{settings.N8N_DOCS_URL}/integrations/",
                ]
                
                for url in urls_to_crawl:
                    try:
                        response = await client.get(url)
                        if response.status_code == 200:
                            soup = BeautifulSoup(response.text, 'html.parser')
                            
                            # Extract workflow examples (this is a simplified example)
                            # In production, you'd parse the actual structure
                            code_blocks = soup.find_all('code', class_='language-json')
                            
                            for block in code_blocks:
                                try:
                                    workflow_json = block.get_text()
                                    # Validate it's a workflow JSON
                                    parsed = json.loads(workflow_json)
                                    if 'nodes' in parsed:
                                        examples_found += 1
                                        
                                        # Extract nodes used
                                        nodes_used = [node.get('type', '') for node in parsed.get('nodes', [])]
                                        
                                        # Check if already exists
                                        stmt = select(LearnedExample).where(
                                            LearnedExample.source == "official_docs",
                                            LearnedExample.workflow_json == workflow_json
                                        )
                                        result = await self.db.execute(stmt)
                                        existing = result.scalar_one_or_none()
                                        
                                        if not existing:
                                            example = LearnedExample(
                                                title=f"Official Docs Example {examples_found}",
                                                description="Extracted from n8n official documentation",
                                                source="official_docs",
                                                source_url=url,
                                                workflow_json=workflow_json,
                                                nodes_used=nodes_used,
                                                complexity_level=self._estimate_complexity(parsed),
                                                learned_at=datetime.utcnow()
                                            )
                                            self.db.add(example)
                                            examples_added += 1
                                except (json.JSONDecodeError, Exception):
                                    continue
                    except Exception:
                        continue
            
            await self.db.commit()
            
            log.status = "completed"
            log.examples_found = examples_found
            log.examples_added = examples_added
            log.completed_at = datetime.utcnow()
            await self.db.commit()
            
        except Exception as e:
            log.status = "failed"
            log.error_message = str(e)
            log.completed_at = datetime.utcnow()
            await self.db.commit()
            raise
        
        return {
            "examples_found": examples_found,
            "examples_added": examples_added
        }
    
    async def learn_from_templates(self) -> Dict[str, Any]:
        """Learn from n8n workflow templates"""
        log = LearningLog(
            learning_type="templates",
            status="running",
            started_at=datetime.utcnow()
        )
        self.db.add(log)
        await self.db.commit()
        
        examples_found = 0
        examples_added = 0
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                # Note: This is a simplified example
                # In production, you'd use n8n's API or scrape their templates page
                response = await client.get(settings.N8N_TEMPLATES_URL)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    # Extract template data (structure depends on actual website)
                    # This is a placeholder - you'd need to inspect the actual HTML structure
                    templates = soup.find_all('div', class_='template-card')
                    
                    for template in templates[:50]:  # Limit to 50 templates
                        try:
                            # Extract template information
                            title_elem = template.find('h3')
                            desc_elem = template.find('p', class_='description')
                            link_elem = template.find('a')
                            
                            if title_elem and link_elem:
                                title = title_elem.get_text(strip=True)
                                description = desc_elem.get_text(strip=True) if desc_elem else ""
                                template_url = link_elem.get('href', '')
                                
                                # Fetch template JSON (if available)
                                # This would require actual API access
                                examples_found += 1
                        except Exception:
                            continue
            
            await self.db.commit()
            
            log.status = "completed"
            log.examples_found = examples_found
            log.examples_added = examples_added
            log.completed_at = datetime.utcnow()
            await self.db.commit()
            
        except Exception as e:
            log.status = "failed"
            log.error_message = str(e)
            log.completed_at = datetime.utcnow()
            await self.db.commit()
            raise
        
        return {
            "examples_found": examples_found,
            "examples_added": examples_added
        }
    
    async def learn_from_github(self) -> Dict[str, Any]:
        """Learn from GitHub repositories"""
        log = LearningLog(
            learning_type="github",
            status="running",
            started_at=datetime.utcnow()
        )
        self.db.add(log)
        await self.db.commit()
        
        examples_found = 0
        examples_added = 0
        
        try:
            headers = {
                "Authorization": f"token {settings.GITHUB_TOKEN}",
                "Accept": "application/vnd.github.v3+json"
            }
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                # Search for n8n workflows on GitHub
                search_url = "https://api.github.com/search/repositories"
                params = {
                    "q": settings.GITHUB_SEARCH_QUERY,
                    "sort": "stars",
                    "order": "desc",
                    "per_page": 30
                }
                
                response = await client.get(search_url, headers=headers, params=params)
                
                if response.status_code == 200:
                    data = response.json()
                    repositories = data.get("items", [])
                    
                    for repo in repositories:
                        if repo.get("stargazers_count", 0) < settings.GITHUB_MIN_STARS:
                            continue
                        
                        # Search for JSON files in the repository
                        contents_url = repo.get("contents_url", "").replace("{+path}", "")
                        
                        try:
                            contents_response = await client.get(
                                contents_url,
                                headers=headers
                            )
                            
                            if contents_response.status_code == 200:
                                contents = contents_response.json()
                                
                                for item in contents:
                                    if item.get("name", "").endswith(".json"):
                                        # Download and parse the JSON file
                                        download_url = item.get("download_url")
                                        if download_url:
                                            file_response = await client.get(download_url)
                                            if file_response.status_code == 200:
                                                try:
                                                    workflow_json = file_response.text
                                                    parsed = json.loads(workflow_json)
                                                    
                                                    if 'nodes' in parsed:
                                                        examples_found += 1
                                                        
                                                        nodes_used = [
                                                            node.get('type', '')
                                                            for node in parsed.get('nodes', [])
                                                        ]
                                                        
                                                        # Check if exists
                                                        stmt = select(LearnedExample).where(
                                                            LearnedExample.source_url == download_url
                                                        )
                                                        result = await self.db.execute(stmt)
                                                        existing = result.scalar_one_or_none()
                                                        
                                                        if not existing:
                                                            example = LearnedExample(
                                                                title=repo.get("name", ""),
                                                                description=repo.get("description", ""),
                                                                source="github",
                                                                source_url=download_url,
                                                                workflow_json=workflow_json,
                                                                nodes_used=nodes_used,
                                                                complexity_level=self._estimate_complexity(parsed),
                                                                stars=repo.get("stargazers_count", 0),
                                                                learned_at=datetime.utcnow()
                                                            )
                                                            self.db.add(example)
                                                            examples_added += 1
                                                except (json.JSONDecodeError, Exception):
                                                    continue
                        except Exception:
                            continue
                        
                        # Rate limiting
                        await asyncio.sleep(1)
            
            await self.db.commit()
            
            log.status = "completed"
            log.examples_found = examples_found
            log.examples_added = examples_added
            log.completed_at = datetime.utcnow()
            await self.db.commit()
            
        except Exception as e:
            log.status = "failed"
            log.error_message = str(e)
            log.completed_at = datetime.utcnow()
            await self.db.commit()
            raise
        
        return {
            "examples_found": examples_found,
            "examples_added": examples_added
        }
    
    def _estimate_complexity(self, workflow_json: Dict[str, Any]) -> str:
        """Estimate workflow complexity based on JSON structure"""
        node_count = len(workflow_json.get('nodes', []))
        connection_count = len(workflow_json.get('connections', {}))
        
        if node_count <= 3 and connection_count <= 3:
            return "simple"
        elif node_count <= 10 and connection_count <= 15:
            return "medium"
        else:
            return "complex"
    
    async def get_relevant_examples(
        self,
        requirement: str,
        limit: int = 10
    ) -> List[LearnedExample]:
        """Get relevant learned examples based on requirement"""
        # Simple approach: return recent examples
        # In production, you'd use semantic search or embeddings
        stmt = select(LearnedExample).order_by(
            LearnedExample.stars.desc(),
            LearnedExample.learned_at.desc()
        ).limit(limit)
        
        result = await self.db.execute(stmt)
        examples = result.scalars().all()
        
        return list(examples)
