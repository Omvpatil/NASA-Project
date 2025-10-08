#!/bin/bash
# Quick GCP Cloud Run Deployment for NASA Backend (Using Podman)

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${GREEN}🚀 NASA Backend - GCP Cloud Run Deployment (Podman)${NC}\n"

# Check for podman
if ! command -v podman &> /dev/null; then
    echo -e "${RED}❌ Podman not installed. Install from: https://podman.io/docs/installation${NC}"
    exit 1
fi

# Check for gcloud
if ! command -v gcloud &> /dev/null; then
    echo -e "${RED}❌ gcloud CLI not installed. Install from: https://cloud.google.com/sdk/docs/install${NC}"
    exit 1
fi

# Get project ID
echo -e "${YELLOW}Enter your GCP Project ID:${NC}"
read -r PROJECT_ID

# Configuration
REGION="us-central1"
SERVICE_NAME="nasa-backend"
IMAGE_NAME="gcr.io/${PROJECT_ID}/${SERVICE_NAME}"

echo -e "\n${GREEN}📋 Configuration:${NC}"
echo -e "  Project: ${PROJECT_ID}"
echo -e "  Region: ${REGION}"
echo -e "  Service: ${SERVICE_NAME}"
echo -e "  Image: ${IMAGE_NAME}\n"

# Confirm
echo -e "${YELLOW}Continue with deployment? (y/n):${NC}"
read -r CONFIRM
if [[ ! $CONFIRM =~ ^[Yy]$ ]]; then
    echo -e "${RED}Deployment cancelled.${NC}"
    exit 0
fi

# Set project
echo -e "\n${GREEN}📌 Setting GCP project...${NC}"
gcloud config set project ${PROJECT_ID}

# Enable APIs
echo -e "${GREEN}🔧 Enabling required APIs...${NC}"
gcloud services enable cloudbuild.googleapis.com run.googleapis.com containerregistry.googleapis.com

# Build image with Podman
echo -e "\n${GREEN}🏗️  Building image with Podman...${NC}"
podman build -t ${IMAGE_NAME} .

# Push to Google Container Registry
echo -e "${GREEN}📦 Pushing to GCR...${NC}"
podman push ${IMAGE_NAME}

# Deploy to Cloud Run
echo -e "\n${GREEN}🚢 Deploying to Cloud Run...${NC}"
gcloud run deploy ${SERVICE_NAME} \
    --image ${IMAGE_NAME} \
    --platform managed \
    --region ${REGION} \
    --allow-unauthenticated \
    --port 8080 \
    --memory 2Gi \
    --cpu 2 \
    --timeout 300 \
    --max-instances 10 \
    --set-env-vars="PORT=8080"

# Get URL
BACKEND_URL=$(gcloud run services describe ${SERVICE_NAME} \
    --platform managed \
    --region ${REGION} \
    --format 'value(status.url)')

# Success
echo -e "\n${GREEN}═══════════════════════════════════════${NC}"
echo -e "${GREEN}✅ Deployment Complete!${NC}"
echo -e "${GREEN}═══════════════════════════════════════${NC}"
echo -e "${YELLOW}Backend URL:${NC} ${BACKEND_URL}"
echo -e "${GREEN}═══════════════════════════════════════${NC}\n"

# Test
echo -e "${YELLOW}Testing health endpoint...${NC}"
if curl -f -s ${BACKEND_URL}/health > /dev/null; then
    echo -e "${GREEN}✅ Health check passed!${NC}\n"
else
    echo -e "${RED}❌ Health check failed. Check logs:${NC}"
    echo -e "  gcloud run services logs tail ${SERVICE_NAME} --region=${REGION}\n"
fi

# Save URL
echo "${BACKEND_URL}" > deployment-url.txt

echo -e "\n${GREEN}📝 Next steps:${NC}"
echo -e "  1. Update frontend .env with: NEXT_PUBLIC_API_URL=${BACKEND_URL}"
echo -e "  2. Test at: ${BACKEND_URL}/docs"
echo -e "  3. View logs: gcloud run services logs tail ${SERVICE_NAME} --region=${REGION}\n"
echo -e "${GREEN}📝 URL saved to deployment-url.txt${NC}\n"

echo -e "${YELLOW}Next steps:${NC}"
echo -e "  1. Update frontend NEXT_PUBLIC_API_URL to: ${BACKEND_URL}"
echo -e "  2. Test endpoints: ${BACKEND_URL}/docs"
echo -e "  3. View logs: gcloud run services logs tail ${SERVICE_NAME} --region=${REGION}"
