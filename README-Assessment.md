# Azure App Service Assessment

This toolkit helps you assess Azure App Services against Microsoft best practices and generate comprehensive reports.

## Quick Start

**For the fastest assessment, just run:**

```bash
./run-assessment.sh
```

This single command will:
1. ✅ Collect all App Service configurations
2. ✅ Analyze against Microsoft best practices  
3. ✅ Generate HTML and text reports
4. ✅ Display summary statistics

## Prerequisites

- Azure CLI installed and configured
- Reader access to the Azure subscription
- Python 3.6 or higher
- Bash shell (macOS/Linux) or Git Bash (Windows)

## Scripts

1. **assess-app-services.sh** - Collects App Service configuration data
2. **analyze-app-services.py** - Analyzes data against best practices
3. **generate-report.py** - Generates HTML report with findings

## Usage

### Step 1: Set Your Azure Subscription

```bash
# List available subscriptions
az account list --output table

# Set the subscription you want to assess
az account set --subscription "<subscription-id-or-name>"

# Verify the current subscription
az account show
```

### Step 2: Collect App Service Data

```bash
# Make the script executable
chmod +x assess-app-services.sh

# Run the data collection
./assess-app-services.sh
```

This will create a directory `app-service-assessment/` with a JSON file containing all App Service configurations.

### Step 3: Analyze Against Best Practices

```bash
# Run the analysis on the collected data
python3 analyze-app-services.py app-service-assessment/app-services-data-*.json
```

This will generate a `findings-*.json` file with all identified issues.

### Step 4: Generate HTML Report

```bash
# Generate the HTML report
python3 generate-report.py app-service-assessment/findings-*.json
```

This creates an HTML report that you can open in any browser.

### Step 5: View the Report

```bash
# Open in default browser (macOS)
open app-service-assessment/assessment-report-*.html

# Or specify the browser
open -a "Google Chrome" app-service-assessment/assessment-report-*.html
```

## What Gets Assessed

The assessment checks for the following best practices:

### Security
- ✅ Minimum TLS version (1.2+)
- ✅ HTTPS-only enforcement
- ✅ Managed Identity usage
- ✅ Remote debugging disabled
- ✅ FTPS enforcement
- ✅ Client certificate configuration
- ✅ IP restrictions
- ✅ VNet integration
- ✅ Authentication/authorization
- ✅ Custom domain SSL certificates
- ✅ Runtime version currency
- ✅ CORS configuration

### Performance
- ✅ Always On enabled
- ✅ HTTP/2 enabled
- ✅ Auto-scaling configuration

### Reliability
- ✅ App Service Plan tier (production-ready)
- ✅ Instance count (redundancy)
- ✅ Zone redundancy
- ✅ Health check configuration
- ✅ Auto-heal settings
- ✅ Backup configuration

### Monitoring
- ✅ Diagnostic logging enabled
- ✅ Application Insights integration

### DevOps
- ✅ Deployment slots (staging)
- ✅ Deployment best practices

## Severity Levels

- **Critical**: Security vulnerabilities or compliance issues requiring immediate attention
- **High**: Significant risks to security, availability, or performance
- **Medium**: Important improvements for production readiness
- **Low**: Recommendations for optimization and best practices

## Output Files

All files are saved in the `app-service-assessment/` directory:

- `app-services-data-*.json` - Raw configuration data
- `findings-*.json` - Analysis results in JSON format
- `assessment-report-*.html` - Final HTML report

## Sample Commands

### Quick Assessment (All Steps)

```bash
# Set subscription
az account set --subscription "your-subscription-name"

# Run all steps
chmod +x assess-app-services.sh
./assess-app-services.sh

# Get the latest data file
DATA_FILE=$(ls -t app-service-assessment/app-services-data-*.json | head -1)

# Analyze
python3 analyze-app-services.py "$DATA_FILE"

# Get the latest findings file
FINDINGS_FILE=$(ls -t app-service-assessment/findings-*.json | head -1)

# Generate report
python3 generate-report.py "$FINDINGS_FILE"

# Open report
REPORT_FILE=$(ls -t app-service-assessment/assessment-report-*.html | head -1)
open "$REPORT_FILE"
```

### Assessment for Specific Resource Group

Modify `assess-app-services.sh` to filter by resource group:

```bash
# Instead of:
APP_SERVICES=$(az webapp list --query "[].{name:name, resourceGroup:resourceGroup, id:id}" -o json)

# Use:
APP_SERVICES=$(az webapp list --resource-group "your-rg-name" --query "[].{name:name, resourceGroup:resourceGroup, id:id}" -o json)
```

## Troubleshooting

### Permission Issues

If you get permission errors:
```bash
chmod +x assess-app-services.sh
chmod +x analyze-app-services.py
chmod +x generate-report.py
```

### Azure CLI Not Logged In

```bash
az login
az account list
az account set --subscription "your-subscription"
```

### No App Services Found

Verify you have the correct subscription set:
```bash
az account show
az webapp list --output table
```

### Python Dependencies

If you encounter import errors, ensure Python 3 is installed:
```bash
python3 --version
```

## Customization

### Add Custom Checks

Edit `analyze-app-services.py` and add new check methods to the `AppServiceAnalyzer` class:

```python
def check_custom_setting(self, app: Dict):
    """Check custom configuration"""
    app_name = app.get("name")
    # Your custom logic here
    if condition_not_met:
        self.findings.append(Finding(
            app_name=app_name,
            category="Custom",
            severity=Finding.MEDIUM,
            title="Your check title",
            description="Description",
            recommendation="What to do",
            reference="https://docs.microsoft.com/..."
        ))
```

Then call it in the `analyze()` method.

### Modify Report Styling

Edit the CSS in `generate-report.py` within the `HTML_TEMPLATE` variable.

## References

- [Azure App Service Best Practices](https://learn.microsoft.com/en-us/azure/app-service/app-service-best-practices)
- [Azure App Service Security](https://learn.microsoft.com/en-us/azure/app-service/overview-security)
- [Azure Well-Architected Framework](https://learn.microsoft.com/en-us/azure/architecture/framework/)

## Support

For issues or questions about this assessment toolkit, please refer to Microsoft documentation or consult with your Azure support team.
