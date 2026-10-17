#!/usr/bin/env bash
# ==============================================================================
# ClipSense (Explainable Video Coach) — Automated Cloud Run Deployment Script
# ==============================================================================
# Automates:
# 1. Loading configuration from .env or active gcloud config
# 2. Enabling required Google Cloud APIs
# 3. Creating dedicated runtime service account & granting Vertex AI permissions
# 4. Building and deploying container to Google Cloud Run
# 5. Health checking the deployed live service
# ==============================================================================

set -euo pipefail

# Text formatting
BOLD="\033[1m"
GREEN="\033[0;32m"
CYAN="\033[0;36m"
YELLOW="\033[0;33m"
RED="\033[0;31m"
RESET="\033[0m"

echo -e "${BOLD}${CYAN}🚀 Starting ClipSense Cloud Run Deployment Automation...${RESET}\n"

# 1. Load environment variables from .env if present
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [ -f "${SCRIPT_DIR}/.env" ]; then
  echo -e "${CYAN}ℹ️  Loading configuration from .env file...${RESET}"
  # Export non-comment lines
  set -a
  source <(grep -v '^#' "${SCRIPT_DIR}/.env" | sed -e 's/\r$//')
  set +a
fi

# 2. Resolve Project ID & Region
PROJECT_ID="${GCP_PROJECT_ID:-$(gcloud config get-value project 2>/dev/null || true)}"
if [ -z "${PROJECT_ID}" ] || [ "${PROJECT_ID}" = "(unset)" ]; then
  echo -e "${RED}❌ Error: No GCP Project ID found.${RESET}"
  echo -e "Please specify GCP_PROJECT_ID in .env or run: gcloud config set project <PROJECT_ID>"
  exit 1
fi

REGION="${GCP_REGION:-us-central1}"
SERVICE_NAME="clipsense-backend"
SA_NAME="clipsense-runtime"
SA_EMAIL="${SA_NAME}@${PROJECT_ID}.iam.gserviceaccount.com"
MODEL="${GEMINI_MODEL:-gemini-3.8-flash}"

echo -e "📌 ${BOLD}Deployment Configuration:${RESET}"
echo -e "   • Project ID:       ${GREEN}${PROJECT_ID}${RESET}"
echo -e "   • Region:           ${GREEN}${REGION}${RESET}"
echo -e "   • Cloud Run Service:${GREEN}${SERVICE_NAME}${RESET}"
echo -e "   • Service Account:  ${GREEN}${SA_EMAIL}${RESET}"
echo -e "   • Gemini Model:     ${GREEN}${MODEL}${RESET}\n"

# 3. Set active project in gcloud
echo -e "${CYAN}🔧 Setting active gcloud project to ${PROJECT_ID}...${RESET}"
gcloud config set project "${PROJECT_ID}" --quiet

# 4. Enable required Google Cloud APIs
echo -e "\n${CYAN}📦 Ensuring required Google Cloud APIs are enabled...${RESET}"
gcloud services enable \
  aiplatform.googleapis.com \
  run.googleapis.com \
  cloudbuild.googleapis.com \
  artifactregistry.googleapis.com \
  --project="${PROJECT_ID}" --quiet

# 5. Create Service Account if not existing
echo -e "\n${CYAN}👤 Checking runtime service account...${RESET}"
if gcloud iam service-accounts describe "${SA_EMAIL}" --project="${PROJECT_ID}" &>/dev/null; then
  echo -e "   ✅ Service account ${BOLD}${SA_NAME}${RESET} already exists."
else
  echo -e "   Creating service account: ${BOLD}${SA_NAME}${RESET}..."
  gcloud iam service-accounts create "${SA_NAME}" \
    --project="${PROJECT_ID}" \
    --display-name="ClipSense runtime" --quiet
  echo -e "   ✅ Created ${SA_EMAIL}"
fi

# 6. Grant Vertex AI user permissions to service account
echo -e "\n${CYAN}🔐 Granting roles/aiplatform.user permissions...${RESET}"
gcloud projects add-iam-policy-binding "${PROJECT_ID}" \
  --member="serviceAccount:${SA_EMAIL}" \
  --role="roles/aiplatform.user" \
  --condition=None --quiet >/dev/null

# 7. Deploy to Google Cloud Run
echo -e "\n${BOLD}${CYAN}🚢 Deploying ${SERVICE_NAME} to Google Cloud Run (${REGION})...${RESET}"

# Build env vars string
ENV_VARS="GCP_PROJECT_ID=${PROJECT_ID},GCP_REGION=${REGION},GEMINI_MODEL=${MODEL},USE_SAMPLE_CACHE_ONLY=false"
if [ -n "${GEMINI_API_KEY:-}" ]; then
  ENV_VARS="${ENV_VARS},GEMINI_API_KEY=${GEMINI_API_KEY}"
fi

gcloud run deploy "${SERVICE_NAME}" \
  --source "${SCRIPT_DIR}/backend" \
  --project="${PROJECT_ID}" \
  --region="${REGION}" \
  --service-account="${SA_EMAIL}" \
  --allow-unauthenticated \
  --timeout=300 \
  --min-instances=0 \
  --max-instances=2 \
  --set-env-vars="${ENV_VARS}" \
  --quiet

# 8. Retrieve Service URL and verify health
echo -e "\n${CYAN}🔍 Retrieving deployed Service URL...${RESET}"
SERVICE_URL=$(gcloud run services describe "${SERVICE_NAME}" \
  --project="${PROJECT_ID}" \
  --region="${REGION}" \
  --format="value(status.url)")

echo -e "\n${BOLD}${GREEN}🎉 Deployment Succeeded!${RESET}"
echo -e "🔗 Live Service URL: ${BOLD}${CYAN}${SERVICE_URL}${RESET}"

# 9. Health check
echo -e "\n${CYAN}🩺 Running automated health check...${RESET}"
HEALTH_RESP=$(curl -s --http1.1 "${SERVICE_URL}/api/health" || true)
if echo "${HEALTH_RESP}" | grep -q '"status":"ok"'; then
  echo -e "   ${GREEN}✅ Health check passed:${RESET} ${HEALTH_RESP}"
else
  echo -e "   ${YELLOW}⚠️  Response:${RESET} ${HEALTH_RESP}"
fi

# 10. Update Frontend API URL hint
echo -e "\n${BOLD}💡 Next Step for Frontend:${RESET}"
echo -e "To point your local React frontend to this deployed backend, update ${BOLD}frontend/.env${RESET}:"
echo -e "   ${CYAN}VITE_API_URL=${SERVICE_URL}${RESET}\n"
