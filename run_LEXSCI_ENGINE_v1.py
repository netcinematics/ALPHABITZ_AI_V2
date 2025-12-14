from alphabitz.lexsci_engine_v2 import LexSciEngine
# import json

def run_LEXSCI_ENGINE():
    """
    Entry point for ALPHABITZ LEXSCI ENGINE.
    Can be triggered by a cron job, CI/CD pipeline, or manual execution.
    """
    print("\n" + "="*60)
    print("   LEXSCI ENGINE | LEXICAL SCIENCE PROTOCOL")
    print("="*60 + "\n")
    
    # 1. Initialize the Mechanism
    # The Engine handles .env loading and file creation internally
    mech = LexSciEngine(
        vocab_path="data/consensus_vocabulary.json",
        pending_path="data/pending_review.json"
    )
    
    # 2. Define Targets (In production, this could fetch from the Pending file)
    targets = [
        "Artificial Intelligence",
        "Prompt Engineering",
        "Hallucination"
    ]
    
    # 3. Execution Loop
    for target in targets:
        result = mech.exactify(target)
        
        # Display Logic (The 'Console Report')
        if "error" not in result:
            analysis = result.get('axi_analysis', {})
            print(f"🔹 TARGET:   {target}")
            print(f"   REALITY:  {analysis.get('actual_reality')}")
            print(f"   ERROR:    {analysis.get('common_misnomer')}")
            print(f"   SYNTAX:   {result.get('ai_oil_syntax')}")
            print("-" * 60)
            
            # Here we would theoretically save to mech.pending_path
            # save_result(mech.pending_path, result)

if __name__ == "__main__":
    run_LEXSCI_ENGINE()