# 📋 Quick Reference Card

## Assessment Workflow

```
┌─────────────────────────────────────────────────────────┐
│  STEP 1: Run Assessment                                 │
│  $ ./run-assessment.sh                                  │
│  ⏱️  Takes: 2-5 minutes                                  │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│  STEP 2: Review HTML Report                             │
│  $ open app-service-assessment/assessment-report-*.html │
│  👀 Interactive report with all findings                │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│  STEP 3: Share with Stakeholders                        │
│  📊 Leadership: EXECUTIVE-SUMMARY.md                    │
│  🔧 DevOps: REMEDIATION-GUIDE.md                        │
│  🎤 Presentation: TALK-TRACK.md                         │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│  STEP 4: Apply Fixes                                    │
│  Follow commands in REMEDIATION-GUIDE.md                │
│  Start with Critical → High → Medium → Low              │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│  STEP 5: Re-Assess                                      │
│  $ ./run-assessment.sh                                  │
│  ✅ Track improvement                                   │
└─────────────────────────────────────────────────────────┘
```

---

## Key Files & Their Purpose

| What You Need | File | Location |
|---------------|------|----------|
| **Run assessment** | `run-assessment.sh` | Root |
| **Full report** | `assessment-report-*.html` | `app-service-assessment/` |
| **Quick summary** | `assessment-summary-*.txt` | `app-service-assessment/` |
| **For executives** | `EXECUTIVE-SUMMARY.md` | `app-service-assessment/` |
| **Fix commands** | `REMEDIATION-GUIDE.md` | `app-service-assessment/` |
| **Present findings** | `TALK-TRACK.md` | `app-service-assessment/` |
| **Package overview** | `INDEX.md` | `app-service-assessment/` |
| **Detailed docs** | `README-Assessment.md` | Root |

---

## One-Liners

### View Latest HTML Report
```bash
open app-service-assessment/assessment-report-*.html
```

### View Text Summary
```bash
cat app-service-assessment/assessment-summary-*.txt
```

### View Finding Count
```bash
jq '.totalFindings, .findingsBySeverity' app-service-assessment/findings-*.json
```

### Export for Email
```bash
# Copy files for sharing
cp app-service-assessment/assessment-report-*.html ~/Desktop/
cp app-service-assessment/EXECUTIVE-SUMMARY.md ~/Desktop/
```

---

## Typical Finding Distribution

Based on this assessment:

```
Total: 52 findings across 6 App Services

🔴 Critical (6)  - TLS 1.2 not configured
🟠 High (6)      - HTTPS-only not enforced
🟡 Medium (22)   - IP restrictions, logging, managed identity
🔵 Low (18)      - HTTP/2, deployment slots, optimizations
```

---

## Fix Timeline Template

| Priority | Timeline | Effort | Cost |
|----------|----------|--------|------|
| 🔴 Critical | 24-48 hours | 30 min | $0 |
| 🟠 High | 1 week | 30 min | $0 |
| 🟡 Medium | 2-4 weeks | 2-4 hours | $0-50/mo |
| 🔵 Low | 1-3 months | 1-2 days | $0-100/mo |

---

## Common Commands

### Azure Setup
```bash
# Login
az login

# Set subscription
az account set --subscription "subscription-name"

# Verify
az account show
```

### Re-run Assessment
```bash
./run-assessment.sh
```

### Manual Steps
```bash
# 1. Collect data only
./assess-app-services-reader.sh

# 2. Analyze only
python3 analyze-app-services.py app-service-assessment/app-services-data-*.json

# 3. Generate reports only
python3 generate-report.py app-service-assessment/findings-*.json
python3 generate-summary.py app-service-assessment/findings-*.json
```

---

## Critical Fixes (Copy-Paste Ready)

### Set TLS 1.2 on All Services
```bash
# Set these based on your environment
declare -A apps=(
  ["app-example-webapp-001"]="rg-example-001"
  ["app-example-webapp-002"]="rg-example-001"
  ["app-example-api-001"]="rg-example-002"
  ["app-example-frontend-001"]="rg-example-003"
  ["app-example-backend-001"]="rg-example-003"
  ["app-example-service-001"]="rg-example-004"
)

for app in "${!apps[@]}"; do
  rg="${apps[$app]}"
  echo "Setting TLS 1.2 for $app..."
  az webapp config set --resource-group "$rg" --name "$app" --min-tls-version 1.2
done
```

### Enable HTTPS-Only on All Services
```bash
for app in "${!apps[@]}"; do
  rg="${apps[$app]}"
  echo "Enabling HTTPS-only for $app..."
  az webapp update --resource-group "$rg" --name "$app" --https-only true
done
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Script won't run | `chmod +x *.sh` |
| Azure not logged in | `az login` |
| jq not found | `brew install jq` |
| Python error | Ensure Python 3.6+ installed |
| Permission errors | Verify Reader access to subscription |
| JSON parse error | Re-run data collection |

---

## Support Resources

- **Microsoft Best Practices**: https://learn.microsoft.com/azure/app-service/
- **Detailed Documentation**: See `README-Assessment.md`
- **Package Overview**: See `app-service-assessment/INDEX.md`

---

## Quick Presentation Prep

**15 minutes before customer meeting:**

1. ✅ Open `app-service-assessment/TALK-TRACK.md`
2. ✅ Open `app-service-assessment/assessment-report-*.html`
3. ✅ Review `app-service-assessment/EXECUTIVE-SUMMARY.md`
4. ✅ Have `app-service-assessment/REMEDIATION-GUIDE.md` ready

**During meeting:**
- Follow talk track flow
- Navigate HTML report together
- Answer questions using remediation guide
- Share executive summary afterward

---

**Keep this card handy for quick reference!**
