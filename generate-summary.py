#!/usr/bin/env python3
"""
Generate a text summary from findings JSON
"""

import json
import sys
from pathlib import Path
from collections import defaultdict

def generate_summary(findings_file: Path) -> str:
    """Generate text summary from findings"""
    with open(findings_file, 'r') as f:
        data = json.load(f)
    
    summary = []
    summary.append("=" * 80)
    summary.append("AZURE APP SERVICE ASSESSMENT - EXECUTIVE SUMMARY")
    summary.append("=" * 80)
    summary.append("")
    summary.append(f"Subscription: {data.get('subscription', 'N/A')}")
    summary.append(f"Subscription ID: {data.get('subscriptionId', 'N/A')}")
    summary.append(f"Assessment Date: {data.get('assessmentDate', 'N/A')}")
    summary.append("")
    summary.append("FINDINGS SUMMARY BY SEVERITY")
    summary.append("-" * 80)
    summary.append(f"  Critical: {data['findingsBySeverity']['Critical']}")
    summary.append(f"  High:     {data['findingsBySeverity']['High']}")
    summary.append(f"  Medium:   {data['findingsBySeverity']['Medium']}")
    summary.append(f"  Low:      {data['findingsBySeverity']['Low']}")
    summary.append(f"  TOTAL:    {data['totalFindings']}")
    summary.append("")
    
    # Group by app service
    apps = defaultdict(lambda: {"Critical": 0, "High": 0, "Medium": 0, "Low": 0, "Total": 0})
    for finding in data['findings']:
        app_name = finding['appService']
        severity = finding['severity']
        apps[app_name][severity] += 1
        apps[app_name]['Total'] += 1
    
    summary.append("FINDINGS BY APP SERVICE")
    summary.append("-" * 80)
    for app_name in sorted(apps.keys()):
        counts = apps[app_name]
        summary.append(f"\n{app_name}")
        summary.append(f"  Critical: {counts['Critical']}, High: {counts['High']}, Medium: {counts['Medium']}, Low: {counts['Low']}")
        summary.append(f"  Total: {counts['Total']} findings")
    
    summary.append("")
    summary.append("")
    
    # Group by category
    categories = defaultdict(lambda: {"Critical": 0, "High": 0, "Medium": 0, "Low": 0, "Total": 0})
    for finding in data['findings']:
        category = finding['category']
        severity = finding['severity']
        categories[category][severity] += 1
        categories[category]['Total'] += 1
    
    summary.append("FINDINGS BY CATEGORY")
    summary.append("-" * 80)
    for category in sorted(categories.keys()):
        counts = categories[category]
        summary.append(f"\n{category}")
        summary.append(f"  Critical: {counts['Critical']}, High: {counts['High']}, Medium: {counts['Medium']}, Low: {counts['Low']}")
        summary.append(f"  Total: {counts['Total']} findings")
    
    summary.append("")
    summary.append("")
    
    # Critical findings details
    critical_findings = [f for f in data['findings'] if f['severity'] == 'Critical']
    if critical_findings:
        summary.append("CRITICAL FINDINGS (Immediate Action Required)")
        summary.append("=" * 80)
        for finding in critical_findings:
            summary.append(f"\n[{finding['appService']}] {finding['title']}")
            summary.append(f"  Category: {finding['category']}")
            summary.append(f"  Issue: {finding['description']}")
            summary.append(f"  Action: {finding['recommendation']}")
            if finding.get('reference'):
                summary.append(f"  Ref: {finding['reference']}")
    
    summary.append("")
    summary.append("")
    
    # High findings details
    high_findings = [f for f in data['findings'] if f['severity'] == 'High']
    if high_findings:
        summary.append("HIGH PRIORITY FINDINGS")
        summary.append("=" * 80)
        for finding in high_findings:
            summary.append(f"\n[{finding['appService']}] {finding['title']}")
            summary.append(f"  Category: {finding['category']}")
            summary.append(f"  Issue: {finding['description']}")
            summary.append(f"  Action: {finding['recommendation']}")
            if finding.get('reference'):
                summary.append(f"  Ref: {finding['reference']}")
    
    summary.append("")
    summary.append("=" * 80)
    summary.append("For complete details, see the HTML report.")
    summary.append("=" * 80)
    
    return "\n".join(summary)

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 generate-summary.py <findings-file.json>")
        sys.exit(1)
    
    findings_file = Path(sys.argv[1])
    
    if not findings_file.exists():
        print(f"Error: File not found: {findings_file}")
        sys.exit(1)
    
    summary_text = generate_summary(findings_file)
    
    # Save to file
    output_file = findings_file.parent / f"assessment-summary-{findings_file.stem.split('-', 1)[1]}.txt"
    with open(output_file, 'w') as f:
        f.write(summary_text)
    
    # Also print to console
    print(summary_text)
    print(f"\n\nSummary saved to: {output_file}")

if __name__ == "__main__":
    main()
