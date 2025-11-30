import google.generativeai as genai
from typing import List, Dict, Any
from src.utils.logger import setup_logger

logger = setup_logger("QAAgent")

class QAAgent:
    def __init__(self, model_name: str = "gemini-1.5-pro-latest"):
        self.model = genai.GenerativeModel(model_name)

    async def validate_plan(self, plan: str, business_rules: List[str]) -> str:
        """
        Validates the proposed modernization plan against the extracted business rules.
        """
        logger.info("🕵️ QA Agent reviewing the plan...")
        
        prompt = f"""
        You are the Quality Assurance (QA) Lead.
        
        Your goal is to validate the following Modernization Plan against the extracted Business Rules.
        
        Extracted Business Rules:
        {business_rules}
        
        Proposed Modernization Plan:
        {plan}
        
        Task:
        1. Verify that the plan addresses the business rules.
        2. Check for any hallucinations (claims about code that isn't in the rules).
        3. Rate the plan's quality (Pass/Fail).
        
        Output your review in Markdown format.
        """
        
        try:
            response = self.model.generate_content(prompt)
            review = response.text
            logger.info("✅ QA Review complete.")
            return review
        except Exception as e:
            logger.error(f"QA Validation failed: {e}")
            return "QA Validation Failed due to error."
