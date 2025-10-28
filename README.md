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
git clone <your-repo-url>
cd azure-appservice-assessment

# 2. Ensure you're logged into Azure
az login
az account set --subscription "<your-subscription-name>"

# 3. Run the assessment (takes 2-5 minutes)
./run-assessment.sh
```

That's it! The script will:
1. ✅ Collect App Service configurations  
2. ✅ Analyze against Microsoft best practices  
3. ✅ Generate interactive HTML and text reports  
4. ✅ Display summary statistics  
5. ✅ Open the report in your browser

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
├── README-Assessment.md                 # Detailed methodology & checks
├── QUICK-REFERENCE.md                   # Cheat sheet for common tasks
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

### Scenario 1: Quick Assessment (Most Common)

```bash
./run-assessment.sh
```

Opens HTML report automatically when complete.

### Scenario 2: Generate Report Only (Already Have Data)

```bash
# If you already collected data and just want to regenerate reports
python3 generate-report.py app-service-assessment/findings-*.json
python3 generate-summary.py app-service-assessment/findings-*.json
```

### Scenario 3: Step-by-Step (For Troubleshooting)

```bash
# 1. Collect data
./assess-app-services-reader.sh

# 2. Analyze
python3 analyze-app-services.py app-service-assessment/app-services-data-*.json

# 3. Generate reports
python3 generate-report.py app-service-assessment/findings-*.json
python3 generate-summary.py app-service-assessment/findings-*.json
```

## 📖 Documentation

| Document | Purpose | When to Use |
|----------|---------|-------------|
| `README.md` | Main documentation & quick start | Start here |
| `README-Assessment.md` | Detailed methodology & checks | Understanding what's assessed |
| `QUICK-REFERENCE.md` | Command cheat sheet | During remediation |
| Generated in output folder: |||
| `assessment-report-*.html` | Interactive findings report | Reviewing & presenting findings |
| `EXECUTIVE-SUMMARY.md` | Business-level summary | Sharing with leadership |
| `REMEDIATION-GUIDE.md` | Copy-paste fix commands | Implementing fixes |
| `TALK-TRACK.md` | Presentation guide | Customer meetings |

## 🔧 Remediation Workflow

After running the assessment:

1. **Review** the HTML report (`open app-service-assessment/assessment-report-*.html`)
2. **Share** `EXECUTIVE-SUMMARY.md` with leadership
3. **Use** `REMEDIATION-GUIDE.md` for exact fix commands
4. **Present** findings using `TALK-TRACK.md` as a guide
5. **Re-assess** after fixes to track improvement

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
- **Questions**: Review the detailed `README-Assessment.md`
- **Issues**: Check that you have Reader access to the subscription

## 📜 License

This is an assessment toolkit based on publicly documented Microsoft best practices.

---

## 🤝 Contributing

Contributions are welcome! This toolkit can be extended with additional checks or improved reporting.

### Adding New Checks

1. Edit `analyze-app-services.py`
2. Add a new method to the `AppServiceAnalyzer` class
3. Call it from the `analyze()` method
4. Test with sample data

### Improving Reports

- HTML template: Edit `HTML_TEMPLATE` in `generate-report.py`
- Text summary: Modify `generate-summary.py`

---

## 🌟 Star This Repo

If this toolkit helped you improve your Azure security posture, please star the repository!

---

**Ready to assess?** Just run: `./run-assessment.sh`

**Questions?** Check `README-Assessment.md` or `QUICK-REFERENCE.md`
