# 🐳 Docker Setup - NASA Research Backend

## Quick Start

### Local Development with Docker

```bash
# 1. Build the image
docker build -t nasa-backend .

# 2. Run the container
docker run -d -p 8000:8080 --name nasa-backend nasa-backend

# 3. Test the API
curl http://localhost:8000/health
```

## Deployment Options

### Option 1: Quick Deploy to GCP (Recommended)

```bash
# Run the deployment script
./deploy.sh
```

The script will:

-   ✅ Enable required GCP APIs
-   ✅ Build and push Docker image
-   ✅ Deploy to Cloud Run
-   ✅ Provide the service URL

### Option 2: Manual GCP Deployment

```bash
# Set your project
export PROJECT_ID="your-project-id"

# Build and push
gcloud builds submit --tag gcr.io/${PROJECT_ID}/nasa-backend

# Deploy
gcloud run deploy nasa-backend \
    --image gcr.io/${PROJECT_ID}/nasa-backend \
    --region us-central1 \
    --platform managed \
    --allow-unauthenticated \
    --port 8080 \
    --memory 2Gi \
    --cpu 2
```

### Option 3: Other Cloud Providers

#### AWS ECS

```bash
# Build and push to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin YOUR_AWS_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com
docker build -t nasa-backend .
docker tag nasa-backend:latest YOUR_AWS_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/nasa-backend:latest
docker push YOUR_AWS_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/nasa-backend:latest
```

#### Azure Container Instances

```bash
# Build and push to ACR
az acr login --name yourregistry
docker build -t yourregistry.azurecr.io/nasa-backend .
docker push yourregistry.azurecr.io/nasa-backend
az container create --resource-group myResourceGroup --name nasa-backend --image yourregistry.azurecr.io/nasa-backend --cpu 2 --memory 2
```

#### DigitalOcean App Platform

```bash
# Use the Dockerfile directly in App Platform dashboard
# Or deploy via doctl CLI
doctl apps create --spec app.yaml
```

## Environment Variables

### Required

-   `PORT`: Application port (default: 8080)

### Optional

-   `GOOGLE_API_KEY`: For Gemini AI features
-   `MAX_WORKERS`: Number of worker processes
-   `CORS_ORIGINS`: Allowed CORS origins (comma-separated)

## Dockerfile Explanation

```dockerfile
FROM python:3.11-slim              # Lightweight Python base
WORKDIR /app                        # Set working directory
COPY requirements.txt .             # Copy dependencies
RUN pip install -r requirements.txt # Install dependencies
COPY . .                            # Copy application code
EXPOSE 8080                         # Expose port
CMD ["uvicorn", "main:app", ...]   # Start application
```

## Resource Requirements

| Environment      | Memory | CPU | Instances |
| ---------------- | ------ | --- | --------- |
| **Development**  | 1 GB   | 1   | 1         |
| **Production**   | 2 GB   | 2   | 1-10      |
| **High Traffic** | 4 GB   | 4   | 1-20      |

## Persistent Data

The following directories should be mounted as volumes for data persistence:

```bash
docker run -d \
  -v $(pwd)/chroma_db:/app/chroma_db \
  -v $(pwd)/small_persistent_db:/app/small_persistent_db \
  -v $(pwd)/papers.db:/app/papers.db \
  nasa-backend
```

## Health Checks

The Dockerfile includes a health check:

```dockerfile
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1
```

## Troubleshooting

### Container won't start

```bash
# Check logs
docker logs nasa-backend

# Common issues:
# 1. Port already in use: Change -p 8000:8080 to -p 9000:8080
# 2. Memory limit: Increase Docker memory allocation
```

### API not responding

```bash
# Check if container is running
docker ps

# Restart container
docker restart nasa-backend

# Check health
docker exec nasa-backend curl http://localhost:8080/health
```

### Build fails

```bash
# Clear Docker cache and rebuild
docker build --no-cache -t nasa-backend .

# Check requirements.txt for issues
```

## Security Best Practices

1. **Don't commit secrets**: Use environment variables or secret management
2. **Run as non-root**: Container runs as non-root user
3. **Scan for vulnerabilities**: `docker scan nasa-backend`
4. **Keep base image updated**: Regularly update Python base image
5. **Minimize image size**: Use `.dockerignore` to exclude unnecessary files

## Multi-stage Builds (Optional)

For smaller images:

```dockerfile
# Build stage
FROM python:3.11-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Runtime stage
FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .
ENV PATH=/root/.local/bin:$PATH
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
```

## CI/CD Integration

### GitHub Actions

```yaml
name: Deploy to GCP
on:
    push:
        branches: [main]
jobs:
    deploy:
        runs-on: ubuntu-latest
        steps:
            - uses: actions/checkout@v2
            - uses: google-github-actions/setup-gcloud@v0
              with:
                  project_id: ${{ secrets.GCP_PROJECT_ID }}
                  service_account_key: ${{ secrets.GCP_SA_KEY }}
            - run: |
                  gcloud builds submit --tag gcr.io/${{ secrets.GCP_PROJECT_ID }}/nasa-backend
                  gcloud run deploy nasa-backend --image gcr.io/${{ secrets.GCP_PROJECT_ID }}/nasa-backend
```

## Monitoring

### View Container Stats

```bash
docker stats nasa-backend
```

### Export Logs

```bash
docker logs nasa-backend > backend-logs.txt
```

### Monitor with Prometheus

```bash
# Add prometheus metrics endpoint to FastAPI
# Deploy with monitoring
docker run -d \
  --name prometheus \
  -p 9090:9090 \
  -v $(pwd)/prometheus.yml:/etc/prometheus/prometheus.yml \
  prom/prometheus
```

## Useful Commands

```bash
# Build
docker build -t nasa-backend .

# Run detached
docker run -d -p 8000:8080 --name nasa-backend nasa-backend

# View logs
docker logs -f nasa-backend

# Execute command in container
docker exec -it nasa-backend bash

# Stop and remove
docker stop nasa-backend && docker rm nasa-backend

# Remove image
docker rmi nasa-backend

# Prune unused resources
docker system prune -a
```

## Documentation

-   Full deployment guide: [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md)
-   API documentation: http://localhost:8000/docs (when running)
-   GCP Cloud Run docs: https://cloud.google.com/run/docs

## Support

For issues:

1. Check `docker logs nasa-backend`
2. Verify environment variables
3. Test with `curl http://localhost:8000/health`
4. Review [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md)
