# 🦭 Podman & GCP Deployment - Complete Setup

## ✅ What's Been Created

### 1. Container Configuration
- ✅ `Dockerfile` - Production-ready container definition (Podman compatible)
- ✅ `.dockerignore` - Optimized build context
- ✅ Health check endpoint configured

### 2. Deployment Scripts
- ✅ `deploy.sh` - Quick one-command GCP deployment (Podman-based)
- ✅ `cloudbuild.yaml` - Automated CI/CD configuration

### 3. Documentation
- ✅ `PODMAN_SETUP.md` - **Podman-specific guide** (NEW)
- ✅ `DOCKER_SETUP.md` - Quick start guide
- ✅ `DEPLOYMENT_GUIDE.md` - Comprehensive deployment documentation
- ✅ `DOCKER_README.md` - Docker/Podman reference guide

## 🚀 Quick Start Guide

### Step 1: Install Podman

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get update && sudo apt-get install -y podman
```

**macOS:**
```bash
brew install podman
podman machine init
podman machine start
```

**Authenticate with GCR:**
```bash
gcloud auth print-access-token | podman login -u oauth2accesstoken --password-stdin gcr.io
```

### Step 2: Test Locally with Podman

```bash
# Build
podman build -t nasa-backend .

# Run
podman run -d -p 8000:8080 --name nasa-backend nasa-backend

# Test
curl http://localhost:8000/health
```

### Step 3: Deploy to GCP Cloud Run

```bash
# Make executable (first time only)
chmod +x deploy.sh

# Deploy (uses Podman)
./deploy.sh
```

### Step 4: Update Frontend

After deployment, update your frontend's `.env` file:

```bash
NEXT_PUBLIC_API_URL=https://nasa-backend-xxxxx-uc.a.run.app
```

## 📋 Deployment Checklist

### Before Deployment
- [ ] Podman installed and tested locally
- [ ] GCP account created
-   [ ] gcloud CLI installed
-   [ ] GCP project created
-   [ ] Billing enabled on GCP project

### During Deployment

-   [ ] Run `./deploy.sh`
-   [ ] Note the deployed URL
-   [ ] Test health endpoint
-   [ ] Verify API docs are accessible

### After Deployment

-   [ ] Update frontend API URL
-   [ ] Test all endpoints
-   [ ] Configure custom domain (optional)
-   [ ] Set up monitoring
-   [ ] Configure secrets in Secret Manager

## 🔧 Configuration Options

### Environment Variables

**Local Podman:**
```bash
podman run -d -p 8000:8080 \
  -e PORT=8080 \
  -e GOOGLE_API_KEY=your-key \
  nasa-backend
```

**GCP Cloud Run:**
```bash
gcloud run deploy nasa-backend \
  --set-env-vars="PORT=8080,GOOGLE_API_KEY=your-key"
```

### Resource Settings

**Development (Lower cost):**

```bash
--memory 1Gi --cpu 1 --max-instances 3
```

**Production (Recommended):**

```bash
--memory 2Gi --cpu 2 --max-instances 10
```

**High Traffic:**

```bash
--memory 4Gi --cpu 4 --max-instances 20
```

## 📊 Cost Estimates (GCP Cloud Run)

| Usage                      | Resources | Est. Monthly Cost |
| -------------------------- | --------- | ----------------- |
| **Light** (10k requests)   | 1GB/1CPU  | $5-10             |
| **Medium** (100k requests) | 2GB/2CPU  | $15-25            |
| **Heavy** (1M requests)    | 2GB/2CPU  | $50-80            |

_Costs based on us-central1 region_

## 🧪 Testing Your Deployment

### 1. Health Check

```bash
curl https://your-service-url.run.app/health
```

### 2. API Documentation

```bash
open https://your-service-url.run.app/docs
```

### 3. Search Endpoint

```bash
curl -X POST https://your-service-url.run.app/search \
  -H "Content-Type: application/json" \
  -d '{"query": "test", "num_results": 5}'
```

### 4. Workflow Endpoint

```bash
curl -X POST https://your-service-url.run.app/workflow \
  -H "Content-Type: application/json" \
  -d '{
    "query": "test",
    "num_results": 3,
    "use_llm": true,
    "google_api_key": "your-key",
    "model_name": "gemini-2.0-flash-exp"
  }'
```

## 🔄 Update Deployment

### Option 1: Using deploy.sh (Podman)
```bash
./deploy.sh
```

### Option 2: Manual with Podman
```bash
podman build -t gcr.io/PROJECT_ID/nasa-backend .
podman push gcr.io/PROJECT_ID/nasa-backend
gcloud run deploy nasa-backend --image gcr.io/PROJECT_ID/nasa-backend
```

### Option 3: Automated CI/CD
```bash
# Trigger build from git
gcloud builds submit --config cloudbuild.yaml

# Or set up automatic triggers in GCP Console
```

## 🛠️ Common Commands

### Podman (Recommended)
```bash
# Build
podman build -t nasa-backend .

# Run
podman run -d -p 8000:8080 --name nasa-backend nasa-backend

# Logs
podman logs -f nasa-backend

# Stop
podman stop nasa-backend

# Remove
podman rm nasa-backend

# Rebuild
podman build --no-cache -t nasa-backend .
```

### Docker (Alternative)
```bash
# Build
docker build -t nasa-backend .

# Run
docker run -d -p 8000:8080 --name nasa-backend nasa-backend

# Logs
docker logs -f nasa-backend

# Stop
docker stop nasa-backend

# Remove
docker rm nasa-backend

# Rebuild
docker build --no-cache -t nasa-backend .
```

### GCP

```bash
# Deploy
gcloud run deploy nasa-backend --image gcr.io/PROJECT_ID/nasa-backend

# View URL
gcloud run services describe nasa-backend --format='value(status.url)'

# Logs
gcloud run services logs tail nasa-backend

# Update settings
gcloud run services update nasa-backend --memory 4Gi --cpu 4

# Delete
gcloud run services delete nasa-backend
```

## 📈 Monitoring & Logs

### Podman Logs
```bash
# Follow logs
podman logs -f nasa-backend

# Export logs
podman logs nasa-backend > logs.txt

# Container stats
podman stats nasa-backend
```

### Docker Logs (Alternative)
```bash
# Follow logs
docker logs -f nasa-backend

# Export logs
docker logs nasa-backend > logs.txt

# Container stats
docker stats nasa-backend
```

### GCP Logs

```bash
# Real-time logs
gcloud run services logs tail nasa-backend --region=us-central1

# View in console
# Navigate to: Cloud Run > nasa-backend > Logs
```

## 🔐 Security Recommendations

1. **Use Secret Manager** for sensitive data
2. **Enable HTTPS** (automatic on Cloud Run)
3. **Restrict CORS** origins in code
4. **Add authentication** for production
5. **Regular security scans**: `docker scan nasa-backend`
6. **Keep dependencies updated**

## 📚 Documentation Reference

| Document | Purpose | When to Use |
|----------|---------|-------------|
| [**PODMAN_SETUP.md**](./PODMAN_SETUP.md) | **Podman guide** | **Podman-specific setup** |
| [DOCKER_SETUP.md](./DOCKER_SETUP.md) | Quick start | First time setup |
| [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md) | Complete guide | Detailed deployment |
| [DOCKER_README.md](./DOCKER_README.md) | Docker/Podman details | Container troubleshooting |
| `cloudbuild.yaml` | CI/CD config | Automated deployments |
| `deploy.sh` | Quick deploy | One-command deployment |

## 🆘 Troubleshooting

### Issue: Container won't start
```bash
# Check logs with Podman
podman logs nasa-backend

# Common fixes:
podman restart nasa-backend
podman build --no-cache -t nasa-backend .

# Or with Docker
docker logs nasa-backend
docker restart nasa-backend
docker build --no-cache -t nasa-backend .
```

### Issue: GCP deployment fails

```bash
# Check build logs
gcloud builds log $(gcloud builds list --limit=1 --format='value(id)')

# Common fixes:
# - Increase memory: --memory 2Gi
# - Check quotas in GCP Console
# - Verify billing is enabled
```

### Issue: API not responding
```bash
# Podman
podman exec nasa-backend curl http://localhost:8080/health

# Docker
docker exec nasa-backend curl http://localhost:8080/health

# GCP
curl https://your-service-url.run.app/health

# Check firewall/CORS settings
```

### Issue: Podman authentication failed
```bash
# Re-authenticate with GCR
gcloud auth print-access-token | podman login -u oauth2accesstoken --password-stdin gcr.io

# Verify login
podman login --get-login gcr.io
```

## 🦭 Why Podman?

- ✅ **Daemonless** - No background process needed
- ✅ **Rootless** - Run without root privileges
- ✅ **Docker-compatible** - Uses same commands
- ✅ **More secure** - No daemon running as root
- ✅ **GCP compatible** - Works seamlessly with Cloud Run

**Quick comparison:**
```bash
# Podman (recommended)
podman build -t nasa-backend .
podman push gcr.io/PROJECT/nasa-backend

# Docker (also works)
docker build -t nasa-backend .
docker push gcr.io/PROJECT/nasa-backend

# Both deploy the same way
gcloud run deploy nasa-backend --image gcr.io/PROJECT/nasa-backend
```

## ✨ Next Steps

1. **Customize Resources**: Adjust memory/CPU based on usage
2. **Add Monitoring**: Set up Cloud Monitoring alerts
3. **Configure Domain**: Add custom domain in Cloud Run
4. **Enable CI/CD**: Set up automatic deployments
5. **Scale Settings**: Configure auto-scaling parameters
6. **Backup Strategy**: Set up database backups

## 🎯 Quick Reference

**Local Development (Podman):**
```bash
podman build -t nasa-backend . && podman run -d -p 8000:8080 nasa-backend
```

**Local Development (Docker):**
```bash
docker build -t nasa-backend . && docker run -d -p 8000:8080 nasa-backend
```

**Deploy to GCP:**
```bash
./deploy.sh  # Uses Podman by default
```

**View Logs:**
```bash
# Local (Podman): podman logs -f nasa-backend
# Local (Docker): docker logs -f nasa-backend
# GCP: gcloud run services logs tail nasa-backend
```

**Update Deployment (Podman):**
```bash
podman build -t gcr.io/PROJECT_ID/nasa-backend .
podman push gcr.io/PROJECT_ID/nasa-backend
gcloud run deploy nasa-backend --image gcr.io/PROJECT_ID/nasa-backend
```

**Update Deployment (Docker):**
```bash
gcloud builds submit --tag gcr.io/PROJECT_ID/nasa-backend
gcloud run deploy nasa-backend --image gcr.io/PROJECT_ID/nasa-backend
```

---

**🦭 You're all set with Podman! Start with `./deploy.sh` to deploy to GCP Cloud Run.**
