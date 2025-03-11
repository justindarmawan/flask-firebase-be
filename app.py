from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import credentials, firestore
import os
import json

app = Flask(__name__)

cred = credentials.Certificate("/etc/secrets/serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

@app.route("/")
def home():
    return jsonify({"message": "Flask Firebase API is running!"})

@app.route("/add", methods=["POST"])
def add_data():
    try:
        data = request.json
        db.collection("test").document().set(data)
        return jsonify({"success": True}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/list", methods=["GET"])
def list_data():
    try:
        docs = db.collection("test").stream()
        data = [doc.to_dict() for doc in docs]
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
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
