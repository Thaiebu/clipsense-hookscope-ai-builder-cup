#!/usr/bin/env bash
# ==============================================================================
# ClipSense (Frontend) — Automated Cloud Run Deployment Script
# ==============================================================================

set -euo pipefail

# Text formatting
BOLD="\033[1m"
GREEN="\033[0;32m"
CYAN="\033[0;36m"
YELLOW="\033[0;33m"
RED="\033[0;31m"
RESET="\033[0m"

echo -e "${BOLD}${CYAN}🚀 Starting ClipSense Frontend Cloud Run Deployment...${RESET}\n"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [ -f "${SCRIPT_DIR}/.env" ]; then
  set -a
  source <(grep -v '^#' "${SCRIPT_DIR}/.env" | sed -e 's/\r$//')
  set +a
fi

PROJECT_ID="${GCP_PROJECT_ID:-$(gcloud config get-value project 2>/dev/null || true)}"
if [ -z "${PROJECT_ID}" ] || [ "${PROJECT_ID}" = "(unset)" ]; then
  echo -e "${RED}❌ Error: No GCP Project ID found.${RESET}"
  exit 1
fi

REGION="${GCP_REGION:-us-central1}"
SERVICE_NAME="clipsense-frontend"

echo -e "📌 ${BOLD}Frontend Deployment Configuration:${RESET}"
echo -e "   • Project ID:       ${GREEN}${PROJECT_ID}${RESET}"
echo -e "   • Region:           ${GREEN}${REGION}${RESET}"
echo -e "   • Service Name:     ${GREEN}${SERVICE_NAME}${RESET}\n"

echo -e "${CYAN}🚢 Building and deploying ${SERVICE_NAME} to Google Cloud Run...${RESET}"

gcloud run deploy "${SERVICE_NAME}" \
  --source "${SCRIPT_DIR}/frontend" \
  --project="${PROJECT_ID}" \
  --region="${REGION}" \
  --allow-unauthenticated \
  --timeout=300 \
  --min-instances=0 \
  --max-instances=2 \
  --quiet

FRONTEND_URL=$(gcloud run services describe "${SERVICE_NAME}" \
  --project="${PROJECT_ID}" \
  --region="${REGION}" \
  --format="value(status.url)")

echo -e "\n${BOLD}${GREEN}🎉 Frontend Deployment Succeeded!${RESET}"
echo -e "🔗 Live Web App: ${BOLD}${CYAN}${FRONTEND_URL}${RESET}\n"
