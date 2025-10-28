#!/bin/bash

# Azure App Service Assessment Script (Reader Access Version)
# This script collects App Service configuration data for best practices review
# Optimized for Reader access - skips commands requiring higher permissions

set -e

# Output directory for collected data
OUTPUT_DIR="./app-service-assessment"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
DATA_FILE="${OUTPUT_DIR}/app-services-data-${TIMESTAMP}.json"

# Create output directory
mkdir -p "${OUTPUT_DIR}"

echo "==================================================="
echo "Azure App Service Assessment Data Collection"
echo "(Reader Access Mode)"
echo "==================================================="
echo ""

# Get current subscription
SUBSCRIPTION=$(az account show --query name -o tsv)
SUBSCRIPTION_ID=$(az account show --query id -o tsv)

echo "Subscription: ${SUBSCRIPTION}"
echo "Subscription ID: ${SUBSCRIPTION_ID}"
echo ""

# Get list of all App Services
echo "Collecting App Service list..."
APP_SERVICES=$(az webapp list --query "[].{name:name, resourceGroup:resourceGroup, id:id}" -o json)

# Check if there are any App Services
APP_SERVICE_COUNT=$(echo "${APP_SERVICES}" | jq '. | length')
echo "Found ${APP_SERVICE_COUNT} App Service(s)"
echo ""

if [ "${APP_SERVICE_COUNT}" -eq 0 ]; then
    echo '{"subscription":"'"${SUBSCRIPTION}"'","subscriptionId":"'"${SUBSCRIPTION_ID}"'","assessmentDate":"'"$(date -u +"%Y-%m-%dT%H:%M:%SZ")"'","appServices":[]}' > "${DATA_FILE}"
    echo "No App Services found in subscription."
    exit 0
fi

# Start JSON array
echo "{" > "${DATA_FILE}"
echo "  \"subscription\": \"${SUBSCRIPTION}\"," >> "${DATA_FILE}"
echo "  \"subscriptionId\": \"${SUBSCRIPTION_ID}\"," >> "${DATA_FILE}"
echo "  \"assessmentDate\": \"$(date -u +"%Y-%m-%dT%H:%M:%SZ")\"," >> "${DATA_FILE}"
echo "  \"appServices\": [" >> "${DATA_FILE}"

# Counter for comma separation
counter=0

# Process each App Service
echo "${APP_SERVICES}" | jq -c '.[]' | while read -r app; do
    APP_NAME=$(echo "${app}" | jq -r '.name')
    RG=$(echo "${app}" | jq -r '.resourceGroup')
    
    echo "Processing: ${APP_NAME} (Resource Group: ${RG})"
    
    # Add comma for previous entry (except first)
    if [ ${counter} -gt 0 ]; then
        echo "," >> "${DATA_FILE}"
    fi
    
    echo "  {" >> "${DATA_FILE}"
    echo "    \"name\": \"${APP_NAME}\"," >> "${DATA_FILE}"
    echo "    \"resourceGroup\": \"${RG}\"," >> "${DATA_FILE}"
    
    # Basic configuration - Reader accessible
    echo "    Getting basic configuration..."
    CONFIG=$(az webapp show --name "${APP_NAME}" --resource-group "${RG}" -o json 2>/dev/null || echo '{}')
    echo "    \"config\": ${CONFIG}," >> "${DATA_FILE}"
    
    # App Service Plan details - Reader accessible
    echo "    Getting App Service Plan..."
    PLAN_ID=$(echo "${CONFIG}" | jq -r '.serverFarmId // empty')
    if [ -n "${PLAN_ID}" ]; then
        PLAN_NAME=$(echo "${PLAN_ID}" | awk -F'/' '{print $NF}')
        PLAN_RG=$(echo "${PLAN_ID}" | awk -F'/' '{print $5}')
        PLAN=$(az appservice plan show --name "${PLAN_NAME}" --resource-group "${PLAN_RG}" -o json 2>/dev/null || echo '{}')
    else
        PLAN='{}'
    fi
    echo "    \"appServicePlan\": ${PLAN}," >> "${DATA_FILE}"
    
    # Runtime configuration - Reader accessible
    echo "    Getting runtime configuration..."
    RUNTIME_CONFIG=$(az webapp config show --name "${APP_NAME}" --resource-group "${RG}" -o json 2>/dev/null || echo '{}')
    echo "    \"runtimeConfig\": ${RUNTIME_CONFIG}," >> "${DATA_FILE}"
    
    # Auth settings - May fail with reader, handle gracefully
    echo "    Getting authentication settings..."
    AUTH=$(az webapp auth show --name "${APP_NAME}" --resource-group "${RG}" -o json 2>/dev/null || echo '{"enabled":false,"note":"Requires contributor access"}')
    echo "    \"authConfig\": ${AUTH}," >> "${DATA_FILE}"
    
    # Diagnostic logs configuration - Reader accessible
    echo "    Getting diagnostic logs configuration..."
    DIAG_LOGS=$(az webapp log config show --name "${APP_NAME}" --resource-group "${RG}" -o json 2>/dev/null || echo '{}')
    echo "    \"diagnosticLogs\": ${DIAG_LOGS}," >> "${DATA_FILE}"
    
    # Custom domains - Reader accessible
    echo "    Getting custom domains..."
    DOMAINS=$(az webapp config hostname list --webapp-name "${APP_NAME}" --resource-group "${RG}" -o json 2>/dev/null || echo '[]')
    echo "    \"customDomains\": ${DOMAINS}," >> "${DATA_FILE}"
    
    # SSL bindings - Reader accessible
    echo "    Getting SSL certificates..."
    SSL_BINDINGS=$(az webapp config ssl list --resource-group "${RG}" -o json 2>/dev/null | jq "[.[] | select(.serverFarmId == \"${PLAN_ID}\")]" || echo '[]')
    echo "    \"sslCertificates\": ${SSL_BINDINGS}," >> "${DATA_FILE}"
    
    # Deployment slots - Reader accessible
    echo "    Getting deployment slots..."
    SLOTS=$(az webapp deployment slot list --name "${APP_NAME}" --resource-group "${RG}" -o json 2>/dev/null || echo '[]')
    echo "    \"deploymentSlots\": ${SLOTS}," >> "${DATA_FILE}"
    
    # Identity/Managed Identity - Reader accessible
    echo "    Getting managed identity..."
    IDENTITY=$(az webapp identity show --name "${APP_NAME}" --resource-group "${RG}" -o json 2>/dev/null)
    if [ -z "${IDENTITY}" ] || [ "${IDENTITY}" = "null" ]; then
        IDENTITY='{"type":"None"}'
    fi
    echo "    \"identity\": ${IDENTITY}," >> "${DATA_FILE}"
    
    # VNet integration - Reader accessible
    echo "    Getting VNet integration..."
    VNET=$(az webapp vnet-integration list --name "${APP_NAME}" --resource-group "${RG}" -o json 2>/dev/null || echo '[]')
    echo "    \"vnetIntegration\": ${VNET}," >> "${DATA_FILE}"
    
    # IP restrictions - Reader accessible
    echo "    Getting IP restrictions..."
    IP_RESTRICTIONS=$(az webapp config access-restriction show --name "${APP_NAME}" --resource-group "${RG}" -o json 2>/dev/null || echo '{}')
    echo "    \"ipRestrictions\": ${IP_RESTRICTIONS}" >> "${DATA_FILE}"
    
    echo "  }" >> "${DATA_FILE}"
    echo "    ✓ Completed"
    
    counter=$((counter + 1))
done

# Close JSON structure
echo "" >> "${DATA_FILE}"
echo "  ]" >> "${DATA_FILE}"
echo "}" >> "${DATA_FILE}"

echo ""
echo "==================================================="
echo "Data collection complete!"
echo "Output file: ${DATA_FILE}"
echo "==================================================="
echo ""
echo "Next steps:"
echo "  1. Analyze: python3 analyze-app-services.py ${DATA_FILE}"
echo "  2. Generate report after analysis"
