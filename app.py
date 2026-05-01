from flask import Flask, render_template, jsonify
import json
import os

app = Flask(__name__)

# Load communities.json
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_PATH = os.path.join(BASE_DIR, 'communities.json')

try:
    with open(JSON_PATH, encoding='utf-8') as f:
        data = json.load(f)
    # Handle the new nested structure
    communities_data = data.get("divisions", {})
    print(f"✅ Loaded {len(communities_data)} divisions successfully")
except Exception as e:
    print(f"❌ Error loading communities.json: {e}")
    communities_data = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_communities/<division>')
def get_communities(division):
    div_data = communities_data.get(division, {})
    communities = div_data.get("communities", {})
    print(f"Division '{division}' requested → {len(communities)} communities found")
    return jsonify(list(communities.keys()))

@app.route('/get_community_data/<division>/<path:community>')
def get_community_data(division, community):
    try:
        comm = communities_data.get(division, {}).get("communities", {}).get(community)
        if comm:
            return jsonify(comm)
        return jsonify({"error": "Community not found"})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)