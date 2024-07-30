# TentaGate: High-Performance API Gateway

## Table of Contents
1. [Introduction](#introduction)
2. [Features](#features)
3. [Architecture](#architecture)
4. [Local Development](#local-development)
5. [Deployment on Azure Kubernetes Service (AKS)](#deployment-on-azure-kubernetes-service-aks)
6. [Configuration](#configuration)
7. [Monitoring and Logging](#monitoring-and-logging)
8. [Scaling](#scaling)
9. [Security Considerations](#security-considerations)
10. [Troubleshooting](#troubleshooting)
11. [Contributing](#contributing)
12. [License](#license)

## Introduction

TentaGate is a high-performance API gateway built with FastAPI, designed to handle high loads in production environments. It serves as a central entry point for microservices architecture, providing essential features such as authentication, rate limiting, caching, and circuit breaking.

The name "TentaGate" is inspired by the multiple "tentacles" (connections) it manages, much like an octopus, while serving as a gateway for API requests.

## Features

- **JWT Authentication**: Secure your APIs with JSON Web Token authentication.
- **Rate Limiting**: Protect your backend services from overload with configurable rate limiting.
- **Response Caching**: Improve performance by caching responses with Redis.
- **Circuit Breaking**: Prevent cascading failures with a circuit breaker pattern.
- **Prometheus Metrics**: Monitor your gateway with built-in Prometheus metrics.
- **CORS Support**: Configure Cross-Origin Resource Sharing as needed.
- **Health Check Endpoint**: Easily monitor the health of your gateway.
- **Azure Kubernetes Service (AKS) Ready**: Deployment configurations for AKS included.

## Architecture

TentaGate is designed with a modular architecture:

- `main.py`: The core FastAPI application.
- `config.py`: Configuration management using environment variables.
- `auth.py`: JWT authentication logic.
- `cache.py`: Redis-based caching implementation.
- `rate_limiter.py`: Rate limiting functionality.
- `circuit_breaker.py`: Circuit breaker pattern implementation.

The application is containerized using Docker and deployed on Azure Kubernetes Service for scalability and ease of management.

## Local Development

1. Clone the repository:
    ```bash
    git clone https://github.com/pythopus/tentagate.git
    cd tentagate
    ```
2. Set up a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use venv\Scripts\activate
    ```
3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4. Set up environment variables in a `.env` file:
    ```bash
    JWT_SECRET_KEY=your_secret_key
    REDIS_URL=redis://localhost:6379
    ALLOWED_ORIGINS=http://localhost:3000,https://yourdomain.com
    ```
5. Run the application:
    ```bash
    uvicorn src.main:app --reload
    ```
6. Access the API documentation at `http://localhost:8000/docs`

## Deployment on Azure Kubernetes Service (AKS)

### Prerequisites

- Azure CLI installed and configured
- kubectl installed
- Docker installed

### Steps

1. Create an AKS cluster:
    ```bash
    az aks create --resource-group myResourceGroup --name myAKSCluster --node-count 3 --enable-addons monitoring --generate-ssh-keys
    ```
2. Connect to the AKS cluster:
    ```bash
    az aks get-credentials --resource-group myResourceGroup --name myAKSCluster
    ```
3. Create an Azure Container Registry (ACR):
    ```bash
    az acr create --resource-group myResourceGroup --name myACRRegistry --sku Basic
    ```
4. Build and push the Docker image:
    ```bash
    docker build -t myACRRegistry.azurecr.io/tentagate:v1 .
    az acr login --name myACRRegistry
    docker push myACRRegistry.azurecr.io/tentagate:v1
    ```
5. Create Kubernetes secrets:
    ```bash
    kubectl create secret generic tentagate-secrets --from-literal=jwt-secret-key=your_secret_key
    ```
6. Apply Kubernetes manifests:
    ```bash
    kubectl apply -f kubernetes/
    ```
7. Set up Ingress Controller:
    ```bash
    helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
    helm repo update
    helm install nginx-ingress ingress-nginx/ingress-nginx
    ```
8. Configure DNS and SSL (if needed)

## Configuration

TentaGate can be configured using environment variables or a `.env` file. Key configurations include:

- `JWT_SECRET_KEY`: Secret key for JWT authentication
- `REDIS_URL`: URL of the Redis server for caching and rate limiting
- `ALLOWED_ORIGINS`: Comma-separated list of allowed origins for CORS
- `BACKEND_SERVICES`: JSON-formatted dictionary of backend service URLs

## Monitoring and Logging

- Use Azure Monitor for containers to monitor your AKS cluster and TentaGate pods.
- Enable Prometheus metrics in your AKS cluster and scrape metrics from TentaGate's `/metrics` endpoint.
- Use Azure Log Analytics for centralized logging.

## Scaling

- Horizontal Pod Autoscaler (HPA) can be used to automatically scale TentaGate based on CPU or custom metrics.
- Consider using Azure Container Instances (ACI) for burst scaling.

## Security Considerations

- Keep your JWT secret key secure and rotate it regularly.
- Use Azure Key Vault for managing secrets instead of Kubernetes secrets for production deployments.
- Implement network policies to control traffic between pods.
- Regularly update dependencies and the base Docker image.

## Troubleshooting

- Check pod logs: `kubectl logs <pod-name>`
- Describe pods for events: `kubectl describe pod <pod-name>`
- Use `kubectl get events` to see cluster-wide events
- Check TentaGate's health endpoint: `/health`

## Contributing

Contributions to TentaGate are welcome! Please refer to the [CONTRIBUTING.md](CONTRIBUTING.md) file for guidelines.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.