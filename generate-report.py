#!/usr/bin/env python3
"""
Azure App Service Assessment Report Generator
Generates a comprehensive HTML report from analysis findings
"""

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Azure App Service Assessment Report</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            background: #f5f5f5;
            padding: 20px;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            padding: 40px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        
        header {{
            border-bottom: 3px solid #0078d4;
            padding-bottom: 20px;
            margin-bottom: 30px;
        }}
        
        h1 {{
            color: #0078d4;
            font-size: 2.5em;
            margin-bottom: 10px;
        }}
        
        h2 {{
            color: #0078d4;
            font-size: 1.8em;
            margin-top: 30px;
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 2px solid #e1e1e1;
        }}
        
        h3 {{
            color: #333;
            font-size: 1.3em;
            margin-top: 20px;
            margin-bottom: 10px;
        }}
        
        .meta-info {{
            background: #f8f9fa;
            padding: 15px;
            border-radius: 4px;
            margin-bottom: 20px;
        }}
        
        .meta-info p {{
            margin: 5px 0;
            color: #666;
        }}
        
        .meta-info strong {{
            color: #333;
        }}
        
        .summary {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }}
        
        .summary-card {{
            padding: 20px;
            border-radius: 8px;
            text-align: center;
            color: white;
        }}
        
        .summary-card.critical {{
            background: linear-gradient(135deg, #dc3545 0%, #c82333 100%);
        }}
        
        .summary-card.high {{
            background: linear-gradient(135deg, #fd7e14 0%, #e8590c 100%);
        }}
        
        .summary-card.medium {{
            background: linear-gradient(135deg, #ffc107 0%, #e0a800 100%);
        }}
        
        .summary-card.low {{
            background: linear-gradient(135deg, #17a2b8 0%, #138496 100%);
        }}
        
        .summary-card.total {{
            background: linear-gradient(135deg, #6c757d 0%, #5a6268 100%);
        }}
        
        .summary-card h3 {{
            color: white;
            font-size: 2.5em;
            margin: 10px 0;
        }}
        
        .summary-card p {{
            font-size: 1em;
            opacity: 0.9;
        }}
        
        .finding {{
            background: white;
            border: 1px solid #e1e1e1;
            border-radius: 6px;
            padding: 20px;
            margin-bottom: 20px;
            border-left: 4px solid #0078d4;
        }}
        
        .finding.critical {{
            border-left-color: #dc3545;
            background: #fff5f5;
        }}
        
        .finding.high {{
            border-left-color: #fd7e14;
            background: #fff8f0;
        }}
        
        .finding.medium {{
            border-left-color: #ffc107;
            background: #fffbf0;
        }}
        
        .finding.low {{
            border-left-color: #17a2b8;
            background: #f0f9fb;
        }}
        
        .finding-header {{
            display: flex;
            justify-content: space-between;
            align-items: start;
            margin-bottom: 15px;
        }}
        
        .finding-title {{
            font-size: 1.2em;
            font-weight: 600;
            color: #333;
            flex: 1;
        }}
        
        .severity-badge {{
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 0.85em;
            font-weight: 600;
            text-transform: uppercase;
            margin-left: 10px;
        }}
        
        .severity-badge.critical {{
            background: #dc3545;
            color: white;
        }}
        
        .severity-badge.high {{
            background: #fd7e14;
            color: white;
        }}
        
        .severity-badge.medium {{
            background: #ffc107;
            color: #333;
        }}
        
        .severity-badge.low {{
            background: #17a2b8;
            color: white;
        }}
        
        .finding-meta {{
            display: flex;
            gap: 20px;
            margin-bottom: 15px;
            font-size: 0.9em;
            color: #666;
        }}
        
        .finding-meta span {{
            display: flex;
            align-items: center;
        }}
        
        .finding-meta strong {{
            margin-right: 5px;
            color: #333;
        }}
        
        .finding-section {{
            margin: 15px 0;
        }}
        
        .finding-section h4 {{
            color: #0078d4;
            font-size: 0.95em;
            margin-bottom: 8px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        
        .finding-section p {{
            color: #555;
            margin-bottom: 10px;
        }}
        
        .recommendation {{
            background: #e7f3ff;
            border-left: 3px solid #0078d4;
            padding: 12px;
            margin: 10px 0;
            border-radius: 4px;
        }}
        
        .reference {{
            font-size: 0.9em;
            margin-top: 10px;
        }}
        
        .reference a {{
            color: #0078d4;
            text-decoration: none;
        }}
        
        .reference a:hover {{
            text-decoration: underline;
        }}
        
        .no-findings {{
            text-align: center;
            padding: 40px;
            background: #e7f3ff;
            border-radius: 8px;
            color: #0078d4;
        }}
        
        .category-section {{
            margin-top: 40px;
        }}
        
        .app-service-group {{
            margin-top: 30px;
        }}
        
        .app-service-header {{
            background: #0078d4;
            color: white;
            padding: 15px 20px;
            border-radius: 6px 6px 0 0;
            font-size: 1.2em;
            font-weight: 600;
        }}
        
        .findings-list {{
            border: 1px solid #e1e1e1;
            border-top: none;
            border-radius: 0 0 6px 6px;
            padding: 20px;
            background: #fafafa;
        }}
        
        footer {{
            margin-top: 40px;
            padding-top: 20px;
            border-top: 2px solid #e1e1e1;
            text-align: center;
            color: #666;
            font-size: 0.9em;
        }}
        
        .toc {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 6px;
            margin: 20px 0;
        }}
        
        .toc ul {{
            list-style: none;
            padding-left: 20px;
        }}
        
        .toc li {{
            margin: 8px 0;
        }}
        
        .toc a {{
            color: #0078d4;
            text-decoration: none;
        }}
        
        .toc a:hover {{
            text-decoration: underline;
        }}
        
        @media print {{
            body {{
                background: white;
                padding: 0;
            }}
            
            .container {{
                box-shadow: none;
                padding: 20px;
            }}
            
            .finding {{
                page-break-inside: avoid;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🔍 Azure App Service Assessment Report</h1>
            <div class="meta-info">
                <p><strong>Subscription:</strong> {subscription}</p>
                <p><strong>Subscription ID:</strong> {subscription_id}</p>
                <p><strong>Assessment Date:</strong> {assessment_date}</p>
                <p><strong>Report Generated:</strong> {report_date}</p>
            </div>
        </header>
        
        <section>
            <h2>Executive Summary</h2>
            <div class="summary">
                <div class="summary-card critical">
                    <p>Critical</p>
                    <h3>{critical_count}</h3>
                </div>
                <div class="summary-card high">
                    <p>High</p>
                    <h3>{high_count}</h3>
                </div>
                <div class="summary-card medium">
                    <p>Medium</p>
                    <h3>{medium_count}</h3>
                </div>
                <div class="summary-card low">
                    <p>Low</p>
                    <h3>{low_count}</h3>
                </div>
                <div class="summary-card total">
                    <p>Total Findings</p>
                    <h3>{total_count}</h3>
                </div>
            </div>
        </section>
        
        {toc_section}
        
        {findings_by_severity}
        
        {findings_by_app}
        
        {findings_by_category}
        
        <footer>
            <p>This report was generated automatically based on Microsoft Azure best practices.</p>
            <p>For more information, visit <a href="https://learn.microsoft.com/en-us/azure/app-service/">Azure App Service Documentation</a></p>
            <p>Generated on {report_date}</p>
        </footer>
    </div>
</body>
</html>
"""


def generate_toc(findings_data: Dict) -> str:
    """Generate table of contents"""
    if findings_data['totalFindings'] == 0:
        return ""
    
    html = '<div class="toc">\n'
    html += '<h3>Table of Contents</h3>\n'
    html += '<ul>\n'
    html += '<li><a href="#severity">Findings by Severity</a></li>\n'
    html += '<li><a href="#appservice">Findings by App Service</a></li>\n'
    html += '<li><a href="#category">Findings by Category</a></li>\n'
    html += '</ul>\n'
    html += '</div>\n'
    
    return html


def generate_findings_by_severity(findings: List[Dict]) -> str:
    """Generate findings grouped by severity"""
    if not findings:
        return '<div class="no-findings"><h3>✅ No issues found! All App Services follow best practices.</h3></div>'
    
    html = '<section id="severity">\n'
    html += '<h2>Findings by Severity</h2>\n'
    
    severities = ["Critical", "High", "Medium", "Low"]
    
    for severity in severities:
        severity_findings = [f for f in findings if f['severity'] == severity]
        
        if not severity_findings:
            continue
        
        html += f'<div class="category-section">\n'
        html += f'<h3>🔴 {severity} Severity ({len(severity_findings)} findings)</h3>\n'
        
        for finding in severity_findings:
            html += generate_finding_card(finding)
        
        html += '</div>\n'
    
    html += '</section>\n'
    return html


def generate_findings_by_app(findings: List[Dict]) -> str:
    """Generate findings grouped by App Service"""
    if not findings:
        return ""
    
    html = '<section id="appservice">\n'
    html += '<h2>Findings by App Service</h2>\n'
    
    # Group by app service
    apps = {}
    for finding in findings:
        app_name = finding['appService']
        if app_name not in apps:
            apps[app_name] = []
        apps[app_name].append(finding)
    
    # Sort by number of findings (descending)
    sorted_apps = sorted(apps.items(), key=lambda x: len(x[1]), reverse=True)
    
    for app_name, app_findings in sorted_apps:
        html += '<div class="app-service-group">\n'
        html += f'<div class="app-service-header">{app_name} ({len(app_findings)} findings)</div>\n'
        html += '<div class="findings-list">\n'
        
        # Sort by severity
        severity_order = {"Critical": 0, "High": 1, "Medium": 2, "Low": 3}
        sorted_findings = sorted(app_findings, key=lambda x: severity_order.get(x['severity'], 4))
        
        for finding in sorted_findings:
            html += generate_finding_card(finding)
        
        html += '</div>\n'
        html += '</div>\n'
    
    html += '</section>\n'
    return html


def generate_findings_by_category(findings: List[Dict]) -> str:
    """Generate findings grouped by category"""
    if not findings:
        return ""
    
    html = '<section id="category">\n'
    html += '<h2>Findings by Category</h2>\n'
    
    # Group by category
    categories = {}
    for finding in findings:
        category = finding['category']
        if category not in categories:
            categories[category] = []
        categories[category].append(finding)
    
    # Sort by number of findings (descending)
    sorted_categories = sorted(categories.items(), key=lambda x: len(x[1]), reverse=True)
    
    for category, cat_findings in sorted_categories:
        html += '<div class="category-section">\n'
        html += f'<h3>📋 {category} ({len(cat_findings)} findings)</h3>\n'
        
        # Sort by severity
        severity_order = {"Critical": 0, "High": 1, "Medium": 2, "Low": 3}
        sorted_findings = sorted(cat_findings, key=lambda x: severity_order.get(x['severity'], 4))
        
        for finding in sorted_findings:
            html += generate_finding_card(finding)
        
        html += '</div>\n'
    
    html += '</section>\n'
    return html


def generate_finding_card(finding: Dict) -> str:
    """Generate HTML for a single finding"""
    severity_lower = finding['severity'].lower()
    
    html = f'<div class="finding {severity_lower}">\n'
    html += '<div class="finding-header">\n'
    html += f'<div class="finding-title">{finding["title"]}</div>\n'
    html += f'<span class="severity-badge {severity_lower}">{finding["severity"]}</span>\n'
    html += '</div>\n'
    
    html += '<div class="finding-meta">\n'
    html += f'<span><strong>App Service:</strong> {finding["appService"]}</span>\n'
    html += f'<span><strong>Category:</strong> {finding["category"]}</span>\n'
    html += '</div>\n'
    
    html += '<div class="finding-section">\n'
    html += '<h4>Description</h4>\n'
    html += f'<p>{finding["description"]}</p>\n'
    html += '</div>\n'
    
    html += '<div class="recommendation">\n'
    html += '<h4>Recommendation</h4>\n'
    html += f'<p>{finding["recommendation"]}</p>\n'
    html += '</div>\n'
    
    if finding.get('reference'):
        html += '<div class="reference">\n'
        html += f'<strong>Reference:</strong> <a href="{finding["reference"]}" target="_blank">{finding["reference"]}</a>\n'
        html += '</div>\n'
    
    html += '</div>\n'
    
    return html


def generate_report(findings_file: Path) -> str:
    """Generate HTML report from findings JSON"""
    with open(findings_file, 'r') as f:
        data = json.load(f)
    
    # Format dates
    assessment_date = data.get('assessmentDate', 'N/A')
    try:
        assessment_date = datetime.fromisoformat(assessment_date.replace('Z', '+00:00')).strftime('%B %d, %Y %H:%M UTC')
    except:
        pass
    
    report_date = datetime.now().strftime('%B %d, %Y %H:%M')
    
    # Generate sections
    toc = generate_toc(data)
    findings_by_sev = generate_findings_by_severity(data['findings'])
    findings_by_app = generate_findings_by_app(data['findings'])
    findings_by_cat = generate_findings_by_category(data['findings'])
    
    # Fill template
    html = HTML_TEMPLATE.format(
        subscription=data.get('subscription', 'N/A'),
        subscription_id=data.get('subscriptionId', 'N/A'),
        assessment_date=assessment_date,
        report_date=report_date,
        critical_count=data['findingsBySeverity']['Critical'],
        high_count=data['findingsBySeverity']['High'],
        medium_count=data['findingsBySeverity']['Medium'],
        low_count=data['findingsBySeverity']['Low'],
        total_count=data['totalFindings'],
        toc_section=toc,
        findings_by_severity=findings_by_sev,
        findings_by_app=findings_by_app,
        findings_by_category=findings_by_cat
    )
    
    return html


def main():
    """Main execution function"""
    if len(sys.argv) < 2:
        print("Usage: python3 generate-report.py <findings-file.json>")
        sys.exit(1)
    
    findings_file = Path(sys.argv[1])
    
    if not findings_file.exists():
        print(f"Error: File not found: {findings_file}")
        sys.exit(1)
    
    print(f"Generating report from: {findings_file}")
    
    html_report = generate_report(findings_file)
    
    # Save report
    output_file = findings_file.parent / f"assessment-report-{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
    
    with open(output_file, 'w') as f:
        f.write(html_report)
    
    print(f"Report generated: {output_file}")
    print(f"\nOpen the report in your browser:")
    print(f"  open {output_file}")


if __name__ == "__main__":
    main()
