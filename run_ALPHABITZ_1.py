# import sys
import asyncio
from alphabitz.engine import ALPHABITZ_AGENTZ

def main():
    """
    Entry point for ALPHABITZ.
    Can be triggered by a cron job (Linux) or Task Scheduler (Windows).
    """
    print("Initializing ALPHABITZ Protocol...")
    
    # Initialize the Mechanism
    # Default paths are relative to execution, can be absolute in production
    mech = ALPHABITZ_AGENTZ(
        vocab_path="data/consensus_vocabulary.json",
        pending_path="data/pending_review.json"
    )
    
    # Run the Cycle
    # mech.run_ALPHABITZ_original_process()
    # asyncio.run(mech.run_ALPHABITZ_research_agent())
    asyncio.run(mech.run_ALPHABITZ_gatherstate_agent())

if __name__ == "__main__":
    main()