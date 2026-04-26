from flask import Flask, render_template, jsonify
import json

app = Flask(__name__)

# Load communities data
with open('communities.json', encoding='utf-8') as f:
    communities_data = json.load(f)

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)