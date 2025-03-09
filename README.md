# GitOps CI/CD Pipeline with GitHub Actions, ArgoCD, and Minikube

This repository demonstrates a complete CI/CD pipeline using GitHub Actions for continuous integration and ArgoCD for continuous deployment to Kubernetes (Minikube). The project includes sample Python-based frontend and backend microservices.

## Architecture Overview

![Architecture Diagram](https://via.placeholder.com/800x400?text=CI/CD+Pipeline+Architecture)

### Components

- **Frontend Service**: Flask web application with simple UI
- **Backend Service**: Flask API service
- **CI Pipeline**: GitHub Actions workflows for testing and building container images
- **CD Pipeline**: ArgoCD for GitOps-based deployments
- **Kubernetes**: Minikube for local development

### Workflow

1. Developer commits code to GitHub repository
2. GitHub Actions triggers CI pipeline:
   - Runs tests
   - Builds Docker images
   - Pushes images to GitHub Container Registry
   - Updates K8s manifests with new image tags
3. ArgoCD detects changes in K8s manifests
4. ArgoCD automatically syncs the changes to the Kubernetes cluster

## Prerequisites

- [Git](https://git-scm.com/downloads)
- [Docker](https://docs.docker.com/get-docker/)
- [Minikube](https://minikube.sigs.k8s.io/docs/start/)
- [kubectl](https://kubernetes.io/docs/tasks/tools/)
- [ArgoCD CLI](https://argo-cd.readthedocs.io/en/stable/cli_installation/) (optional)

## Setup Instructions

### 1. Start Minikube

```bash
minikube start --driver=docker
```

### 2. Install ArgoCD on Minikube

```bash
kubectl create namespace argocd
kubectl apply -n argocd -f k8s/argocd/argocd-install.yaml
kubectl port-forward svc/argocd-server -n argocd 8080:443
```

Access ArgoCD UI at https://localhost:8080 with credentials:
- Username: admin
- Password: (Get initial password with command below)

```bash
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d
```

### 3. Deploy Applications with ArgoCD

```bash
kubectl apply -f k8s/argocd/applications/
```

### 4. Access the Application

```bash
minikube service frontend-service
```

## Local Development

### Running Services Locally

#### Backend Service

```bash
cd services/backend
pip install -r requirements.txt
python app.py
```

The backend service will be available at http://localhost:5000

#### Frontend Service

```bash
cd services/frontend
pip install -r requirements.txt
python app.py
```

The frontend service will be available at http://localhost:3000

### Running with Docker Compose (Alternative)

A docker-compose.yml file is provided for local development:

```bash
docker-compose up -d
```

## CI/CD Pipeline Explanation

### CI Pipeline (GitHub Actions)

The CI pipeline is triggered on push events to specific branches:
- `main` branch: Builds and deploys to production
- `staging` branch: Builds and deploys to staging
- Any other branch: Runs tests only

The workflow:
1. Checkout code
2. Set up Python environment
3. Install dependencies
4. Run tests
5. Build Docker image
6. Push to GitHub Container Registry
7. Update Kubernetes manifests with new image tag

### CD Pipeline (ArgoCD)

ArgoCD follows the GitOps pattern by:
1. Monitoring the Git repository for changes in Kubernetes manifests
2. Automatically syncing those changes to the cluster
3. Ensuring the cluster state matches the desired state in Git

## Project Structure

- `.github/workflows/`: Contains GitHub Actions workflow definitions
- `services/`: Contains the microservice applications
  - `backend/`: Backend API service
  - `frontend/`: Frontend web application
- `k8s/`: Contains Kubernetes manifests
  - `argocd/`: ArgoCD configuration
  - `backend/`: Backend service deployment manifests
  - `frontend/`: Frontend service deployment manifests

```
cicd-microservices-demo/
├── README.md
├── .github/
│   └── workflows/
│       ├── backend-ci.yml
│       └── frontend-ci.yml
├── services/
│   ├── backend/
│   │   ├── Dockerfile
│   │   ├── app.py
│   │   ├── requirements.txt
│   │   └── tests/
│   │       └── test_app.py
│   └── frontend/
│       ├── Dockerfile
│       ├── app.py
│       ├── requirements.txt
│       ├── static/
│       │   └── style.css
│       ├── templates/
│       │   └── index.html
│       └── tests/
│           └── test_app.py
└── k8s/
    ├── argocd/
    │   ├── applications/
    │   │   ├── backend-app.yaml
    │   │   └── frontend-app.yaml
    │   └── argocd-install.yaml
    ├── backend/
    │   ├── deployment.yaml
    │   └── service.yaml
    ├── frontend/
    │   ├── deployment.yaml
    │   └── service.yaml
    └── namespace.yaml
```


## Learning Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [ArgoCD Documentation](https://argo-cd.readthedocs.io/en/stable/)
- [Kubernetes Documentation](https://kubernetes.io/docs/home/)
- [GitOps Principles](https://www.gitops.tech/)

## License

This project is licensed under the MIT License - see the LICENSE file for details.




