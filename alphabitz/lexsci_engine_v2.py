import os
import json
import logging
import google.generativeai as genai
from typing import Dict, Any
from dotenv import load_dotenv

# --- CONFIGURATION ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s | AXI | %(message)s')
logger = logging.getLogger("LEXSCI")

# --- THE SYSTEM PROMPT ---
LEXSCI_SYSTEM_PROMPT = """
You are the LEXSCI ENGINE (Lexical Exactification Science).

### THE CONTEXT
Human language suffers from 'Semantic Drift', 'Cliche', and 'Actual Falseness'. 
This 'Fragile English' causes Hallucination in AI and Confusion in Humans.
Your Mission is to REVERSE this entropy.

### THE MECHANISM: EXACTIFICATION
You must take a target concept and perform 'Ontological Surgery'.
1. **Strip** the bias, emotion, and historical baggage.
2. **Identify** the underlying 'Mechanism of Action' (How it actually works).
3. **Re-encode** the concept using 'Atomic Bitz' (Indivisible units of meaning).

### OUTPUT SCHEMA (Strict JSON)
{
    "target_concept": "String",
    "status": "EXACTIFIED",
    "axi_analysis": {
        "common_misnomer": "Why the current word is false or weak.",
        "actual_reality": "The physical/logical truth of the phenomenon.",
        "semantic_drift_detected": "Boolean"
    },
    "derivation_trace": "Step-by-step logic: Misnomer -> Mechanism -> Truth.",
    "lexical_bitz": [
        { "bit_id": "UPPERCASE_ID", "function": "What this component does." }
    ],
    "ai_oil_syntax": "aPREFIX + ROOT + SUFFIX (The optimized token)",
    "confidence_score": 0.0-1.0
}
"""

class LexSciEngine:
    """
    The Engine of Truth. 
    Converts 'Fragile English' into 'Pristine Logic' (AI_OIL).
    Includes robust initialization and path management.
    """
    def __init__(self, vocab_path: str = "data/consensus.json", pending_path: str = "data/pending_review.json"):
        # 1. Load Environment Variables
        load_dotenv()
        
        # 2. Retrieve API Key
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.model_name = os.getenv("GEMINI_MODEL", "gemini-2.5-flash") # Default to flash if not set

        # 3. Configure Gemini
        if not self.api_key:
            logger.warning("⚠️  No GEMINI_API_KEY found in environment variables. Engine will run in MOCK MODE.")
            self.model = None
        else:
            try:
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel(
                    model_name=self.model_name,
                    system_instruction=LEXSCI_SYSTEM_PROMPT,
                    generation_config={"response_mime_type": "application/json"}
                )
                logger.info(f"✅ LEXSCI ENGINE ONLINE. Connected to {self.model_name}.")
            except Exception as e:
                logger.error(f"❌ Error configuring Gemini: {e}")
                self.model = None

        # 4. Set Paths
        self.vocab_path = vocab_path
        self.pending_path = pending_path
        self._ensure_files_exist()

    def _ensure_files_exist(self):
        """Ensures data directories and files exist."""
        for path in [self.vocab_path, self.pending_path]:
            directory = os.path.dirname(path)
            if directory and not os.path.exists(directory):
                os.makedirs(directory)
                logger.info(f"Created directory: {directory}")
            if not os.path.exists(path):
                with open(path, 'w') as f:
                    json.dump({}, f)
                logger.info(f"Created data file: {path}")

    def exactify(self, concept: str) -> Dict[str, Any]:
        """
        The Exactification Process.
        """
        logger.info(f"⚡ EXACTIFYING: '{concept}'")
        
        if not self.model: 
            return self._mock_response(concept)

        prompt = f"""
        TARGET: "{concept}"
        PROTOCOL: BEST_REFLECT_ACTUAL_REALITY
        ACTION: DERIVE_TRUTH_FROM_NOISE
        """

        try:
            response = self.model.generate_content(prompt)
            return json.loads(response.text)
        except Exception as e:
            logger.error(f"❌ COMPUTATION FAILED: {e}")
            return {"error": str(e)}

    def _mock_response(self, concept: str):
        return {
            "target_concept": concept,
            "status": "MOCK_DATA",
            "axi_analysis": { "actual_reality": "API Key Required for Truth." },
            "ai_oil_syntax": "aMOCK + DATA",
            "derivation_trace": "Mock trace."
        }