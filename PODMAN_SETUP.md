# 🦭 Podman Deployment Guide for NASA Backend

## Why Podman?

Podman is a daemonless container engine that's:
- ✅ **Rootless** - Run containers without root privileges
- ✅ **Docker-compatible** - Uses same commands and Dockerfiles
- ✅ **Secure** - No daemon running as root
- ✅ **Lightweight** - No background daemon needed
- ✅ **GCP Compatible** - Works with Google Container Registry

## 📋 Prerequisites

### 1. Install Podman

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get update
sudo apt-get install -y podman
```

**Linux (Fedora/RHEL/CentOS):**
```bash
sudo dnf install -y podman
```

**macOS:**
```bash
brew install podman
podman machine init
podman machine start
```

**Windows (WSL2):**
```bash
# Inside WSL2
sudo apt-get update
sudo apt-get install -y podman
```

### 2. Install Google Cloud SDK
```bash
# Linux/macOS
curl https://sdk.cloud.google.com | bash
exec -l $SHELL

# Or use package manager
# Ubuntu/Debian: sudo apt-get install google-cloud-cli
# macOS: brew install --cask google-cloud-sdk
```

### 3. Authenticate Podman with GCR

```bash
# Configure Docker credential helper for Podman
gcloud auth configure-docker

# For podman specifically
gcloud auth print-access-token | podman login -u oauth2accesstoken --password-stdin gcr.io
```

## 🚀 Quick Start

### Local Testing

```bash
# Navigate to project
cd "NASA Project"

# Build with Podman
podman build -t nasa-backend .

# Run locally
podman run -d -p 8000:8080 --name nasa-backend nasa-backend

# Test
curl http://localhost:8000/health

# View logs
podman logs -f nasa-backend

# Stop
podman stop nasa-backend
podman rm nasa-backend
```

### Deploy to GCP Cloud Run

```bash
# Make deploy script executable
chmod +x deploy.sh

# Run deployment
./deploy.sh
```

The script will:
1. ✅ Check Podman installation
2. ✅ Build image with Podman
3. ✅ Push to Google Container Registry
4. ✅ Deploy to Cloud Run
5. ✅ Test health endpoint

## 📦 Manual Deployment Steps

### Step 1: Authenticate
```bash
# Set GCP project
gcloud config set project YOUR_PROJECT_ID

# Login to GCR with Podman
gcloud auth print-access-token | podman login -u oauth2accesstoken --password-stdin gcr.io
```

### Step 2: Build Image
```bash
# Build
podman build -t gcr.io/YOUR_PROJECT_ID/nasa-backend .

# Verify
podman images | grep nasa-backend
```

### Step 3: Push to GCR
```bash
# Push
podman push gcr.io/YOUR_PROJECT_ID/nasa-backend

# Verify in GCP Console
# Container Registry > Images > nasa-backend
```

### Step 4: Deploy to Cloud Run
```bash
gcloud run deploy nasa-backend \
    --image gcr.io/YOUR_PROJECT_ID/nasa-backend \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated \
    --port 8080 \
    --memory 2Gi \
    --cpu 2 \
    --timeout 300 \
    --max-instances 10
```

### Step 5: Test
```bash
# Get URL
URL=$(gcloud run services describe nasa-backend \
    --platform managed \
    --region us-central1 \
    --format 'value(status.url)')

# Test
curl $URL/health
open $URL/docs
```

## 🔧 Podman Commands Reference

### Container Management
```bash
# List running containers
podman ps

# List all containers
podman ps -a

# Run container
podman run -d -p 8000:8080 --name nasa-backend nasa-backend

# Run with environment variables
podman run -d -p 8000:8080 \
    -e GOOGLE_API_KEY=your-key \
    --name nasa-backend nasa-backend

# Stop container
podman stop nasa-backend

# Start container
podman start nasa-backend

# Remove container
podman rm nasa-backend

# Force remove running container
podman rm -f nasa-backend
```

### Image Management
```bash
# List images
podman images

# Build image
podman build -t nasa-backend .

# Build without cache
podman build --no-cache -t nasa-backend .

# Tag image
podman tag nasa-backend gcr.io/PROJECT_ID/nasa-backend

# Remove image
podman rmi nasa-backend

# Remove unused images
podman image prune -a
```

### Logs and Debugging
```bash
# View logs
podman logs nasa-backend

# Follow logs
podman logs -f nasa-backend

# Container stats
podman stats nasa-backend

# Inspect container
podman inspect nasa-backend

# Execute command in container
podman exec -it nasa-backend bash

# Check container health
podman healthcheck run nasa-backend
```

### Registry Operations
```bash
# Login to GCR
gcloud auth print-access-token | podman login -u oauth2accesstoken --password-stdin gcr.io

# Push image
podman push gcr.io/PROJECT_ID/nasa-backend

# Pull image
podman pull gcr.io/PROJECT_ID/nasa-backend

# Search images
podman search nasa
```

## 🔄 Docker to Podman Migration

Podman uses the same commands as Docker! Just replace `docker` with `podman`:

```bash
# Docker → Podman
docker build -t nasa-backend .     → podman build -t nasa-backend .
docker run -d -p 8000:8080 ...     → podman run -d -p 8000:8080 ...
docker ps                          → podman ps
docker logs nasa-backend           → podman logs nasa-backend
docker stop nasa-backend           → podman stop nasa-backend
```

### Alias for Docker Compatibility
```bash
# Add to ~/.bashrc or ~/.zshrc
alias docker=podman

# Now you can use docker commands
docker build -t nasa-backend .
docker run -d -p 8000:8080 nasa-backend
```

## 🐟 Fish Shell Specific

For Fish shell users:

```fish
# Add alias to ~/.config/fish/config.fish
alias docker=podman

# Or create function
function docker
    podman $argv
end
```

## 🔐 Rootless Mode (Recommended)

Podman can run containers without root privileges:

```bash
# Check if running rootless
podman info | grep -i rootless

# Configure rootless (if needed)
podman system migrate

# Run container rootless
podman run --rm -d -p 8000:8080 nasa-backend

# Set up user namespaces (Linux)
echo "user.max_user_namespaces=15000" | sudo tee -a /etc/sysctl.conf
sudo sysctl -p
```

## 🔍 Troubleshooting

### Issue: "permission denied" when building
```bash
# Check Podman installation
podman version

# Run with sudo (not recommended for production)
sudo podman build -t nasa-backend .

# Or configure rootless mode
podman system migrate
```

### Issue: "cannot push to gcr.io"
```bash
# Re-authenticate
gcloud auth login
gcloud auth configure-docker

# Login with Podman
gcloud auth print-access-token | podman login -u oauth2accesstoken --password-stdin gcr.io

# Check credentials
podman login --get-login gcr.io
```

### Issue: "port already in use"
```bash
# Find and stop container using port
podman ps | grep 8080
podman stop <container-id>

# Or use different port
podman run -d -p 8001:8080 nasa-backend
```

### Issue: Podman machine not running (macOS)
```bash
# Check status
podman machine list

# Start machine
podman machine start

# Initialize new machine
podman machine init --cpus 2 --memory 4096 --disk-size 50
podman machine start
```

### Issue: "exec: failed to exec in container"
```bash
# Remove container and rebuild
podman rm -f nasa-backend
podman rmi nasa-backend
podman build --no-cache -t nasa-backend .
podman run -d -p 8000:8080 nasa-backend
```

## 📊 Performance Comparison

| Feature | Docker | Podman |
|---------|--------|--------|
| Daemon | Required | Daemonless |
| Root privileges | Usually required | Rootless supported |
| Security | Good | Better (no root daemon) |
| Command compatibility | Native | 100% compatible |
| Build speed | Fast | Similar/slightly faster |
| Resource usage | Higher (daemon) | Lower (no daemon) |
| GCP integration | ✅ | ✅ |

## 🆚 Podman vs Docker for GCP

**Why Podman for GCP Cloud Run:**
- ✅ More secure (no root daemon)
- ✅ Same deployment process
- ✅ Better resource management
- ✅ Works with GCR seamlessly
- ✅ No licensing concerns
- ✅ Open source (Apache 2.0)

**Deployment process is identical:**
```bash
# With Docker
docker build -t gcr.io/PROJECT/nasa-backend .
docker push gcr.io/PROJECT/nasa-backend

# With Podman
podman build -t gcr.io/PROJECT/nasa-backend .
podman push gcr.io/PROJECT/nasa-backend

# Both deploy the same way
gcloud run deploy nasa-backend --image gcr.io/PROJECT/nasa-backend
```

## 🚀 Advanced Usage

### Multi-arch Builds
```bash
# Build for different architectures
podman build --platform linux/amd64 -t nasa-backend .
podman build --platform linux/arm64 -t nasa-backend-arm .
```

### Podman Compose
```bash
# Install podman-compose
pip install podman-compose

# Use docker-compose.yml files
podman-compose up -d
podman-compose down
```

### Pod Management (Kubernetes-like)
```bash
# Create pod
podman pod create --name nasa-pod -p 8080:8080

# Run container in pod
podman run -d --pod nasa-pod nasa-backend

# List pods
podman pod ps

# Stop pod
podman pod stop nasa-pod
```

### Volume Management
```bash
# Create volume
podman volume create nasa-data

# Run with volume
podman run -d -p 8000:8080 \
    -v nasa-data:/app/chroma_db \
    --name nasa-backend nasa-backend

# List volumes
podman volume ls

# Inspect volume
podman volume inspect nasa-data
```

## 🔗 Useful Resources

- **Podman Official Docs**: https://docs.podman.io
- **Podman Tutorial**: https://podman.io/getting-started
- **GCP + Podman**: https://cloud.google.com/blog/topics/developers-practitioners/podman-google-cloud
- **Rootless Containers**: https://rootlesscontaine.rs
- **Podman Desktop**: https://podman-desktop.io

## 📝 Quick Reference

**Build & Run Locally:**
```bash
podman build -t nasa-backend . && podman run -d -p 8000:8080 nasa-backend
```

**Deploy to GCP:**
```bash
./deploy.sh
```

**View Logs:**
```bash
# Local
podman logs -f nasa-backend

# GCP
gcloud run services logs tail nasa-backend
```

**Update Deployment:**
```bash
podman build -t gcr.io/PROJECT_ID/nasa-backend .
podman push gcr.io/PROJECT_ID/nasa-backend
gcloud run deploy nasa-backend --image gcr.io/PROJECT_ID/nasa-backend
```

---

**🦭 You're all set with Podman! More secure, daemonless, and 100% Docker-compatible.**
