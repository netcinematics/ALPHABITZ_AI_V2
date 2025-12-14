import os
import json
import logging
import google.generativeai as genai
from typing import Dict, Any

# --- CONFIGURATION ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s | AXI | %(message)s')
logger = logging.getLogger("LEXSCI")

API_KEY = os.getenv("GEMINI_API_KEY") 
MODEL_NAME = "gemini-2.5-flash"

# --- THE SYSTEM PROMPT: THE PHILOSOPHY IN CODE ---
# We do not hide the AXI. We encode it as the LAW of the System.
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
    """
    def __init__(self, api_key: str = API_KEY):
        if not api_key:
            logger.warning("⚠️  Running in MOCK MODE (No API Key).")
            self.model = None
        else:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel(
                model_name=MODEL_NAME,
                system_instruction=LEXSCI_SYSTEM_PROMPT,
                generation_config={"response_mime_type": "application/json"}
            )
            logger.info("✅ LEXSCI ENGINE ONLINE. Connected to Gemini.")

    def exactify(self, concept: str) -> Dict[str, Any]:
        """
        The Exactification Process.
        It does not 'fix' the word; it 'resolves' the reality.
        """
        logger.info(f"⚡ EXACTIFYING: '{concept}'")
        
        if not self.model: 
            return self._mock_response(concept)

        # The Prompt is no longer polite. It is a Command.
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
            "axi_analysis": { "actual_reality": "API Key Required for Truth." }
        }

# --- DEMONSTRATION OF WISDOM ---
if __name__ == "__main__":
    engine = LexSciEngine()
    
    # We choose concepts that MATTER.
    targets = [
        "Artificial Intelligence",  # The Misnomer of the Century
        "Hallucination",            # The Excuse for Probability
        "Prompt Engineering"        # The Illusion of Control
    ]

    print("\n" + "="*60)
    print("   LEXSCI: THE RESOLUTION OF PERPETUAL CONFUSION")
    print("="*60 + "\n")

    for t in targets:
        result = engine.exactify(t)
        
        if "error" not in result:
            print(f"🔹 TARGET:   {t}")
            print(f"   REALITY:  {result['axi_analysis']['actual_reality']}")
            print(f"   SYNTAX:   {result.get('ai_oil_syntax')}")
            print(f"   TRACE:    {result.get('derivation_trace')}")
            print("-" * 60)