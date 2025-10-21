"""
LLM Service for interacting with various LLM providers
"""
from typing import Optional, Dict, Any, List
import json
import httpx
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_community.chat_models import ChatOllama
from app.core.config import settings


class LLMService:
    """Service for LLM interactions"""
    
    def __init__(self, provider: str = None, config: Dict[str, Any] = None):
        """Initialize LLM service"""
        self.provider = provider or settings.DEFAULT_LLM_PROVIDER
        self.config = config or {}
        self.client = self._initialize_client()
    
    def _initialize_client(self):
        """Initialize LLM client based on provider"""
        if self.provider == "openai":
            return ChatOpenAI(
                api_key=self.config.get("api_key", settings.OPENAI_API_KEY),
                model=self.config.get("model_name", "gpt-4-turbo-preview"),
                temperature=self.config.get("temperature", 0.7) / 100,
                max_tokens=self.config.get("max_tokens", 4000)
            )
        elif self.provider == "gemini":
            from langchain_google_genai import ChatGoogleGenerativeAI
            return ChatGoogleGenerativeAI(
                google_api_key=self.config.get("api_key", settings.GEMINI_API_KEY),
                model=self.config.get("model_name", "gemini-1.5-pro"),
                temperature=self.config.get("temperature", 0.7) / 100,
                max_output_tokens=self.config.get("max_tokens", 4000)
            )
        elif self.provider == "anthropic":
            from langchain_community.chat_models import ChatAnthropic
            return ChatAnthropic(
                api_key=self.config.get("api_key", settings.ANTHROPIC_API_KEY),
                model=self.config.get("model_name", "claude-3-opus-20240229"),
                temperature=self.config.get("temperature", 0.7) / 100,
                max_tokens=self.config.get("max_tokens", 4000)
            )
        elif self.provider == "ollama":
            return ChatOllama(
                base_url=self.config.get("api_url", settings.OLLAMA_BASE_URL),
                model=self.config.get("model_name", settings.OLLAMA_MODEL),
                temperature=self.config.get("temperature", 0.7) / 100
            )
        else:
            raise ValueError(f"Unsupported LLM provider: {self.provider}")
    
    async def analyze_requirement(self, requirement: str, context: Optional[str] = None) -> Dict[str, Any]:
        """Analyze user requirement and generate questions"""
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert n8n workflow analyst. Your task is to analyze user requirements 
            and identify what information is needed to create a perfect n8n workflow.
            
            IMPORTANT: Do NOT make assumptions. If information is unclear or missing, you MUST ask questions.
            
            Analyze the requirement and return a JSON response with:
            1. summary: Brief summary of what the user wants
            2. identified_components: List of components you identified
            3. missing_information: List of information that is missing or unclear
            4. questions: Array of questions to ask the user (each with id, question, question_type, options if applicable, required)
            5. estimated_complexity: "simple", "medium", or "complex"
            
            Question types: "text", "choice", "multiple_choice"
            """),
            ("user", "Requirement: {requirement}\n\nContext: {context}")
        ])
        
        chain = prompt | self.client
        response = await chain.ainvoke({
            "requirement": requirement,
            "context": context or "None provided"
        })
        
        # Parse response
        try:
            result = json.loads(response.content)
            return result
        except json.JSONDecodeError:
            # If LLM doesn't return valid JSON, extract information
            return {
                "summary": response.content[:200],
                "identified_components": [],
                "missing_information": [],
                "questions": [],
                "estimated_complexity": "medium"
            }
    
    async def generate_development_spec(
        self,
        requirement: str,
        answers: List[Dict[str, str]],
        learned_examples: List[Dict[str, Any]]
    ) -> str:
        """Generate detailed development specification"""
        
        # Prepare examples context
        examples_context = "\n\n".join([
            f"Example {i+1}: {ex.get('title', 'Untitled')}\n"
            f"Description: {ex.get('description', 'N/A')}\n"
            f"Nodes: {', '.join(ex.get('nodes_used', []))}\n"
            f"Complexity: {ex.get('complexity_level', 'N/A')}"
            for i, ex in enumerate(learned_examples[:5])
        ])
        
        # Prepare answers context
        answers_context = "\n".join([
            f"Q{i+1}: {ans['question']}\nA{i+1}: {ans['answer']}"
            for i, ans in enumerate(answers)
        ])
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert n8n workflow architect. Create a comprehensive development specification 
            document for building an n8n workflow based on user requirements and answers.
            
            The specification should include:
            1. Title: Clear title for the workflow
            2. Objective: What the workflow aims to achieve
            3. User Requirements: Detailed breakdown of requirements
            4. Workflow Steps: Step-by-step execution flow
            5. Required Nodes: List of n8n nodes needed
            6. Node Configurations: Configuration for each node
            7. Data Flow: How data moves between nodes
            8. Error Handling: Error handling strategies
            9. Testing Criteria: How to test the workflow
            10. Estimated Cost: If using paid APIs or services
            
            Use the learned examples as reference for best practices.
            Be specific and detailed. Focus on efficiency and cost-effectiveness.
            """),
            ("user", """Original Requirement: {requirement}
            
User Answers:
{answers}

Relevant Examples:
{examples}

Generate a comprehensive development specification document.""")
        ])
        
        chain = prompt | self.client
        response = await chain.ainvoke({
            "requirement": requirement,
            "answers": answers_context,
            "examples": examples_context
        })
        
        return response.content
    
    async def generate_n8n_json(
        self,
        development_spec: str,
        learned_examples: List[Dict[str, Any]]
    ) -> str:
        """Generate n8n workflow JSON based on development spec"""
        
        # Prepare example JSONs
        examples_json = "\n\n".join([
            f"Example {i+1} ({ex.get('title', 'Untitled')}):\n{ex.get('workflow_json', '{}')[:500]}..."
            for i, ex in enumerate(learned_examples[:3])
        ])
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert n8n workflow developer. Generate a complete, valid n8n workflow JSON 
            based on the development specification.
            
            IMPORTANT:
            1. The JSON must be valid n8n format
            2. Include all necessary nodes and connections
            3. Configure each node properly
            4. Use appropriate node types from n8n's latest nodes
            5. Ensure proper error handling
            6. Optimize for performance and cost
            7. Follow n8n best practices
            
            Return ONLY the JSON workflow, no explanations."""),
            ("user", """Development Specification:
{spec}

Reference Examples (for structure):
{examples}

Generate the complete n8n workflow JSON:""")
        ])
        
        chain = prompt | self.client
        response = await chain.ainvoke({
            "spec": development_spec,
            "examples": examples_json
        })
        
        return response.content
    
    async def test_and_optimize_workflow(
        self,
        workflow_json: str,
        development_spec: str
    ) -> Dict[str, Any]:
        """Test and optimize the generated workflow"""
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert n8n workflow reviewer. Analyze the generated workflow JSON and:
            
            1. Check for errors or invalid configurations
            2. Verify it meets the development specification
            3. Identify optimization opportunities
            4. Suggest improvements for efficiency and cost
            5. Check for security concerns
            6. Validate error handling
            
            Return a JSON response with:
            - passed: boolean (true if workflow is valid and meets spec)
            - issues: array of issues found
            - suggestions: array of improvement suggestions
            - optimization_opportunities: array of optimization ideas
            - optimized_json: improved version of the workflow JSON (if changes needed)
            """),
            ("user", """Development Specification:
{spec}

Generated Workflow JSON:
{workflow}

Analyze and optimize:""")
        ])
        
        chain = prompt | self.client
        response = await chain.ainvoke({
            "spec": development_spec,
            "workflow": workflow_json
        })
        
        try:
            result = json.loads(response.content)
            return result
        except json.JSONDecodeError:
            return {
                "passed": True,
                "issues": [],
                "suggestions": [],
                "optimization_opportunities": [],
                "optimized_json": workflow_json
            }
