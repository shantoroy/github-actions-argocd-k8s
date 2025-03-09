from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import time
import json

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Simple in-memory database
tasks = [
    {"id": 1, "title": "Learn Kubernetes", "completed": False},
    {"id": 2, "title": "Master ArgoCD", "completed": False},
    {"id": 3, "title": "Implement CI/CD Pipeline", "completed": False}
]

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "timestamp": time.time()})

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    return jsonify(tasks)

@app.route('/api/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = next((task for task in tasks if task["id"] == task_id), None)
    if task:
        return jsonify(task)
    return jsonify({"error": "Task not found"}), 404

@app.route('/api/tasks', methods=['POST'])
def create_task():
    if not request.json or 'title' not in request.json:
        return jsonify({"error": "Invalid task data"}), 400
    
    task_id = max(task["id"] for task in tasks) + 1 if tasks else 1
    task = {
        "id": task_id,
        "title": request.json["title"],
        "completed": False
    }
    tasks.append(task)
    return jsonify(task), 201

@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = next((task for task in tasks if task["id"] == task_id), None)
    if not task:
        return jsonify({"error": "Task not found"}), 404
    
    if not request.json:
        return jsonify({"error": "Invalid task data"}), 400
    
    if 'title' in request.json:
        task['title'] = request.json['title']
    if 'completed' in request.json:
        task['completed'] = bool(request.json['completed'])
    
    return jsonify(task)

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    global tasks
    task = next((task for task in tasks if task["id"] == task_id), None)
    if not task:
        return jsonify({"error": "Task not found"}), 404
    
    tasks = [task for task in tasks if task["id"] != task_id]
    return jsonify({"result": "Task deleted"}), 200

@app.route('/api/info', methods=['GET'])
def get_info():
    # Return information about the application, including environment variables
    env_info = {
        "APP_NAME": os.environ.get("APP_NAME", "Backend API"),
        "VERSION": os.environ.get("VERSION", "1.0.0"),
        "ENVIRONMENT": os.environ.get("ENVIRONMENT", "development"),
        "KUBERNETES_NODE": os.environ.get("KUBERNETES_NODE", "unknown")
    }
    return jsonify(env_info)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=os.environ.get("DEBUG", "true").lower() == "true")