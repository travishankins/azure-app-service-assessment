#!/usr/bin/env python3
"""
Generate documentation files from assessment findings
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from collections import defaultdict

def generate_executive_summary(findings_file: Path, data_file: Path) -> str:
    """Generate executive summary document"""
    with open(findings_file, 'r') as f:
        findings_data = json.load(f)
    
    with open(data_file, 'r') as f:
        raw_data = json.load(f)
    
    app_services = raw_data.get('appServices', [])
    app_count = len(app_services)
    
    # Group findings by app
    apps = defaultdict(lambda: {"Critical": 0, "High": 0, "Medium": 0, "Low": 0})
    for finding in findings_data['findings']:
        apps[finding['appService']][finding['severity']] += 1
    
    content = f"""# Azure App Service Assessment - Executive Summary

**Subscription:** {findings_data.get('subscription', 'N/A')}  
**Assessment Date:** {findings_data.get('assessmentDate', 'N/A')}  
**App Services Assessed:** {app_count}  
**Total Findings:** {findings_data['totalFindings']}

---

## Executive Overview

This assessment evaluated **{app_count} Azure App Services** against Microsoft best practices across Security, Performance, Reliability, and Monitoring dimensions.

### Key Statistics

| Severity | Count | Percentage |
|----------|-------|------------|
| 🔴 **Critical** | {findings_data['findingsBySeverity']['Critical']} | {findings_data['findingsBySeverity']['Critical']/findings_data['totalFindings']*100:.1f}% |
| 🟠 **High** | {findings_data['findingsBySeverity']['High']} | {findings_data['findingsBySeverity']['High']/findings_data['totalFindings']*100:.1f}% |
| 🟡 **Medium** | {findings_data['findingsBySeverity']['Medium']} | {findings_data['findingsBySeverity']['Medium']/findings_data['totalFindings']*100:.1f}% |
| 🔵 **Low** | {findings_data['findingsBySeverity']['Low']} | {findings_data['findingsBySeverity']['Low']/findings_data['totalFindings']*100:.1f}% |

---

## Critical Findings (Immediate Action Required)

"""
    
    critical = [f for f in findings_data['findings'] if f['severity'] == 'Critical']
    if critical:
        # Group by title
        by_title = defaultdict(list)
        for f in critical:
            by_title[f['title']].append(f['appService'])
        
        for title, apps_list in by_title.items():
            content += f"### 🔴 {title}\n\n"
            content += f"**Affected Services:** {len(apps_list)} of {app_count}\n\n"
            example = next(f for f in critical if f['title'] == title)
            content += f"**Issue:** {example['description']}\n\n"
            content += f"**Recommendation:** {example['recommendation']}\n\n"
            content += f"**Priority:** IMMEDIATE (24-48 hours)\n\n"
    else:
        content += "✅ No critical findings!\n\n"
    
    content += """---

## High Priority Findings

"""
    
    high = [f for f in findings_data['findings'] if f['severity'] == 'High']
    if high:
        by_title = defaultdict(list)
        for f in high:
            by_title[f['title']].append(f['appService'])
        
        for title, apps_list in by_title.items():
            content += f"### 🟠 {title}\n\n"
            content += f"**Affected Services:** {len(apps_list)} of {app_count}\n\n"
            example = next(f for f in high if f['title'] == title)
            content += f"**Issue:** {example['description']}\n\n"
            content += f"**Priority:** HIGH (Within 1 week)\n\n"
    else:
        content += "✅ No high-priority findings!\n\n"
    
    content += """---

## Recommended Action Plan

### Phase 1: Immediate (This Week)
- Fix all Critical findings
- Cost: $0
- Effort: 30-60 minutes

### Phase 2: High Priority (Within 2 Weeks)
- Fix all High findings
- Cost: $0
- Effort: 1-2 hours

### Phase 3: Medium Priority (Within 30 Days)
- Address security hardening
- Enable monitoring and logging
- Cost: $0-100/month

---

## Next Steps

1. Review the complete HTML report for all findings
2. Share REMEDIATION-GUIDE.md with DevOps team
3. Schedule remediation work
4. Re-assess after fixes to measure improvement

---

**For detailed findings and remediation steps, see:**
- `assessment-report-*.html` - Full interactive report
- `REMEDIATION-GUIDE.md` - Exact fix commands
- `assessment-summary-*.txt` - Quick text overview
"""
    
    return content


def generate_remediation_guide(findings_file: Path, data_file: Path) -> str:
    """Generate remediation guide with exact commands"""
    with open(findings_file, 'r') as f:
        findings_data = json.load(f)
    
    with open(data_file, 'r') as f:
        raw_data = json.load(f)
    
    # Build app to resource group mapping
    app_rg_map = {}
    for app in raw_data.get('appServices', []):
        app_rg_map[app['name']] = app['resourceGroup']
    
    content = """# Azure App Service Remediation Guide

This guide provides exact commands to fix each finding category.

**Before you begin:**
- Ensure you have Contributor access to the subscription
- Test changes in non-production first if possible
- Have a rollback plan
- Notify stakeholders of changes

---

## Quick Fixes (Zero Cost, Minimal Risk)

### Fix All Critical Issues

"""
    
    # Critical findings
    critical = [f for f in findings_data['findings'] if f['severity'] == 'Critical']
    by_title = defaultdict(list)
    for f in critical:
        by_title[f['title']].append(f['appService'])
    
    for title, apps_list in by_title.items():
        example = next(f for f in critical if f['title'] == title)
        content += f"#### {title}\n\n"
        content += f"**Affected:** {len(apps_list)} service(s)\n\n"
        content += f"{example['recommendation']}\n\n"
        content += "**Apply to all affected services:**\n\n```bash\n"
        
        for app_name in apps_list:
            rg = app_rg_map.get(app_name, '<resource-group>')
            if 'min-tls-version' in example['recommendation']:
                content += f"az webapp config set --resource-group {rg} --name {app_name} --min-tls-version 1.2\n"
            elif 'https-only' in example['recommendation']:
                content += f"az webapp update --resource-group {rg} --name {app_name} --https-only true\n"
        
        content += "```\n\n"
    
    content += "### Fix All High Priority Issues\n\n"
    
    # High findings
    high = [f for f in findings_data['findings'] if f['severity'] == 'High']
    by_title = defaultdict(list)
    for f in high:
        by_title[f['title']].append(f['appService'])
    
    for title, apps_list in by_title.items():
        example = next(f for f in high if f['title'] == title)
        content += f"#### {title}\n\n"
        content += f"**Affected:** {len(apps_list)} service(s)\n\n"
        content += f"{example['recommendation']}\n\n"
        content += "**Apply to all affected services:**\n\n```bash\n"
        
        for app_name in apps_list:
            rg = app_rg_map.get(app_name, '<resource-group>')
            if 'https-only' in example['recommendation']:
                content += f"az webapp update --resource-group {rg} --name {app_name} --https-only true\n"
            elif 'remote-debugging' in example['recommendation']:
                content += f"az webapp config set --resource-group {rg} --name {app_name} --remote-debugging-enabled false\n"
        
        content += "```\n\n"
    
    content += """---

## Service-Specific Remediation

Below are all findings organized by App Service for systematic remediation.

"""
    
    # Group by app service
    apps = defaultdict(list)
    for finding in findings_data['findings']:
        apps[finding['appService']].append(finding)
    
    for app_name in sorted(apps.keys()):
        rg = app_rg_map.get(app_name, '<resource-group>')
        findings = apps[app_name]
        content += f"### {app_name}\n\n"
        content += f"**Resource Group:** `{rg}`  \n"
        content += f"**Findings:** {len(findings)}  \n\n"
        
        # Sort by severity
        severity_order = {"Critical": 0, "High": 1, "Medium": 2, "Low": 3}
        findings.sort(key=lambda x: severity_order.get(x['severity'], 4))
        
        for i, finding in enumerate(findings, 1):
            content += f"#### {i}. {finding['title']} ({finding['severity']})\n\n"
            content += f"**Issue:** {finding['description']}\n\n"
            content += f"**Fix:** {finding['recommendation']}\n\n"
            if finding.get('reference'):
                content += f"**Reference:** {finding['reference']}\n\n"
        
        content += "---\n\n"
    
    content += """## Verification

After applying fixes, verify changes:

```bash
# Check TLS version
az webapp config show --resource-group <rg> --name <app> --query minTlsVersion

# Check HTTPS-only
az webapp show --resource-group <rg> --name <app> --query httpsOnly

# Check logging
az webapp log config show --resource-group <rg> --name <app>
```

## Re-Assessment

After remediation, run the assessment again to verify improvements:

```bash
./run-assessment.sh
```

Compare the findings count before and after to measure progress.
"""
    
    return content


def main():
    if len(sys.argv) < 3:
        print("Usage: python3 generate-docs.py <findings-file.json> <data-file.json>")
        sys.exit(1)
    
    findings_file = Path(sys.argv[1])
    data_file = Path(sys.argv[2])
    
    if not findings_file.exists() or not data_file.exists():
        print("Error: One or more input files not found")
        sys.exit(1)
    
    output_dir = findings_file.parent
    
    # Generate Executive Summary
    exec_summary = generate_executive_summary(findings_file, data_file)
    exec_file = output_dir / "EXECUTIVE-SUMMARY.md"
    with open(exec_file, 'w') as f:
        f.write(exec_summary)
    print(f"✓ Generated: {exec_file}")
    
    # Generate Remediation Guide
    remediation = generate_remediation_guide(findings_file, data_file)
    remediation_file = output_dir / "REMEDIATION-GUIDE.md"
    with open(remediation_file, 'w') as f:
        f.write(remediation)
    print(f"✓ Generated: {remediation_file}")


if __name__ == "__main__":
    main()
