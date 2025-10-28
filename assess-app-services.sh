#!/bin/bash

# Azure App Service Assessment Script
# This script collects App Service configuration data for best practices review
# Requires: Azure CLI with reader access to the subscription

set -e

# Output directory for collected data
OUTPUT_DIR="./app-service-assessment"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
DATA_FILE="${OUTPUT_DIR}/app-services-data-${TIMESTAMP}.json"

# Create output directory
mkdir -p "${OUTPUT_DIR}"

echo "==================================================="
echo "Azure App Service Assessment Data Collection"
echo "==================================================="
echo ""

# Get current subscription
SUBSCRIPTION=$(az account show --query name -o tsv)
SUBSCRIPTION_ID=$(az account show --query id -o tsv)

echo "Subscription: ${SUBSCRIPTION}"
echo "Subscription ID: ${SUBSCRIPTION_ID}"
echo ""

# Initialize JSON structure
echo "{" > "${DATA_FILE}"
echo "  \"subscription\": \"${SUBSCRIPTION}\"," >> "${DATA_FILE}"
echo "  \"subscriptionId\": \"${SUBSCRIPTION_ID}\"," >> "${DATA_FILE}"
echo "  \"assessmentDate\": \"$(date -u +"%Y-%m-%dT%H:%M:%SZ")\"," >> "${DATA_FILE}"
echo "  \"appServices\": [" >> "${DATA_FILE}"

# Get list of all App Services
echo "Collecting App Service data..."
APP_SERVICES=$(az webapp list --query "[].{name:name, resourceGroup:resourceGroup, id:id}" -o json)

# Check if there are any App Services
APP_SERVICE_COUNT=$(echo "${APP_SERVICES}" | jq '. | length')
echo "Found ${APP_SERVICE_COUNT} App Service(s)"
echo ""

if [ "${APP_SERVICE_COUNT}" -eq 0 ]; then
    echo "  ]" >> "${DATA_FILE}"
    echo "}" >> "${DATA_FILE}"
    echo "No App Services found in subscription."
    exit 0
fi

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
    
    # Get detailed App Service configuration
    echo "  {" >> "${DATA_FILE}"
    echo "    \"name\": \"${APP_NAME}\"," >> "${DATA_FILE}"
    echo "    \"resourceGroup\": \"${RG}\"," >> "${DATA_FILE}"
    
    # Basic configuration
    CONFIG=$(az webapp show --name "${APP_NAME}" --resource-group "${RG}" -o json)
    echo "    \"config\": ${CONFIG}," >> "${DATA_FILE}"
    
    # App Service Plan details
    PLAN_ID=$(echo "${CONFIG}" | jq -r '.serverFarmId')
    PLAN_NAME=$(echo "${PLAN_ID}" | awk -F'/' '{print $NF}')
    PLAN_RG=$(echo "${PLAN_ID}" | awk -F'/' '{print $5}')
    
    PLAN=$(az appservice plan show --name "${PLAN_NAME}" --resource-group "${PLAN_RG}" -o json 2>/dev/null || echo '{}')
    echo "    \"appServicePlan\": ${PLAN}," >> "${DATA_FILE}"
    
    # Runtime configuration
    RUNTIME_CONFIG=$(az webapp config show --name "${APP_NAME}" --resource-group "${RG}" -o json 2>/dev/null || echo '{}')
    echo "    \"runtimeConfig\": ${RUNTIME_CONFIG}," >> "${DATA_FILE}"
    
    # App Settings (without values for security) - may require contributor access
    APP_SETTINGS=$(az webapp config appsettings list --name "${APP_NAME}" --resource-group "${RG}" --query "[].{name:name}" -o json 2>/dev/null || echo '[]')
    echo "    \"appSettingKeys\": ${APP_SETTINGS}," >> "${DATA_FILE}"
    
    # Connection strings (names only, no values) - may require contributor access
    CONN_STRINGS=$(az webapp config connection-string list --name "${APP_NAME}" --resource-group "${RG}" --query "keys(@)" -o json 2>/dev/null || echo '[]')
    echo "    \"connectionStringKeys\": ${CONN_STRINGS}," >> "${DATA_FILE}"
    
    # Auth settings
    AUTH=$(az webapp auth show --name "${APP_NAME}" --resource-group "${RG}" -o json 2>/dev/null || echo '{}')
    echo "    \"authConfig\": ${AUTH}," >> "${DATA_FILE}"
    
    # TLS/SSL configuration
    TLS=$(az webapp config show --name "${APP_NAME}" --resource-group "${RG}" --query "{minTlsVersion:minTlsVersion, http20Enabled:http20Enabled, ftpsState:ftpsState, alwaysOn:alwaysOn, webSocketsEnabled:webSocketsEnabled, remoteDebuggingEnabled:remoteDebuggingEnabled}" -o json 2>/dev/null || echo '{}')
    echo "    \"tlsConfig\": ${TLS}," >> "${DATA_FILE}"
    
    # Diagnostic logs configuration
    DIAG_LOGS=$(az webapp log config show --name "${APP_NAME}" --resource-group "${RG}" -o json 2>/dev/null || echo '{}')
    echo "    \"diagnosticLogs\": ${DIAG_LOGS}," >> "${DATA_FILE}"
    
    # Backup configuration
    BACKUP=$(az webapp config backup list --webapp-name "${APP_NAME}" --resource-group "${RG}" -o json 2>/dev/null || echo '[]')
    echo "    \"backupConfig\": ${BACKUP}," >> "${DATA_FILE}"
    
    # Custom domains
    DOMAINS=$(az webapp config hostname list --webapp-name "${APP_NAME}" --resource-group "${RG}" -o json 2>/dev/null || echo '[]')
    echo "    \"customDomains\": ${DOMAINS}," >> "${DATA_FILE}"
    
    # SSL bindings
    SSL_BINDINGS=$(az webapp config ssl list --resource-group "${RG}" -o json 2>/dev/null || echo '[]')
    echo "    \"sslCertificates\": ${SSL_BINDINGS}," >> "${DATA_FILE}"
    
    # Deployment slots
    SLOTS=$(az webapp deployment slot list --name "${APP_NAME}" --resource-group "${RG}" -o json 2>/dev/null || echo '[]')
    echo "    \"deploymentSlots\": ${SLOTS}," >> "${DATA_FILE}"
    
    # Identity/Managed Identity
    IDENTITY=$(az webapp identity show --name "${APP_NAME}" --resource-group "${RG}" -o json 2>/dev/null || echo '{}')
    echo "    \"identity\": ${IDENTITY}," >> "${DATA_FILE}"
    
    # VNet integration
    VNET=$(az webapp vnet-integration list --name "${APP_NAME}" --resource-group "${RG}" -o json 2>/dev/null || echo '[]')
    echo "    \"vnetIntegration\": ${VNET}," >> "${DATA_FILE}"
    
    # IP restrictions
    IP_RESTRICTIONS=$(az webapp config access-restriction show --name "${APP_NAME}" --resource-group "${RG}" -o json 2>/dev/null || echo '{}')
    echo "    \"ipRestrictions\": ${IP_RESTRICTIONS}" >> "${DATA_FILE}"
    
    echo "  }" >> "${DATA_FILE}"
    
    counter=$((counter + 1))
done

# Close JSON structure
echo "  ]" >> "${DATA_FILE}"
echo "}" >> "${DATA_FILE}"

echo ""
echo "==================================================="
echo "Data collection complete!"
echo "Output file: ${DATA_FILE}"
echo "==================================================="
