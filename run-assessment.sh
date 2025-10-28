#!/bin/bash

# Master script to run complete Azure App Service Assessment
# Usage: ./run-assessment.sh

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║   Azure App Service Security & Best Practices Assessment      ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Check prerequisites
echo "Checking prerequisites..."
if ! command -v az &> /dev/null; then
    echo "❌ Azure CLI not found. Please install it first."
    exit 1
fi

if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install it first."
    exit 1
fi

if ! command -v jq &> /dev/null; then
    echo "❌ jq not found. Please install it first (brew install jq)."
    exit 1
fi

echo "✅ All prerequisites met"
echo ""

# Verify Azure login
echo "Verifying Azure login..."
if ! az account show &> /dev/null; then
    echo "❌ Not logged into Azure. Please run: az login"
    exit 1
fi

SUBSCRIPTION=$(az account show --query name -o tsv)
echo "✅ Logged in to subscription: ${SUBSCRIPTION}"
echo ""

# Confirm before proceeding
echo "This assessment will:"
echo "  1. Collect App Service configurations (read-only)"
echo "  2. Analyze against Microsoft best practices"
echo "  3. Generate reports (HTML and text)"
echo ""
read -p "Continue with assessment? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Assessment cancelled."
    exit 0
fi

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "STEP 1/4: Collecting App Service Data"
echo "═══════════════════════════════════════════════════════════════"
"${SCRIPT_DIR}/assess-app-services-reader.sh"

# Find the latest data file
DATA_FILE=$(ls -t "${SCRIPT_DIR}/app-service-assessment/app-services-data-"*.json 2>/dev/null | head -1)

if [ -z "${DATA_FILE}" ]; then
    echo "❌ No data file found. Collection may have failed."
    exit 1
fi

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "STEP 2/4: Analyzing Against Best Practices"
echo "═══════════════════════════════════════════════════════════════"
python3 "${SCRIPT_DIR}/analyze-app-services.py" "${DATA_FILE}"

# Find the latest findings file
FINDINGS_FILE=$(ls -t "${SCRIPT_DIR}/app-service-assessment/findings-"*.json 2>/dev/null | head -1)

if [ -z "${FINDINGS_FILE}" ]; then
    echo "❌ No findings file found. Analysis may have failed."
    exit 1
fi

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "STEP 3/4: Generating HTML Report"
echo "═══════════════════════════════════════════════════════════════"
python3 "${SCRIPT_DIR}/generate-report.py" "${FINDINGS_FILE}"

# Find the latest report file
REPORT_FILE=$(ls -t "${SCRIPT_DIR}/app-service-assessment/assessment-report-"*.html 2>/dev/null | head -1)

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "STEP 4/5: Generating Text Summary"
echo "═══════════════════════════════════════════════════════════════"
python3 "${SCRIPT_DIR}/generate-summary.py" "${FINDINGS_FILE}"

SUMMARY_FILE=$(ls -t "${SCRIPT_DIR}/app-service-assessment/assessment-summary-"*.txt 2>/dev/null | head -1)

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "STEP 5/5: Generating Documentation"
echo "═══════════════════════════════════════════════════════════════"
python3 "${SCRIPT_DIR}/generate-docs.py" "${FINDINGS_FILE}" "${DATA_FILE}"

echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║                  ASSESSMENT COMPLETE!                          ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""
echo "Generated Files:"
echo "  📊 HTML Report: ${REPORT_FILE}"
echo "  📄 Text Summary: ${SUMMARY_FILE}"
echo "  🔍 Findings (JSON): ${FINDINGS_FILE}"
echo "  💾 Raw Data (JSON): ${DATA_FILE}"
echo ""
echo "Quick View:"
echo "  View HTML Report:  open ${REPORT_FILE}"
echo "  View Summary:      cat ${SUMMARY_FILE}"
echo ""

# Ask if user wants to open the report
read -p "Open HTML report in browser now? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    open "${REPORT_FILE}"
fi

# Show quick stats
CRITICAL=$(jq '.findingsBySeverity.Critical' "${FINDINGS_FILE}")
HIGH=$(jq '.findingsBySeverity.High' "${FINDINGS_FILE}")
MEDIUM=$(jq '.findingsBySeverity.Medium' "${FINDINGS_FILE}")
LOW=$(jq '.findingsBySeverity.Low' "${FINDINGS_FILE}")
TOTAL=$(jq '.totalFindings' "${FINDINGS_FILE}")

echo ""
echo "Quick Summary:"
echo "  🔴 Critical: ${CRITICAL}"
echo "  🟠 High:     ${HIGH}"
echo "  🟡 Medium:   ${MEDIUM}"
echo "  🔵 Low:      ${LOW}"
echo "  ━━━━━━━━━━━━━━━"
echo "  📊 Total:    ${TOTAL}"
echo ""
echo "Next Steps:"
echo "  1. Review the HTML report for detailed findings"
echo "  2. Prioritize Critical and High severity issues"
echo "  3. Create remediation plan with your team"
echo "  4. Share reports with stakeholders"
echo ""
