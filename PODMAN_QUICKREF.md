# 🦭 Podman Quick Reference

## Installation

### Linux (Ubuntu/Debian)
```bash
sudo apt-get update
sudo apt-get install -y podman
```

### macOS
```bash
brew install podman
podman machine init
podman machine start
```

### Verify Installation
```bash
podman --version
podman info
```

## GCP Authentication

```bash
# Authenticate with Google Cloud
gcloud auth login
gcloud config set project YOUR_PROJECT_ID

# Login Podman to GCR
gcloud auth print-access-token | podman login -u oauth2accesstoken --password-stdin gcr.io

# Verify authentication
podman login --get-login gcr.io
```

## Docker to Podman Command Translation

| Task | Docker | Podman |
|------|--------|--------|
| **Build** | `docker build -t image .` | `podman build -t image .` |
| **Run** | `docker run -d -p 8000:8080 image` | `podman run -d -p 8000:8080 image` |
| **List** | `docker ps` | `podman ps` |
| **Logs** | `docker logs container` | `podman logs container` |
| **Stop** | `docker stop container` | `podman stop container` |
| **Remove** | `docker rm container` | `podman rm container` |
| **Images** | `docker images` | `podman images` |
| **Push** | `docker push image` | `podman push image` |
| **Pull** | `docker pull image` | `podman pull image` |
| **Exec** | `docker exec -it container bash` | `podman exec -it container bash` |

## Common Commands

### Build & Run
```bash
# Build
podman build -t nasa-backend .

# Run detached
podman run -d -p 8000:8080 --name nasa-backend nasa-backend

# Run with env vars
podman run -d -p 8000:8080 \
  -e GOOGLE_API_KEY=your-key \
  --name nasa-backend nasa-backend

# Run with volume
podman run -d -p 8000:8080 \
  -v ./data:/app/chroma_db \
  --name nasa-backend nasa-backend
```

### Container Management
```bash
# List running containers
podman ps

# List all containers
podman ps -a

# Stop container
podman stop nasa-backend

# Start container
podman start nasa-backend

# Restart container
podman restart nasa-backend

# Remove container
podman rm nasa-backend

# Force remove running container
podman rm -f nasa-backend

# Remove all stopped containers
podman container prune
```

### Image Management
```bash
# List images
podman images

# Remove image
podman rmi nasa-backend

# Remove unused images
podman image prune -a

# Tag image
podman tag nasa-backend gcr.io/PROJECT_ID/nasa-backend

# Inspect image
podman inspect nasa-backend
```

### Logs & Debugging
```bash
# View logs
podman logs nasa-backend

# Follow logs
podman logs -f nasa-backend

# Last 100 lines
podman logs --tail 100 nasa-backend

# Container stats
podman stats nasa-backend

# Execute command
podman exec nasa-backend curl http://localhost:8080/health

# Interactive shell
podman exec -it nasa-backend bash

# Copy files from container
podman cp nasa-backend:/app/logs.txt ./logs.txt

# Copy files to container
podman cp ./config.json nasa-backend:/app/config.json
```

### GCP Deployment
```bash
# Build for GCP
podman build -t gcr.io/PROJECT_ID/nasa-backend .

# Push to GCR
podman push gcr.io/PROJECT_ID/nasa-backend

# Deploy to Cloud Run
gcloud run deploy nasa-backend \
  --image gcr.io/PROJECT_ID/nasa-backend \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --port 8080 \
  --memory 2Gi \
  --cpu 2
```

## Podman-Specific Features

### Rootless Mode (Default)
```bash
# Check if running rootless
podman info | grep -i rootless

# Run as root (not recommended)
sudo podman run -d -p 8000:8080 nasa-backend
```

### Pod Management
```bash
# Create pod
podman pod create --name nasa-pod -p 8080:8080

# Run container in pod
podman run -d --pod nasa-pod nasa-backend

# List pods
podman pod ps

# Stop pod
podman pod stop nasa-pod

# Remove pod
podman pod rm nasa-pod
```

### System Management
```bash
# System info
podman system info

# Disk usage
podman system df

# Clean up everything
podman system prune -a

# Reset (macOS)
podman machine stop
podman machine rm
podman machine init
podman machine start
```

## Alias for Docker Compatibility

### Bash/Zsh
```bash
# Add to ~/.bashrc or ~/.zshrc
alias docker=podman

# Reload
source ~/.bashrc  # or ~/.zshrc
```

### Fish Shell
```fish
# Add to ~/.config/fish/config.fish
alias docker=podman

# Or create function
function docker
    podman $argv
end

# Reload
source ~/.config/fish/config.fish
```

## Troubleshooting

### Issue: "permission denied"
```bash
# Check Podman version
podman version

# Try rootless
podman system migrate

# Check user namespaces (Linux)
cat /proc/sys/user/max_user_namespaces
# Should be > 0
```

### Issue: "cannot push to gcr.io"
```bash
# Re-authenticate
gcloud auth login
gcloud auth print-access-token | podman login -u oauth2accesstoken --password-stdin gcr.io

# Check credentials
podman login --get-login gcr.io
```

### Issue: "port already in use"
```bash
# Find container using port
podman ps | grep 8080

# Stop it
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

# Reinitialize
podman machine stop
podman machine rm
podman machine init --cpus 2 --memory 4096
podman machine start
```

### Issue: Build fails
```bash
# Clear cache
podman system prune -a

# Build without cache
podman build --no-cache -t nasa-backend .

# Check disk space
podman system df
df -h
```

## Quick Deploy Script

```bash
#!/bin/bash
# Quick local test with Podman

# Variables
IMAGE_NAME="nasa-backend"
PORT=8000

# Build
echo "Building..."
podman build -t $IMAGE_NAME .

# Stop old container
echo "Cleaning up..."
podman rm -f $IMAGE_NAME 2>/dev/null || true

# Run new container
echo "Running..."
podman run -d -p $PORT:8080 --name $IMAGE_NAME $IMAGE_NAME

# Wait for startup
sleep 3

# Test
echo "Testing..."
curl http://localhost:$PORT/health

# Show logs
echo -e "\nLogs:"
podman logs $IMAGE_NAME

echo -e "\n✅ Container running at http://localhost:$PORT"
```

## Comparison: Podman vs Docker

| Feature | Podman | Docker |
|---------|--------|--------|
| **Daemon** | ❌ Daemonless | ✅ Requires daemon |
| **Root Access** | ❌ Rootless | ⚠️ Often needs root |
| **Security** | 🔒 More secure | 🔓 Less secure |
| **Commands** | Same as Docker | Standard |
| **Compose** | podman-compose | docker-compose |
| **Pods** | ✅ Kubernetes-like | ❌ No pods |
| **GCP** | ✅ Full support | ✅ Full support |
| **Performance** | Similar/Better | Similar |
| **License** | Apache 2.0 | Docker Desktop license |

## Resources

- **Podman Docs**: https://docs.podman.io
- **Tutorial**: https://podman.io/getting-started
- **GCP + Podman**: https://cloud.google.com/blog/topics/developers-practitioners/podman-google-cloud
- **Migration Guide**: https://podman.io/migrate

---

**🦭 Podman: Daemonless, Rootless, Docker-compatible!**
