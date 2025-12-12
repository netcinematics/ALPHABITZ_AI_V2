
from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from google.adk.runners import InMemoryRunner
from google.adk.tools import google_search
from google.genai import types
import logging

# Configure Logging
logger = logging.getLogger(__name__)

retry_config = types.HttpRetryOptions(
    attempts=5,
    exp_base=7,
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504]
)

MODEL_NAME = "gemini-2.5-flash"

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
            """,
            tools=[google_search],
        )
        self.runner = InMemoryRunner(agent=self.agent)
        logger.info("✅ GATHERSTATE_AGENT initialized.")

    async def gather_misnomer_MECH(self, context: str = "") -> str:
        """
        Gathers Misnomer concepts.
        """
        logger.info("Running gather_misnomer_MECH...")
        prompt = f"""
        Search for significant MISNOMERS in current technology, science, or culture.
        Find concepts that are widely used but technically incorrect.
        Context: {context}
        Return a list of top 3 misnomers, ranked by impact.
        Format: 1. [Concept] - [Brief Reason]
        """
        response_events = await self.runner.run_debug(prompt)
        return str(response_events)

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
        response_events = await self.runner.run_debug(prompt)
        return str(response_events)

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
        response_events = await self.runner.run_debug(prompt)
        return str(response_events)

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
        response_events = await self.runner.run_debug(prompt)
        return str(response_events)

# Define instance for direct usage if needed, but class is modular.
# gather_agent_instance = GATHERSTATE_AGENT()
