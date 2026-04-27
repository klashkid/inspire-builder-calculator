from flask import Flask, render_template, jsonify
import json
import os

app = Flask(__name__)

# More robust JSON loading
json_path = os.path.join(os.path.dirname(__file__), 'communities.json')

try:
    with open(json_path, encoding='utf-8') as f:
        communities_data = json.load(f)
    print("✅ communities.json loaded successfully")
except Exception as e:
    print(f"❌ Error loading communities.json: {e}")
    communities_data = {}

# Rest of your routes...
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_communities/<division>')
def get_communities(division):
    if division in communities_data:
        return jsonify(list(communities_data[division].keys()))
    return jsonify([])

@app.route('/get_community_data/<division>/<path:community>')
def get_community_data(division, community):
    try:
        comm = communities_data.get(division, {}).get(community)
        if comm:
            return jsonify(comm)
        return jsonify({"error": "Community not found"})
    except:
        return jsonify({"error": "Data not found"})