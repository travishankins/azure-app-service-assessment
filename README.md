# Azure App Service Assessment Toolkit

> Automated security and best practices assessment for Azure App Services with comprehensive reporting

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Shell](https://img.shields.io/badge/Shell-Bash-green.svg)](https://www.gnu.org/software/bash/)
[![Python](https://img.shields.io/badge/Python-3.6+-blue.svg)](https://www.python.org/)

Assess your Azure App Services against Microsoft's best practices across **Security**, **Reliability**, **Performance**, and **Monitoring** dimensions. Get actionable recommendations with exact remediation commands.

## ✨ Features

- 🔍 **52+ Best Practice Checks** across 4 categories
- 📊 **Beautiful HTML Reports** with interactive navigation
- 🎯 **Severity-Based Findings** (Critical, High, Medium, Low)
- 💰 **Cost-Aware Recommendations** with ROI guidance
- 📋 **Copy-Paste Remediation Commands** ready to execute
- 🔐 **Reader-Access Compatible** - no changes to your environment
- 📈 **Progress Tracking** - re-assess to measure improvement

## 🚀 Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/travishankins/azure-app-service-assessment.git
cd azure-app-service-assessment

# 2. Ensure you're logged into Azure
az login
az account set --subscription "<your-subscription-name>"

# 3. Run the complete assessment (takes 2-5 minutes)
./run-assessment.sh
```

### What Happens Automatically

The `run-assessment.sh` script orchestrates everything for you:

1. **📥 Data Collection** (~1-3 min)
   - Scans all App Services in your subscription
   - Collects configuration details using Azure CLI
   - Saves raw data to `app-service-assessment/app-services-data-*.json`

2. **🔍 Analysis** (~10-30 sec)
   - Evaluates each App Service against 52+ best practice checks
   - Categorizes findings by severity (Critical, High, Medium, Low)
   - Saves analysis to `app-service-assessment/findings-*.json`

3. **📊 Report Generation** (~5-10 sec)
   - **Automatically creates** all reports - you don't need to run anything else!
   - Generates interactive HTML report (`assessment-report-*.html`)
   - Creates text summary (`assessment-summary-*.txt`)
   - Produces executive summary (`EXECUTIVE-SUMMARY.md`)
   - Generates remediation guide (`REMEDIATION-GUIDE.md`)
   - Creates presentation materials (`TALK-TRACK.md`, `INDEX.md`)

4. **✅ Completion**
   - Displays summary statistics in terminal
   - Automatically opens HTML report in your default browser
   - All reports ready to share with stakeholders

**You don't need to run any additional commands** - everything is generated automatically!

## 📋 Prerequisites

- **Azure CLI** ([Install](https://docs.microsoft.com/cli/azure/install-azure-cli))
- **Python 3.6+** (comes with macOS/most Linux distros)
- **jq** - JSON processor (`brew install jq` on macOS, `apt-get install jq` on Linux)
- **Bash** - Shell environment (default on macOS/Linux)
- **Azure Subscription Access** - Reader role minimum (no write permissions needed)

## 📁 Project Structure

```
.
├── run-assessment.sh                    # ⭐ Master script - run this first!
├── assess-app-services-reader.sh        # Data collection (reader-access optimized)
├── assess-app-services.sh               # Data collection (contributor-access)
├── analyze-app-services.py              # Best practices analysis engine
├── generate-report.py                   # HTML report generator
├── generate-summary.py                  # Text summary generator
├── README.md                            # Main documentation (you are here)
├── QUICK-REFERENCE.md                   # Cheat sheet for common tasks
├── docs/
│   └── methodology.md                   # Checks, severity levels & customization
├── .gitignore                           # Git ignore patterns
└── app-service-assessment/              # 📁 Output directory (auto-created)
    ├── assessment-report-*.html         # ⭐ Interactive HTML report
    ├── assessment-summary-*.txt         # Text summary
    ├── findings-*.json                  # Machine-readable findings
    ├── app-services-data-*.json         # Raw Azure configuration data
    ├── EXECUTIVE-SUMMARY.md             # Generated summary for leadership
    ├── REMEDIATION-GUIDE.md             # Generated fix commands
    ├── TALK-TRACK.md                    # Presentation guide
    └── INDEX.md                         # Package overview
```

**Note:** The `app-service-assessment/` directory is created automatically when you run the assessment.

## 📊 What Gets Assessed

The toolkit evaluates App Services across 4 dimensions:

### 🔐 Security (28 checks)
- TLS/SSL configuration
- HTTPS enforcement
- Managed Identity
- IP restrictions
- Authentication settings
- VNet integration
- Runtime versions

### 💪 Reliability (12 checks)
- Instance redundancy
- Health checks
- Auto-heal settings
- Backup configuration
- Deployment slots
- Zone redundancy

### 📈 Performance (6 checks)
- Always On settings
- HTTP/2 enablement
- Auto-scaling configuration

### 📊 Monitoring (6 checks)
- Diagnostic logging
- Application Insights integration

## 🎯 Usage Scenarios

### Scenario 1: Complete Assessment (Recommended - Fully Automated)

```bash
./run-assessment.sh
```

**This single command does everything:**
- ✅ Collects all App Service configurations
- ✅ Analyzes against best practices
- ✅ **Generates ALL reports automatically** (HTML, text, markdown)
- ✅ Opens HTML report in your browser
- ✅ No additional commands needed!

**Reports Created Automatically:**
- `assessment-report-*.html` - Interactive HTML report
- `assessment-summary-*.txt` - Quick text summary
- `EXECUTIVE-SUMMARY.md` - Business-level overview
- `REMEDIATION-GUIDE.md` - Copy-paste fix commands
- `TALK-TRACK.md` - Presentation guide
- `INDEX.md` - Package overview

### Scenario 2: Regenerate Reports Only (Already Have Analysis Data)

If you want to regenerate reports with different formatting but already have findings:

```bash
# Regenerate just the HTML and text reports
python3 generate-report.py app-service-assessment/findings-*.json
python3 generate-summary.py app-service-assessment/findings-*.json

# Regenerate just the documentation
python3 generate-docs.py app-service-assessment/findings-*.json app-service-assessment/app-services-data-*.json
```

### Scenario 3: Manual Step-by-Step (For Troubleshooting or Custom Workflows)

If you need granular control or debugging:

```bash
# 1. Collect data only
./assess-app-services-reader.sh

# 2. Analyze data only
python3 analyze-app-services.py app-service-assessment/app-services-data-*.json

# 3. Generate all reports manually
python3 generate-report.py app-service-assessment/findings-*.json
python3 generate-summary.py app-service-assessment/findings-*.json
python3 generate-docs.py app-service-assessment/findings-*.json app-service-assessment/app-services-data-*.json
```

**💡 Tip:** For most users, Scenario 1 (just running `./run-assessment.sh`) is all you need!

## 📖 Documentation

| Document | Purpose | When to Use |
|----------|---------|-------------|
| `README.md` | Main documentation & quick start | Start here |
| `docs/methodology.md` | Checks, severity levels & customization | Understanding what's assessed |
| `QUICK-REFERENCE.md` | Command cheat sheet | During remediation |
| Generated in output folder: |||
| `assessment-report-*.html` | Interactive findings report | Reviewing & presenting findings |
| `EXECUTIVE-SUMMARY.md` | Business-level summary | Sharing with leadership |
| `REMEDIATION-GUIDE.md` | Copy-paste fix commands | Implementing fixes |
| `TALK-TRACK.md` | Presentation guide | Customer meetings |

## 🔧 Remediation Workflow

After running `./run-assessment.sh`, all reports are **automatically created** in the `app-service-assessment/` directory:

1. **Review Findings**
   ```bash
   # HTML report opens automatically, or manually open:
   open app-service-assessment/assessment-report-*.html
   ```

2. **Share with Leadership**
   ```bash
   # Email or share the executive summary
   cat app-service-assessment/EXECUTIVE-SUMMARY.md
   ```

3. **Implement Fixes**
   ```bash
   # Use the remediation guide with copy-paste commands
   cat app-service-assessment/REMEDIATION-GUIDE.md
   ```

4. **Present to Stakeholders**
   ```bash
   # Follow the talk track for customer meetings
   cat app-service-assessment/TALK-TRACK.md
   ```

5. **Re-assess After Fixes**
   ```bash
   # Run again to verify improvements
   ./run-assessment.sh
   ```

**All documentation is generated automatically** - no manual report creation needed!

## 💡 Example Output

```
Quick Summary:
  🔴 Critical: 6
  🟠 High:     6
  🟡 Medium:   22
  🔵 Low:      18
  ━━━━━━━━━━━━━━━
  📊 Total:    52
```

Common findings:
- ❌ TLS 1.2 not enforced
- ❌ HTTPS-only not enabled
- ❌ No IP restrictions
- ❌ Diagnostic logging disabled
- ❌ Single instance (no redundancy)

All with specific remediation steps!

## 🔄 Re-Assessment

To track improvement after remediation:

```bash
# Run assessment again
./run-assessment.sh

# Compare findings count before/after
```

**Recommended schedule:**
- After critical fixes: Immediate re-assessment
- Ongoing: Monthly or quarterly

## ⚙️ Troubleshooting

### "Azure CLI not found"
```bash
# Install Azure CLI
brew install azure-cli  # macOS
# Or follow: https://docs.microsoft.com/cli/azure/install-azure-cli
```

### "Not logged into Azure"
```bash
az login
az account set --subscription "<subscription-name-or-id>"
az account show  # Verify
```

### "jq: command not found"
```bash
brew install jq  # macOS
# Or: sudo apt-get install jq  # Linux
```

### "Permission denied"
```bash
chmod +x *.sh  # Make scripts executable
```

## 🤝 Support

- **Microsoft Documentation**: [Azure App Service Best Practices](https://learn.microsoft.com/en-us/azure/app-service/app-service-best-practices)
- **Questions**: Review [`docs/methodology.md`](docs/methodology.md)
- **Issues**: Check that you have Reader access to the subscription

## 🤝 Contributing

Contributions are welcome — see [CONTRIBUTING.md](CONTRIBUTING.md). This toolkit can be
extended with additional checks or improved reporting.

## ⚖️ License

Released under the [MIT License](LICENSE). The checks are based on publicly
documented Microsoft best practices.
