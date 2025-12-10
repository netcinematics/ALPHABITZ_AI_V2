import json
import os
import sys

# Define paths (matching run_mission.py)
PENDING_PATH = "data/pending_review.json"
CONSENSUS_PATH = "data/consensus_vocabulary.json"

def load_json(path):
    if not os.path.exists(path):
        return {}
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {}

def save_json(path, data):
    with open(path, 'w') as f:
        json.dump(data, f, indent=4)

def arbitrate():
    print("=== LEXSCI HUMAN ARBITRATION TERMINAL ===")
    
    pending = load_json(PENDING_PATH)
    if not pending:
        print("No pending concepts to review.")
        return

    consensus = load_json(CONSENSUS_PATH)
    
    concepts = list(pending.keys())
    print(f"Found {len(concepts)} concepts awaiting review.\n")

    for concept in concepts:
        data = pending[concept]
        print(f"--- REVIEWING: {concept} ---")
        print(json.dumps(data, indent=2))
        print("\nOPTIONS:")
        print("[A] Approve (Move to Consensus)")
        print("[R] Reject (Delete from Pending)")
        print("[S] Skip")
        print("[Q] Quit")
        
        choice = input("Select Action > ").strip().upper()
        
        if choice == 'A':
            consensus[concept] = data
            del pending[concept]
            print(f"APPROVED: {concept}")
        elif choice == 'R':
            del pending[concept]
            print(f"REJECTED: {concept}")
        elif choice == 'S':
            print("Skipped.")
            continue
        elif choice == 'Q':
            break
        else:
            print("Invalid choice, skipping.")

    # Save changes
    save_json(PENDING_PATH, pending)
    save_json(CONSENSUS_PATH, consensus)
    print("\nArbitration session complete. Files updated.")

if __name__ == "__main__":
    arbitrate()
