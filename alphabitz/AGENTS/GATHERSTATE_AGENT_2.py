
from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from google.adk.runners import InMemoryRunner
from google.adk.tools import google_search
from google.genai import types
from google.api_core.exceptions import ResourceExhausted
import logging
from typing import Dict, List, Optional

# Configure Logging
logger = logging.getLogger(__name__)

retry_config = types.HttpRetryOptions(
    attempts=3,
    exp_base=7,
    initial_delay=3,
    http_status_codes=[429, 500, 503, 504]
)

# MODEL_NAME = "gemini-2.0-flash-exp"
MODEL_NAME = "gemini-2.5-flash"
# MODEL_NAME = "gemini-1.5-flash-pro"

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
            Return the highest ranked topics first.
            IMPORTANT: Do NOT return any concepts listed in the exclusion list provided in the prompt.
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

    async def gather_misnomer_MECH(self, context: str = "", existing_vocab_keys: List[str] = []) -> str:
        """
        Gathers Misnomer concepts.
        """
        logger.info("Running gather_misnomer_MECH...")
        prompt = f"""
        Find a concept that is misunderstood by the general public but has a specific 
        technical reality. Focus on AI, Neuroscience, Psychology, Sociology, or Quantum Mechanics.
        
        EXCLUSION LIST (DO NOT RETURN THESE): {existing_vocab_keys}
        
        Return ONLY the concept name of a high-impact misnomer that is NOT in the exclusion list.
        """
        # Search for significant MISNOMERS in current technology, science, or culture.
        # Find concepts that are widely used but technically incorrect.
        # Context: {context}
        # Return a list of top 3 misnomers, ranked by impact.
        # Format: 1. [Concept] - [Brief Reason]
        try:
            response_events = await self.runner.run_debug(prompt)
            # return str(response_events)
            response_tgt = self._extract_text_from_events(response_events)
            logger.info(f"Gathered misnomers: {response_tgt}")
            return str(response_tgt)
        except ResourceExhausted:
            logger.error("API Quota Reached (429). Halting GATHERSTATE_AGENT.")
            return "API_LIMIT_REACHED"

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
