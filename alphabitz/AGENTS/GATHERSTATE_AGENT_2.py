
from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from google.adk.runners import InMemoryRunner
from google.adk.tools import google_search
from google.genai import types
from google.api_core.exceptions import ResourceExhausted
import logging
import random
import ast
import re
from typing import Dict, List, Optional

# Configure Logging
logger = logging.getLogger(__name__)

retry_config = types.HttpRetryOptions(
    attempts=3,
    exp_base=7,
    initial_delay=3,
    http_status_codes=[429, 500, 503, 504]
)

# MODEL_NAME = "gemini-2.5-flash"
MODEL_NAME = "gemini-2.5-flash-lite"
# MODEL_NAME = "gemini-1.5-flash"
# MODEL_NAME = "gemini-1.5-flash-pro"
# MODEL_NAME = "gemini-2.0-flash-exp"

class GATHERSTATE_AGENT:
    """
    GATHERSTATE_AGENT specializes at searching GEMINI for various forms of 
    MISNOMER, CLICHE, POLYSEMY, HOMONYMY and returning the highest ranked topics first.
    """
    def __init__(self):
        self.agent = Agent(
            name="GATHERSTATE_AGENT",
            model=Gemini(
                model=MODEL_NAME,
                retry_options=retry_config
            ),
            description="An advanced agent for gathering and analyzing linguistic states.",
            instruction="""You are the GATHERSTATE agent.
            Your mission is to search for and identify linguistic concepts such as 
            MISNOMER, CLICHE, POLYSEMY, and HOMONYMY.
            Prioritize inputs that are confusing, widely misused, or scientifically inaccurate.
            
            CRITICAL RULE: You MUST check the provided Exclusion List. 
            NEVER return a concept that is already in the Exclusion List.
            Return COMMON, everyday misnomers. Do not prioritize the "highest ranked" or most famous scientific ones if they are excluded.
            Diversity and variety are key.
            """,
            tools=[google_search],
        )
        self.runner = InMemoryRunner(agent=self.agent)
        logger.info("✅ GATHERSTATE_AGENT initialized.")

    def _extract_text_from_events(self, events: List) -> str:
        """Helper to extract text from the last model event."""
        for event in reversed(events):
            if hasattr(event, 'content') and hasattr(event.content, 'role') and event.content.role == 'model':
                if hasattr(event.content, 'parts') and len(event.content.parts) > 0:
                     return event.content.parts[0].text.strip()
        return str(events)

    async def gather_misnomer_MECH(self, context: str = "", existing_vocab_keys: List[str] = []) -> List[str]:
        """
        Gathers Misnomer concepts.
        """
        logger.info("Running gather_misnomer_MECH...")
        # Prepare the prompt string
        prompt = f"""
        Find 5 DISTINCT, COMMON misnomers from different fields (Science, History, Technology, Psychology).
        Do NOT focus only on AI.
        
        FORBIDDEN CONCEPTS (ALREADY FOUND): 
        {", ".join(existing_vocab_keys)}
        
        INSTRUCTION: Return a Python list of strings containing 5 new, unique misnomers.
        Strictly output the list ONLY. No "Here are..." preamble. No Markdown bullets.
        Example format: ["Cloud Computing", "Survival of the Fittest", "Dark Ages"]
        """
        try:
            response_events = await self.runner.run_debug(prompt)
            response_text = self._extract_text_from_events(response_events)
            
            candidates = []
            
            # Attempt 1: Parse as Python list
            try:
                # Clean code blocks and preambles
                clean_text = response_text.replace("```python", "").replace("```json", "").replace("```", "").strip()
                # Try to find the list bracket start/end
                if '[' in clean_text and ']' in clean_text:
                    start = clean_text.find('[')
                    end = clean_text.rfind(']') + 1
                    clean_text = clean_text[start:end]
                
                candidates = ast.literal_eval(clean_text)
            except:
                logger.warning("Could not parse list with ast.literal_eval. Trying regex fallback.")
                
                # Attempt 2: Regex for bullets or numbered lists
                # Matches: * Item  OR  1. Item  OR  - Item
                matches = re.findall(r'(?:^\s*[\*\-\+]|\d+\.)\s+(.+)$', response_text, re.MULTILINE)
                if matches:
                     # Clean up bolding like **Science:** The Big Bang -> The Big Bang
                     candidates = [re.sub(r'\*\*.*?\*\*[:\-]?\s*', '', m).strip() for m in matches]

            if isinstance(candidates, list) and candidates:
                 # Filter duplicates
                 unique_candidates = [c for c in candidates if c not in existing_vocab_keys]
                 if unique_candidates:
                     logger.info(f"Gathered {len(unique_candidates)} unique candidates: {unique_candidates}")
                     return unique_candidates
                 else:
                     logger.warning("All returned candidates were duplicates.")
                     return []
            
            # Fallback
            logger.warning("Parsing failed completely. Returning empty list.")
            return [] 
        except ResourceExhausted:
            logger.error("API Quota Reached (429). Halting GATHERSTATE_AGENT.")
            return []

    async def gather_cliche_MECH(self, context: str = "") -> str:
        """
        Gathers Cliche concepts.
        """
        logger.info("Running gather_cliche_MECH...")
        prompt = f"""
        Search for overused CLICHES in business, AI, or modern writing.
        Context: {context}
        Return a list of top 3 cliches that dilute meaning.
        Format: 1. [Cliche] - [Brief Reason]
        """
        try:
            response_events = await self.runner.run_debug(prompt)
            response_tgt = self._extract_text_from_events(response_events)
            logger.info(f"Gathered cliches: {response_tgt}")
            return str(response_tgt)
        except ResourceExhausted:
            logger.error("API Quota Reached (429). Halting GATHERSTATE_AGENT.")
            return "API_LIMIT_REACHED"

    async def gather_polysemy_MECH(self, context: str = "") -> str:
        """
        Gathers Polysemy examples (words with multiple meanings causing confusion).
        """
        logger.info("Running gather_polysemy_MECH...")
        prompt = f"""
        Find words with high POLYSEMY (multiple meanings) that cause confusion in technical or AI contexts.
        Context: {context}
        Return the top 3 examples.
        Format: 1. [Word] - [Meaning A] vs [Meaning B]
        """
        try:
            response_events = await self.runner.run_debug(prompt)
            # return self._extract_text_from_events(response_events)
            response_tgt = self._extract_text_from_events(response_events)
            logger.info(f"Gathered polysemy: {response_tgt}")
            return str(response_tgt)
        except ResourceExhausted:
            logger.error("API Quota Reached (429). Halting GATHERSTATE_AGENT.")
            return "API_LIMIT_REACHED"

    async def gather_homonymy_MECH(self, context: str = "") -> str:
        """
        Gathers Homonymy examples.
        """
        logger.info("Running gather_homonymy_MECH...")
        prompt = f"""
        Find HOMONYMS that are problematic in automated text processing or understanding.
        Context: {context}
        Return the top 3 examples.
        """
        try:
            response_events = await self.runner.run_debug(prompt)
            response_tgt = self._extract_text_from_events(response_events)
            logger.info(f"Gathered homonymy: {response_tgt}")
            return str(response_tgt)
        except ResourceExhausted:
            logger.error("API Quota Reached (429). Halting GATHERSTATE_AGENT.")
            return "API_LIMIT_REACHED"

# Define instance for direct usage if needed, but class is modular.
# gather_agent_instance = GATHERSTATE_AGENT()
