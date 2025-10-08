# NASA Research Platform - FastAPI Backend Deployment Guide

## 📦 Docker Setup

### Prerequisites

-   Docker installed on your system
-   GCP account (for Cloud Run deployment)
-   gcloud CLI installed and configured

---

## 🐳 Local Docker Deployment

### 1. Build the Docker Image

```bash
cd "NASA Project"
docker build -t nasa-backend:latest .
```

### 2. Run the Container Locally

```bash
docker run -d \
  -p 8000:8080 \
  --name nasa-backend \
  -v $(pwd)/chroma_db:/app/chroma_db \
  -v $(pwd)/small_persistent_db:/app/small_persistent_db \
  -v $(pwd)/papers.db:/app/papers.db \
  nasa-backend:latest
```

### 3. Test the API

```bash
# Health check
curl http://localhost:8000/health

# Test search endpoint
curl -X POST http://localhost:8000/search \
  -H "Content-Type: application/json" \
  -d '{"query": "microgravity effects", "num_results": 5}'
```

### 4. View Logs

```bash
docker logs -f nasa-backend
```

### 5. Stop the Container

```bash
docker stop nasa-backend
docker rm nasa-backend
```

---

## ☁️ GCP Cloud Run Deployment

### Option 1: Using gcloud CLI (Recommended)

#### Step 1: Set up GCP Project

```bash
# Set your project ID
export PROJECT_ID="your-gcp-project-id"
export REGION="us-central1"

# Set the project
gcloud config set project ${PROJECT_ID}

# Enable required APIs
gcloud services enable \
    cloudbuild.googleapis.com \
    run.googleapis.com \
    containerregistry.googleapis.com
```

#### Step 2: Build and Push Image

```bash
# Navigate to backend directory
cd "NASA Project"

# Build and push to Google Container Registry
gcloud builds submit --tag gcr.io/${PROJECT_ID}/nasa-backend
```

#### Step 3: Deploy to Cloud Run

```bash
gcloud run deploy nasa-backend \
    --image gcr.io/${PROJECT_ID}/nasa-backend \
    --platform managed \
    --region ${REGION} \
    --allow-unauthenticated \
    --port 8080 \
    --memory 2Gi \
    --cpu 2 \
    --timeout 300 \
    --max-instances 10 \
    --set-env-vars="PORT=8080"
```

#### Step 4: Get the Service URL

```bash
gcloud run services describe nasa-backend \
    --platform managed \
    --region ${REGION} \
    --format 'value(status.url)'
```

### Option 2: Using Google Cloud Console

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Navigate to **Cloud Run**
3. Click **Create Service**
4. Select **Deploy from Container Registry**
5. Choose the image: `gcr.io/YOUR_PROJECT_ID/nasa-backend`
6. Configure:
    - **Container port**: 8080
    - **Memory**: 2 GiB
    - **CPU**: 2
    - **Timeout**: 300 seconds
    - **Max instances**: 10
    - **Authentication**: Allow unauthenticated
7. Click **Create**

---

## 🔧 Environment Variables

### Required for Production

```bash
# Add to Cloud Run deployment
--set-env-vars="
PORT=8080,
GOOGLE_API_KEY=your-gemini-api-key
"
```

### Optional Variables

```bash
--set-env-vars="
PORT=8080,
GOOGLE_API_KEY=your-api-key,
MAX_WORKERS=4,
CORS_ORIGINS=https://yourfrontend.com
"
```

---

## 📊 Resource Configuration

### Recommended for Production

| Resource          | Value | Reason                    |
| ----------------- | ----- | ------------------------- |
| **Memory**        | 2 GiB | ChromaDB + LLM processing |
| **CPU**           | 2     | Parallel request handling |
| **Timeout**       | 300s  | Long-running LLM requests |
| **Max Instances** | 10    | Auto-scaling limit        |
| **Min Instances** | 0     | Cost optimization         |

### Cost Optimization

```bash
# Development/Testing (Lower resources)
gcloud run deploy nasa-backend \
    --memory 1Gi \
    --cpu 1 \
    --max-instances 3 \
    --min-instances 0
```

---

## 🔐 Security Best Practices

### 1. Enable Authentication (Optional)

```bash
gcloud run deploy nasa-backend \
    --no-allow-unauthenticated
```

### 2. Use Secret Manager for API Keys

```bash
# Create secret
echo -n "your-api-key" | gcloud secrets create gemini-api-key \
    --data-file=-

# Grant access to Cloud Run
gcloud secrets add-iam-policy-binding gemini-api-key \
    --member="serviceAccount:PROJECT_NUMBER-compute@developer.gserviceaccount.com" \
    --role="roles/secretmanager.secretAccessor"

# Deploy with secret
gcloud run deploy nasa-backend \
    --set-secrets="GOOGLE_API_KEY=gemini-api-key:latest"
```

### 3. Restrict CORS Origins

Update `main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-frontend-domain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 📈 Monitoring & Logging

### View Logs

```bash
# Real-time logs
gcloud run services logs tail nasa-backend --region=${REGION}

# View in Cloud Console
# Navigate to: Cloud Run > nasa-backend > Logs
```

### Set up Alerts

```bash
# CPU usage alert
gcloud alpha monitoring policies create \
    --notification-channels=CHANNEL_ID \
    --display-name="High CPU Usage" \
    --condition-threshold-value=0.8 \
    --condition-threshold-duration=300s
```

---

## 🔄 CI/CD with Cloud Build

### Create cloudbuild.yaml

```yaml
# cloudbuild.yaml
steps:
    # Build the container image
    - name: "gcr.io/cloud-builders/docker"
      args: ["build", "-t", "gcr.io/$PROJECT_ID/nasa-backend", "."]

    # Push to Container Registry
    - name: "gcr.io/cloud-builders/docker"
      args: ["push", "gcr.io/$PROJECT_ID/nasa-backend"]

    # Deploy to Cloud Run
    - name: "gcr.io/google.com/cloudsdktool/cloud-sdk"
      entrypoint: gcloud
      args:
          - "run"
          - "deploy"
          - "nasa-backend"
          - "--image"
          - "gcr.io/$PROJECT_ID/nasa-backend"
          - "--region"
          - "us-central1"
          - "--platform"
          - "managed"
          - "--allow-unauthenticated"

images:
    - "gcr.io/$PROJECT_ID/nasa-backend"
```

### Trigger Build

```bash
gcloud builds submit --config cloudbuild.yaml
```

---

## 🧪 Testing the Deployment

### Health Check

```bash
BACKEND_URL=$(gcloud run services describe nasa-backend \
    --region=${REGION} \
    --format='value(status.url)')

curl ${BACKEND_URL}/health
```

### Test Search

```bash
curl -X POST ${BACKEND_URL}/search \
    -H "Content-Type: application/json" \
    -d '{
        "query": "microgravity effects on cells",
        "num_results": 5
    }'
```

### Test Workflow

```bash
curl -X POST ${BACKEND_URL}/workflow \
    -H "Content-Type: application/json" \
    -d '{
        "query": "space radiation DNA damage",
        "num_results": 3,
        "use_llm": true,
        "google_api_key": "your-key",
        "model_name": "gemini-2.0-flash-exp"
    }'
```

---

## 📝 Troubleshooting

### Container Won't Start

```bash
# Check logs
docker logs nasa-backend

# Common issues:
# 1. Port mismatch (ensure PORT=8080)
# 2. Missing dependencies in requirements.txt
# 3. Database files not accessible
```

### Cloud Run Deployment Fails

```bash
# Check build logs
gcloud builds log $(gcloud builds list --limit=1 --format='value(id)')

# Common issues:
# 1. Insufficient memory/CPU
# 2. Timeout too low
# 3. Missing environment variables
```

### High Latency

```bash
# Increase resources
gcloud run services update nasa-backend \
    --memory 4Gi \
    --cpu 4

# Enable min instances (keeps container warm)
gcloud run services update nasa-backend \
    --min-instances 1
```

---

## 💰 Cost Estimation

### Cloud Run Pricing (us-central1)

-   **CPU**: $0.00002400/vCPU-second
-   **Memory**: $0.00000250/GiB-second
-   **Requests**: $0.40/million requests

### Example Monthly Cost (2 GiB, 2 CPU)

-   **100,000 requests/month**: ~$15-25
-   **1,000,000 requests/month**: ~$50-80

### Cost Optimization Tips

1. Set `--min-instances 0` (pay only when used)
2. Use appropriate timeout values
3. Enable request compression
4. Cache responses where possible

---

## 🚀 Production Checklist

-   [ ] Environment variables configured
-   [ ] Secrets stored in Secret Manager
-   [ ] CORS origins restricted
-   [ ] Memory/CPU sized appropriately
-   [ ] Monitoring and alerts set up
-   [ ] Custom domain configured (optional)
-   [ ] SSL/TLS enabled
-   [ ] Backup strategy for databases
-   [ ] CI/CD pipeline configured
-   [ ] Load testing completed

---

## 📚 Additional Resources

-   [Cloud Run Documentation](https://cloud.google.com/run/docs)
-   [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
-   [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)
-   [GCP Pricing Calculator](https://cloud.google.com/products/calculator)

---

## 🆘 Support

For issues or questions:

1. Check Cloud Run logs
2. Review Docker container logs
3. Verify environment variables
4. Check API quotas and limits
5. Review GCP billing dashboard
