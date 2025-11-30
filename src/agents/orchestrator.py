import google.generativeai as genai
from src.utils.logger import setup_logger
from src.agents.scanner import ScannerAgent
from src.agents.analyst import AnalystAgent
from src.agents.qa import QAAgent
from src.state.project_state import ProjectState

logger = setup_logger("Orchestrator")

class OrchestratorAgent:
    def __init__(self, model_name: str = "gemini-2.0-flash"):
        """
        Initializes the Orchestrator Agent.
        """
        self.model_name = model_name
        self.model = genai.GenerativeModel(model_name)
        self.project_state = None
        logger.info(f"🤖 Orchestrator initialized with model: {model_name}")

    async def process_repository(self, repo_url: str) -> str:
        """
        Orchestrates the modernization process.
        """
        logger.info(f"Orchestrator processing repo: {repo_url}")
        
        # Initialize Project State
        self.project_state = ProjectState(repo_path=repo_url)
        
        # Initialize Sub-Agents
        scanner = ScannerAgent(self.model_name)
        analyst = AnalystAgent(self.model_name)
        qa = QAAgent(self.model_name)
        
        # --- Step 1: Discovery (Scanner Agent) ---
        logger.info("--- Step 1: Scanning Codebase ---")
        scan_results = await scanner.scan_repository(repo_url)
        self.project_state.update_scan_results(scan_results)
        logger.info(f"Scanner Results: {scan_results['summary']}")
        
        # --- Step 2: Analysis (Analyst Agent) ---
        logger.info("--- Step 2: Analyzing Logic ---")
        business_rules = await analyst.analyze_logic(scan_results)
        
        # Update state with extracted rules (simplified for now, ideally per file)
        # In a real scenario, Analyst would return a dict of {file: rules}
        # For now, we'll just log it, as the Analyst Agent doesn't return per-file rules in the current signature
        # We will improve this in the next iteration or let the Analyst update the state directly if passed
        
        # --- Step 3: Architecture (Orchestrator as Architect) ---
        logger.info("--- Step 3: Generating Modernization Plan ---")
        prompt = f"""
        You are the Lead Architect. 
        A scan of the repository '{repo_url}' has been completed.
        
        Scan Summary:
        {scan_results['summary']}
        
        Detected Languages:
        {scan_results['languages']}
        
        Extracted Business Rules:
        {business_rules}
        
        Please generate a preliminary modernization report outlining the next steps.
        """
        
        try:
            response = self.model.generate_content(prompt)
            initial_plan = response.text
        except Exception as e:
            import traceback
            logger.error(f"Failed to generate plan: {e}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            initial_plan = f"Error generating modernization plan: {str(e)}"
        
        # --- Step 4: Quality Assurance (QA Agent) ---
        logger.info("--- Step 4: QA Validation ---")
        qa_review = await qa.validate_plan(initial_plan, business_rules)
        
        final_report = f"{initial_plan}\n\n---\n\n# 🕵️ QA Review\n{qa_review}"
        
        # Update State
        self.project_state.set_modernization_plan(final_report)
        self.project_state.save_to_json()
        
        return final_report
