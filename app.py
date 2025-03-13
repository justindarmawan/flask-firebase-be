from flask import Flask, request, jsonify
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, firestore
import os
import json

app = Flask(__name__)
CORS(app, origins=["https://justindarmawan.github.io"])

cred = credentials.Certificate("/etc/secrets/serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

@app.route("/")
def home():
    return jsonify({"message": "Flask Firebase API is running!"})
    
@app.route("/homepage", methods=["GET"])
def fetch_homepage():
    try:
        doc_ref = db.collection("website_content").document("homepage")
        doc = doc_ref.get()
        
        if doc.exists:
            return jsonify(doc.to_dict()), 200
        else:
            return jsonify({"error": "No homepage content found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
