import json
import os
import datetime
import logging
import asyncio
from typing import Dict, List, Optional

# --- CRITICAL IMPORTS FOR AGENTZ ---
from google.adk.runners import InMemoryRunner
# from google.adk.tools import google_search
# from google.adk.agents import Agent
# from google.adk.models.google_llm import Gemini
# from google.genai import types



# --- CRITICAL IMPORTS FOR GEMINI ---
import google.generativeai as genai
from dotenv import load_dotenv

# Import Principles from the local package
from .prompts import LEXSCI_SYSTEM_PROMPT, get_MISNOMER_PROMPT
from .AGENTS.RESEARCH_AGENT import RESEARCH_AGENT
from .AGENTS.GATHERSTATE_AGENT_2 import GATHERSTATE_AGENT

# _________________________________________________________________ RETRY_CONFIG:
# retry_config=types.HttpRetryOptions(
#     attempts=5,  # Maximum retry attempts
#     exp_base=7,  # Delay multiplier
#     initial_delay=1, # Initial delay before first retry (in seconds)
#     http_status_codes=[429, 500, 503, 504] # Retry on these HTTP errors
# )
# print("✅ HttpRetry initialized.")


# _________________________________________________________________ APP CONSTANTS:
# APP_NAME = "ALPHA_BITZ_CAPSTONE"  # Application
# SESSION_ID = "MAIN_SESSION"  # Session
# USER_ID = "spaceOTTER" #"default"  # User
# MODEL_NAME = "gemini-2.5-flash"
# # MODEL_NAME = "gemini-2.5-flash-lite"
MAX_GATHER_ATTEMPTS = 3
# print("✅ Constants Initialized.")



# Setup Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - AXI - %(message)s')
logger = logging.getLogger(__name__)

class ALPHABITZ_AGENTZ:
    def __init__(self, vocab_path: str = "data/consensus.json", pending_path: str = "data/pending_review.json"):
        # 1. Load Environment Variables (looks for .env file)
        load_dotenv()
        
        # 2. Retrieve API Key
        self.api_key = os.getenv("GEMINI_API_KEY")
        
        # 3. Configure Gemini
        if not self.api_key:
            logger.warning("No GEMINI_API_KEY found in environment variables. Model will not function.")
            self.model = None
        else:
            try:
                genai.configure(api_key=self.api_key)
                # Initialize the specific model for Exactification
                self.model = genai.GenerativeModel(
                    'gemini-2.5-flash', 
                    system_instruction=LEXSCI_SYSTEM_PROMPT
                )
                logger.info("Gemini Model configured successfully.")
            except Exception as e:
                logger.error(f"Error configuring Gemini: {e}")
                self.model = None
        
        self.vocab_path = vocab_path
        self.pending_path = pending_path
        self._ensure_files_exist()

    def _ensure_files_exist(self):
        """Ensures the JSON storage files exist to prevent FileNotFoundError."""
        for path in [self.vocab_path, self.pending_path]:
            if not os.path.exists(path):
                os.makedirs(os.path.dirname(path), exist_ok=True)
                with open(path, 'w') as f:
                    json.dump({}, f)

# ___________________________________________________
# 
# ___________________________________________________
    def load_consensus_vocabulary(self) -> Dict:
        """Reads the human-approved vocabulary."""
        try:
            with open(self.vocab_path, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}

    def load_pending_vocabulary(self) -> Dict:
        """Reads the pending review vocabulary."""
        try:
            with open(self.pending_path, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}

    def _gather_MISNOMER_CONCEPTS_bak(self, existing_vocab: List[str]) -> str:
        """
        Phase 1: Gather MISNOMER CONCEPTS.
        Uses the AI and Google Search (implicitly) to find a concept needing exactification.
        """
        if not self.model:
            logger.error("Cannot gather MISNOMER CONCEPTS: Model not initialized.")
            return "LEXICAL_UNDEFINED"

        logger.info("Initiating Concept Gather...")
        
        MISNOMER_PROMPT = get_MISNOMER_PROMPT(existing_vocab)
        
        try:
            # We instantiate a fresh model connection for CONCEPT_GATHER.
            gather_MISNOMER_MODEL = genai.GenerativeModel('gemini-2.5-flash')
            
            # The MISNMOER_GATHER_AGENT uses the prompt to guide its search and selection
            response = gather_MISNOMER_MODEL.generate_content(MISNOMER_PROMPT)
            target = response.text.strip().replace('"', '').replace("'", "")
            #target = "Dark Matter"
            
            logger.info(f"Target Acquired: {target}")
            return target
        except Exception as e:
            logger.error(f"Concept Gather failed: {e}")
            return "LEXICAL_UNDEFINED"

    def _exactify_process(self, concept: str) -> Dict:
        """
        Phase 2: The Exactification Loop.
        Applies principles to the target concept, generating the structured JSON.
        """
        if not self.model:
            return {"error": "Model not initialized"}

        logger.info(f"Running Exactification Protocols on: {concept}")
        
        prompt = f"TARGET CONCEPT: {concept}. Perform LEXSCI Exactification now."
        
        try:
            response = self.model.generate_content(prompt)
            # response = "```json{}```"
            
            # Clean generic markdown fences if present (```json ... ```)
            clean_text = response.text.replace("```json", "").replace("```", "").strip()
            data = json.loads(clean_text)
            
            # Add metadata
            data['timestamp'] = datetime.datetime.now().isoformat()
            data['version'] = "LEXSCI_v1"
            return data
        except Exception as e:
            logger.error(f"Exactification failed: {e}")
            return {"error": str(e), "concept": concept}

    def _transcode_audio_inputs(self):
        """
        Phase 0: Ingest.
        Placeholder for future audio transcode implementation (Speech-to-Text).
        """
        logger.info("Scanning audio inputs (Placeholder)... No new audio streams.")

    def _save_to_pending(self, concept: str, data: Dict):
        """Appends the result to the pending review file."""
        try:
            with open(self.pending_path, 'r+') as f:
                try:
                    pending = json.load(f)
                except json.JSONDecodeError:
                    pending = {}
                
                pending[concept] = data
                
                f.seek(0)
                json.dump(pending, f, indent=4)
                f.truncate()
        except FileNotFoundError:
            # Create if it somehow disappeared
            with open(self.pending_path, 'w') as f:
                json.dump({concept: data}, f, indent=4)
                
        logger.info(f"Concept '{concept}' saved to Pending Review.")

    def test_connection(self):
        """
        Verifies the library is imported and the API key is recognized.
        """
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] LEXSCI SYSTEM CHECK...")
        print(f"[{timestamp}] CORE LIBRARY IMPORTED SUCCESSFULLY.")
        
        if self.model:
             print(f"[{timestamp}] GEMINI API: CONNECTED")
        else:
             print(f"[{timestamp}] GEMINI API: DISCONNECTED (Check .env for key)")
             
        print(f"[{timestamp}] READY FOR MISSION.")

# ___________________________________________________
# 
# ___________________________________________________

    def run_ALPHABITZ_original_process(self):
        """
        The Main Cycle: Ingest -> Gather -> Exactify -> Save.
        """
        logger.info("=== STARTING DAILY ALPHABITZ MISSION ===")
        
        # 1. Ingest Audio / Update Inputs
        self._transcode_audio_inputs()
        
        # 2. Load Human Truth (Consensus)
        vocab = self.load_consensus_vocabulary()
        existing_keys = list(vocab.keys())
        
        # 3. Gather
        target_concept = self._gather_MISNOMER_CONCEPTS_bak(existing_keys)
        
        if target_concept == "LEXICAL_UNDEFINED":
            logger.warning("Mission Aborted: No target found.")
            return

        # 4. Exactify
        result = self._exactify_process(target_concept)
        # TODO if error do no save to pending.
        
        # 5. Save to Pending (Human Loop)
        self._save_to_pending(target_concept, result)
        
        logger.info("=== MISSION COMPLETE. AWAITING HUMAN ARBITRATION ===")


# ___________________________________________________
# 
# ___________________________________________________

    async def run_ALPHABITZ_research_agent(self):
        """
        The Main Cycle: Ingest -> Gather -> Exactify -> Save.
        """
        logger.info("=== Load ALPHABITZ AGENTZ ===")
        
        # MISNOMER_PROMPT = get_MISNOMER_PROMPT(existing_vocab)
        
        # try:
        #     # We instantiate a fresh model connection for CONCEPT_GATHER.
        #     gather_MISNOMER_MODEL = genai.GenerativeModel('gemini-2.5-flash')
            
        #     # The MISNMOER_GATHER_AGENT uses the prompt to guide its search and selection
        #     response = gather_MISNOMER_MODEL.generate_content(MISNOMER_PROMPT)
        #     target = response.text.strip().replace('"', '').replace("'", "")
        #     #target = "Dark Matter"
            
        #     logger.info(f"Target Acquired: {target}")
        #     return target
        # except Exception as e:
        #     logger.error(f"Concept Gather failed: {e}")
        #     return "LEXICAL_UNDEFINED"


        # RESEARCH_AGENT = Agent(
        #     name="CONCISE_ASSISTANT",
        #     model=Gemini(
        #         model=MODEL_NAME,
        #         retry_options=retry_config
        #     ),
        #     description="A concise agent that answers questions with brief answers.",
        #     instruction="""You are a concise assistant. Answer briefly, with a single short sentence to explain.
        #     Use Google Search tool for current answers. Do not be sycophantic.
        #     """,
        #     tools=[google_search],
        # )

        # print("✅ RESEARCH_AGENT defined.")

        research_runner = InMemoryRunner(agent=RESEARCH_AGENT)

        print("ANSWER: Has AI created a more sophisticated human language yet?")

        # RESEARCH QUESTION 1): Has AI created a new human language yet?
        response1 = await research_runner.run_debug([
            """Yes or no, has artificial intelligence,
            ever created a NEW LANGUAGE of ENHANCED_SYNTAX,
            that was adopted by humanity - to train AI with exactness?""",
            # " What is the latest news about AI introducing a new human language?"
        ])
        # print(f"RESPONSE: {response1}")
        
        
        logger.info("=== AGENTZ LOADED ===")

    async def run_ALPHABITZ_gatherstate_agent(self):
        """
        Advanced Cycle: Uses GATHERSTATE_AGENT to find Misnomers/Cliches/etc.
        """
        logger.info("=== STARTING ALPHABITZ 3 (GATHERSTATE) ===")
        
        # Initialize the GATHERSTATE AGENT
        gather_agent = GATHERSTATE_AGENT()
        
        # 1. Gather Misnomers
        logger.info("Gathering Misnomers...")
        
        # Load both consensus and pending vocabularies
        consensus_vocab = self.load_consensus_vocabulary()
        pending_vocab = self.load_pending_vocabulary()
        
        # Combine keys from both to create the exclusion list
        existing_keys = list(consensus_vocab.keys()) + list(pending_vocab.keys())
        
        misnomers = "LEXICAL_UNDEFINED"
        
            # Retry Loop
        for attempt in range(MAX_GATHER_ATTEMPTS):
            logger.info(f"Gather Attempt {attempt + 1}/{MAX_GATHER_ATTEMPTS}...")
            
            # Gather candidate
            candidate = await gather_agent.gather_misnomer_MECH(existing_keys)
            
            # Check for API Limit Error
            if candidate == "API_LIMIT_REACHED":
                logger.error("Gather Loop Aborted due to API Rate Limit.")
                return

            # Simple normalization for check: strip whitespace and quotes
            # The agent might return "Concept" or 'Concept'
            candidate_clean = candidate.strip().strip("'").strip('"')
            
            # Check for duplication (case-insensitive check against existing keys)
            is_duplicate = any(k.lower() == candidate_clean.lower() for k in existing_keys)
            
            if is_duplicate:
                logger.warning(f"Duplicate Target Found: '{candidate_clean}'. Retrying...")
                # Add it to existing_keys temporarily so next prompt excludes it explicitly if passed again
                existing_keys.append(candidate_clean)
                await asyncio.sleep(2) # Pace the retries
                continue
            else:
                logger.info(f"Unique Target Acquired: '{candidate_clean}'")
                misnomers = candidate_clean
                break

        
        if misnomers == "LEXICAL_UNDEFINED":
            logger.warning("Mission Aborted: Could not find unique target after max attempts.")
            return

        # 4. Exactify
        result = self._exactify_process(misnomers)
        # TODO if error do no save to pending.
        
        # 5. Save to Pending (Human Loop)
        self._save_to_pending(misnomers, result)


        # misnomers = await gather_agent.gather_misnomer_MECH()
        # print(f"MISNOMERS FOUND:\n{misnomers}")
        
        # 2. Gather Cliches (Example of extending coverage)
        # logger.info("Gathering Cliches...")
        # cliches = await gather_agent.gather_cliche_MECH()
        # print(f"CLICHES FOUND:\n{cliches}")

        # Note: In a full implementation, we would parse these text responses 
        # and feed them into the exactification process (Phase 2).
        # For now, we just gather and log as requested for the prototype.
        
        logger.info("=== ALPHABITZ 3 COMPLETE ===")

