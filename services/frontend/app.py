from flask import Flask, render_template, jsonify, request, redirect, url_for
import requests
import os
import json

app = Flask(__name__)

# Get backend URL from environment variables, default to localhost in development
BACKEND_URL = os.environ.get("BACKEND_URL", "http://localhost:5000")

@app.route('/')
def index():
    try:
        # Get tasks from backend API
        response = requests.get(f"{BACKEND_URL}/api/tasks")
        tasks = response.json() if response.status_code == 200 else []
        
        # Get backend info
        info_response = requests.get(f"{BACKEND_URL}/api/info")
        info = info_response.json() if info_response.status_code == 200 else {}
        
        return render_template('index.html', tasks=tasks, backend_info=info)
    except requests.exceptions.RequestException as e:
        return render_template('index.html', 
                              tasks=[], 
                              error=f"Failed to connect to backend API: {str(e)}",
                              backend_info={})

@app.route('/add-task', methods=['POST'])
def add_task():
    task_title = request.form.get('title')
    if task_title:
        try:
            requests.post(
                f"{BACKEND_URL}/api/tasks",
                json={"title": task_title}
            )
        except requests.exceptions.RequestException:
            pass  # Error handling will be done on the main page
    return redirect(url_for('index'))

@app.route('/toggle-task/<int:task_id>', methods=['POST'])
def toggle_task(task_id):
    try:
        # First, get the current state of the task
        response = requests.get(f"{BACKEND_URL}/api/tasks/{task_id}")
        if response.status_code == 200:
            task = response.json()
            # Toggle the completed status
            updated = requests.put(
                f"{BACKEND_URL}/api/tasks/{task_id}",
                json={"completed": not task["completed"]}
            )
    except requests.exceptions.RequestException:
        pass  # Error handling will be done on the main page
    return redirect(url_for('index'))

@app.route('/health')
def health():
    try:
        # Check backend health
        backend_health = requests.get(f"{BACKEND_URL}/api/health")
        backend_status = backend_health.json() if backend_health.status_code == 200 else {"status": "unreachable"}
        
        # Return frontend health along with backend status
        return jsonify({
            "frontend": {"status": "healthy"},
            "backend": backend_status
        })
    except requests.exceptions.RequestException:
        return jsonify({
            "frontend": {"status": "healthy"},
            "backend": {"status": "unreachable"}
        })

@app.route('/info')
def info():
    # Return information about the frontend application
    env_info = {
        "APP_NAME": os.environ.get("APP_NAME", "Frontend App"),
        "VERSION": os.environ.get("VERSION", "1.0.0"),
        "ENVIRONMENT": os.environ.get("ENVIRONMENT", "development"),
        "BACKEND_URL": BACKEND_URL,
        "KUBERNETES_NODE": os.environ.get("KUBERNETES_NODE", "unknown")
    }
    return jsonify(env_info)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 3000))
    app.run(host='0.0.0.0', port=port, debug=os.environ.get("DEBUG", "true").lower() == "true")