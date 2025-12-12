
from flask import Flask, render_template, jsonify, request
import json
import os
import shutil
from datetime import datetime

app = Flask(__name__)

CONSENSUS_PATH = "data/consensus_vocabulary.json"
PENDING_PATH = "data/pending_review.json"

def load_json(path):
    if not os.path.exists(path):
        return {}
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading {path}: {e}")
        return {}

def save_json(path, data):
    with open(path, 'w') as f:
        json.dump(data, f, indent=4)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/pending', methods=['GET'])
def get_pending():
    data = load_json(PENDING_PATH)
    return jsonify(data)

@app.route('/api/consensus', methods=['GET'])
def get_consensus():
    data = load_json(CONSENSUS_PATH)
    return jsonify(data)

@app.route('/api/arbitrate', methods=['POST'])
def arbitrate():
    """
    Action: 'approve' or 'reject'
    Concept: key in pending dict
    """
    req_data = request.json
    action = req_data.get('action')
    concept = req_data.get('concept')

    pending = load_json(PENDING_PATH)
    consensus = load_json(CONSENSUS_PATH)

    if concept not in pending:
        return jsonify({"status": "error", "message": "Concept not found in pending"}), 404

    item_data = pending[concept]

    if action == 'approve':
        # Move to consensus
        # Structure in consensus might be simplified or full, we'll keep full for now
        consensus[concept] = item_data
        del pending[concept]
        save_json(CONSENSUS_PATH, consensus)
        save_json(PENDING_PATH, pending)
        return jsonify({"status": "success", "message": f"Approved {concept}"})

    elif action == 'reject':
        # Just delete from pending
        del pending[concept]
        save_json(PENDING_PATH, pending)
        return jsonify({"status": "success", "message": f"Rejected {concept}"})

    return jsonify({"status": "error", "message": "Invalid action"}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)
