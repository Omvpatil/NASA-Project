# 🚀 NASA Research Backend - Docker & GCP Deployment

## 📋 Quick Overview

This FastAPI backend is containerized with Docker and ready for deployment to Google Cloud Platform (GCP) Cloud Run.

## 🐳 Files Overview

```
NASA Project/
├── Dockerfile              # Docker container definition
├── .dockerignore          # Files to exclude from Docker build
├── requirements.txt       # Python dependencies
├── deploy.sh             # Quick deployment script
├── cloudbuild.yaml       # GCP Cloud Build config
├── DEPLOYMENT_GUIDE.md   # Comprehensive deployment guide
└── DOCKER_README.md      # Docker-specific documentation
```

## ⚡ Quick Start

### 1️⃣ Local Docker Development

```bash
# Build the image
docker build -t nasa-backend .

# Run the container
docker run -d -p 8000:8080 --name nasa-backend nasa-backend

# Test the API
curl http://localhost:8000/health
curl http://localhost:8000/docs
```

### 2️⃣ Deploy to GCP Cloud Run

```bash
# Make deploy script executable (if needed)
chmod +x deploy.sh

# Run deployment
./deploy.sh
```

That's it! The script will:

-   ✅ Configure your GCP project
-   ✅ Build and push Docker image
-   ✅ Deploy to Cloud Run
-   ✅ Provide your service URL

## 📖 Documentation

| Document                                     | Description                                |
| -------------------------------------------- | ------------------------------------------ |
| [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md) | Complete deployment guide with all options |
| [DOCKER_README.md](./DOCKER_README.md)       | Docker-specific setup and troubleshooting  |
| This README                                  | Quick start guide                          |

## 🔧 Configuration

### Environment Variables

**Required:**

-   `PORT`: 8080 (default for Cloud Run)

**Optional:**

-   `GOOGLE_API_KEY`: For Gemini AI features
-   `CORS_ORIGINS`: Allowed CORS origins

### Resource Settings (Cloud Run)

| Setting       | Development | Production |
| ------------- | ----------- | ---------- |
| Memory        | 1 GB        | 2 GB       |
| CPU           | 1           | 2          |
| Timeout       | 60s         | 300s       |
| Max Instances | 3           | 10         |

## 🧪 Testing

### Health Check

```bash
curl http://localhost:8000/health
```

### API Documentation

```bash
# Interactive docs
open http://localhost:8000/docs

# Or visit in browser
http://localhost:8000/redoc
```

### Test Search Endpoint

```bash
curl -X POST http://localhost:8000/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "microgravity effects",
    "num_results": 5
  }'
```

## 🔄 Deployment Options

### Option 1: Quick Deploy Script (Recommended)

```bash
./deploy.sh
```

### Option 2: Manual GCP Deployment

```bash
# Set project
gcloud config set project YOUR_PROJECT_ID

# Build & deploy
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/nasa-backend
gcloud run deploy nasa-backend \
  --image gcr.io/YOUR_PROJECT_ID/nasa-backend \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

### Option 3: Automated CI/CD

Use the included `cloudbuild.yaml`:

```bash
gcloud builds submit --config cloudbuild.yaml
```

Or set up a trigger in GCP Console for automatic deployments on git push.

## 📊 Monitoring

### View Logs (Docker)

```bash
docker logs -f nasa-backend
```

### View Logs (GCP)

```bash
gcloud run services logs tail nasa-backend --region=us-central1
```

### Container Stats

```bash
docker stats nasa-backend
```

## 🛠️ Troubleshooting

### Docker Issues

**Container won't start:**

```bash
docker logs nasa-backend
docker restart nasa-backend
```

**Port already in use:**

```bash
docker run -d -p 9000:8080 --name nasa-backend nasa-backend
```

**Build fails:**

```bash
docker build --no-cache -t nasa-backend .
```

### GCP Issues

**Deployment fails:**

```bash
# Check build logs
gcloud builds log $(gcloud builds list --limit=1 --format='value(id)')
```

**High latency:**

```bash
# Increase resources
gcloud run services update nasa-backend \
  --memory 4Gi \
  --cpu 4
```

**Service not responding:**

```bash
# Check service status
gcloud run services describe nasa-backend --region=us-central1

# View recent logs
gcloud run services logs tail nasa-backend --region=us-central1
```

## 🔐 Security Best Practices

1. **Use Secret Manager** for API keys:

    ```bash
    gcloud secrets create gemini-api-key --data-file=-
    ```

2. **Restrict CORS** in `main.py`:

    ```python
    allow_origins=["https://your-frontend.com"]
    ```

3. **Enable authentication** (optional):
    ```bash
    gcloud run deploy nasa-backend --no-allow-unauthenticated
    ```

## 💰 Cost Optimization

### Development

```bash
gcloud run deploy nasa-backend \
  --memory 1Gi \
  --cpu 1 \
  --max-instances 3 \
  --min-instances 0
```

### Production with Auto-scaling

```bash
gcloud run deploy nasa-backend \
  --memory 2Gi \
  --cpu 2 \
  --max-instances 10 \
  --min-instances 1  # Keeps 1 instance warm
```

## 📁 Persistent Data

For data persistence, mount volumes:

```bash
docker run -d \
  -p 8000:8080 \
  -v $(pwd)/chroma_db:/app/chroma_db \
  -v $(pwd)/papers.db:/app/papers.db \
  nasa-backend
```

## 🔗 Useful Links

-   **GCP Cloud Run**: https://cloud.google.com/run/docs
-   **FastAPI Docs**: https://fastapi.tiangolo.com/deployment/
-   **Docker Hub**: https://hub.docker.com/
-   **Python Docker**: https://hub.docker.com/_/python

## 📞 Support

For detailed help, check:

1. [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md) - Complete deployment guide
2. [DOCKER_README.md](./DOCKER_README.md) - Docker troubleshooting
3. Docker logs: `docker logs nasa-backend`
4. GCP logs: `gcloud run services logs tail nasa-backend`

## 🎯 Next Steps After Deployment

1. **Update Frontend**: Set `NEXT_PUBLIC_API_URL` to your Cloud Run URL
2. **Configure Domain**: Add custom domain in Cloud Run console
3. **Set up Monitoring**: Enable Cloud Monitoring and alerts
4. **Configure Secrets**: Move API keys to Secret Manager
5. **Enable CI/CD**: Set up Cloud Build triggers

---

**Happy Deploying! 🚀**
