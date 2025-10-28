#!/usr/bin/env python3
"""
Azure App Service Best Practices Analyzer
Analyzes collected App Service data against Microsoft best practices
"""

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any

class Finding:
    """Represents a single finding from the assessment"""
    
    CRITICAL = "Critical"
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"
    
    def __init__(self, app_name: str, category: str, severity: str, 
                 title: str, description: str, recommendation: str, 
                 reference: str = ""):
        self.app_name = app_name
        self.category = category
        self.severity = severity
        self.title = title
        self.description = description
        self.recommendation = recommendation
        self.reference = reference
    
    def to_dict(self) -> Dict[str, str]:
        return {
            "appService": self.app_name,
            "category": self.category,
            "severity": self.severity,
            "title": self.title,
            "description": self.description,
            "recommendation": self.recommendation,
            "reference": self.reference
        }


class AppServiceAnalyzer:
    """Analyzes App Service configurations for best practices"""
    
    def __init__(self, data: Dict[str, Any]):
        self.data = data
        self.findings: List[Finding] = []
    
    def analyze(self) -> List[Finding]:
        """Run all analysis checks"""
        print("Starting analysis...")
        
        for app_service in self.data.get("appServices", []):
            app_name = app_service.get("name", "Unknown")
            print(f"  Analyzing: {app_name}")
            
            self.check_tls_version(app_service)
            self.check_https_only(app_service)
            self.check_managed_identity(app_service)
            self.check_always_on(app_service)
            self.check_remote_debugging(app_service)
            self.check_ftps_state(app_service)
            self.check_http20_enabled(app_service)
            self.check_client_certificate_mode(app_service)
            self.check_diagnostic_logs(app_service)
            self.check_backup_configuration(app_service)
            self.check_deployment_slots(app_service)
            self.check_app_service_plan(app_service)
            self.check_vnet_integration(app_service)
            self.check_ip_restrictions(app_service)
            self.check_authentication(app_service)
            self.check_custom_domain_ssl(app_service)
            self.check_runtime_version(app_service)
            self.check_health_check(app_service)
            self.check_auto_heal(app_service)
            self.check_cors_configuration(app_service)
        
        print(f"Analysis complete. Found {len(self.findings)} issues.")
        return self.findings
    
    def check_tls_version(self, app: Dict):
        """Check minimum TLS version"""
        app_name = app.get("name")
        tls_config = app.get("tlsConfig", {})
        min_tls = tls_config.get("minTlsVersion")
        
        if not min_tls or min_tls < "1.2":
            self.findings.append(Finding(
                app_name=app_name,
                category="Security",
                severity=Finding.CRITICAL,
                title="Minimum TLS version not set to 1.2 or higher",
                description=f"Current TLS version: {min_tls or 'Not set'}. TLS 1.0 and 1.1 are deprecated and insecure.",
                recommendation="Set minimum TLS version to 1.2 or higher using: az webapp config set --min-tls-version 1.2",
                reference="https://learn.microsoft.com/en-us/azure/app-service/configure-ssl-bindings#enforce-tls-versions"
            ))
    
    def check_https_only(self, app: Dict):
        """Check HTTPS only enforcement"""
        app_name = app.get("name")
        config = app.get("config", {})
        https_only = config.get("httpsOnly", False)
        
        if not https_only:
            self.findings.append(Finding(
                app_name=app_name,
                category="Security",
                severity=Finding.HIGH,
                title="HTTPS Only not enforced",
                description="App Service is accessible over HTTP, exposing data to man-in-the-middle attacks.",
                recommendation="Enable HTTPS Only using: az webapp update --https-only true",
                reference="https://learn.microsoft.com/en-us/azure/app-service/configure-ssl-bindings#enforce-https"
            ))
    
    def check_managed_identity(self, app: Dict):
        """Check for Managed Identity usage"""
        app_name = app.get("name")
        identity = app.get("identity", {})
        identity_type = identity.get("type", "None")
        
        if identity_type == "None":
            self.findings.append(Finding(
                app_name=app_name,
                category="Security",
                severity=Finding.MEDIUM,
                title="Managed Identity not enabled",
                description="Not using Managed Identity increases risk of credential exposure in code or configuration.",
                recommendation="Enable System-Assigned Managed Identity using: az webapp identity assign",
                reference="https://learn.microsoft.com/en-us/azure/app-service/overview-managed-identity"
            ))
    
    def check_always_on(self, app: Dict):
        """Check Always On setting"""
        app_name = app.get("name")
        tls_config = app.get("tlsConfig", {})
        runtime_config = app.get("runtimeConfig", {})
        always_on = tls_config.get("alwaysOn") or runtime_config.get("alwaysOn", False)
        
        # Check if it's a production tier (not Free or Shared)
        plan = app.get("appServicePlan", {})
        sku = plan.get("sku", {}).get("tier", "").lower()
        
        if sku not in ["free", "shared"] and not always_on:
            self.findings.append(Finding(
                app_name=app_name,
                category="Performance",
                severity=Finding.MEDIUM,
                title="Always On is not enabled",
                description="App may experience cold starts and increased latency after idle periods.",
                recommendation="Enable Always On using: az webapp config set --always-on true",
                reference="https://learn.microsoft.com/en-us/azure/app-service/configure-common#configure-general-settings"
            ))
    
    def check_remote_debugging(self, app: Dict):
        """Check remote debugging status"""
        app_name = app.get("name")
        tls_config = app.get("tlsConfig", {})
        runtime_config = app.get("runtimeConfig", {})
        remote_debug = tls_config.get("remoteDebuggingEnabled") or runtime_config.get("remoteDebuggingEnabled", False)
        
        if remote_debug:
            self.findings.append(Finding(
                app_name=app_name,
                category="Security",
                severity=Finding.HIGH,
                title="Remote debugging is enabled",
                description="Remote debugging should only be enabled temporarily and poses a security risk in production.",
                recommendation="Disable remote debugging using: az webapp config set --remote-debugging-enabled false",
                reference="https://learn.microsoft.com/en-us/azure/app-service/configure-common#configure-general-settings"
            ))
    
    def check_ftps_state(self, app: Dict):
        """Check FTPS enforcement"""
        app_name = app.get("name")
        tls_config = app.get("tlsConfig", {})
        runtime_config = app.get("runtimeConfig", {})
        ftps_state = tls_config.get("ftpsState") or runtime_config.get("ftpsState", "")
        
        if ftps_state.lower() == "allallowed":
            self.findings.append(Finding(
                app_name=app_name,
                category="Security",
                severity=Finding.MEDIUM,
                title="FTP is allowed (not secure)",
                description="Plain FTP is insecure. Only FTPS should be allowed.",
                recommendation="Set FTPS to FtpsOnly or Disabled: az webapp config set --ftps-state FtpsOnly",
                reference="https://learn.microsoft.com/en-us/azure/app-service/deploy-ftp"
            ))
    
    def check_http20_enabled(self, app: Dict):
        """Check HTTP/2 enablement"""
        app_name = app.get("name")
        tls_config = app.get("tlsConfig", {})
        runtime_config = app.get("runtimeConfig", {})
        http20 = tls_config.get("http20Enabled") or runtime_config.get("http20Enabled", False)
        
        if not http20:
            self.findings.append(Finding(
                app_name=app_name,
                category="Performance",
                severity=Finding.LOW,
                title="HTTP/2 not enabled",
                description="HTTP/2 provides better performance with multiplexing and header compression.",
                recommendation="Enable HTTP/2 using: az webapp config set --http20-enabled true",
                reference="https://learn.microsoft.com/en-us/azure/app-service/configure-common#configure-general-settings"
            ))
    
    def check_client_certificate_mode(self, app: Dict):
        """Check client certificate configuration"""
        app_name = app.get("name")
        config = app.get("config", {})
        client_cert_enabled = config.get("clientCertEnabled", False)
        client_cert_mode = config.get("clientCertMode", "")
        
        # This is informational - only flag if enabled but mode is Optional
        if client_cert_enabled and client_cert_mode == "Optional":
            self.findings.append(Finding(
                app_name=app_name,
                category="Security",
                severity=Finding.LOW,
                title="Client certificates set to Optional",
                description="Client certificates are enabled but set to optional mode.",
                recommendation="Consider setting to Required if mutual TLS authentication is needed: az webapp update --client-cert-mode Required",
                reference="https://learn.microsoft.com/en-us/azure/app-service/app-service-web-configure-tls-mutual-auth"
            ))
    
    def check_diagnostic_logs(self, app: Dict):
        """Check diagnostic logging configuration"""
        app_name = app.get("name")
        diag_logs = app.get("diagnosticLogs", {})
        
        app_logs = diag_logs.get("applicationLogsConfiguration", {})
        http_logs = diag_logs.get("httpLogsConfiguration", {})
        
        app_logs_enabled = app_logs.get("fileSystem", {}).get("level", "Off") != "Off" or \
                          app_logs.get("azureBlobStorage", {}).get("level", "Off") != "Off"
        
        http_logs_enabled = http_logs.get("fileSystem", {}).get("enabled", False) or \
                           http_logs.get("azureBlobStorage", {}).get("enabled", False)
        
        if not app_logs_enabled and not http_logs_enabled:
            self.findings.append(Finding(
                app_name=app_name,
                category="Monitoring",
                severity=Finding.MEDIUM,
                title="Diagnostic logging not configured",
                description="No application or HTTP logging is enabled, making troubleshooting difficult.",
                recommendation="Enable diagnostic logs using: az webapp log config --application-logging filesystem --level information",
                reference="https://learn.microsoft.com/en-us/azure/app-service/troubleshoot-diagnostic-logs"
            ))
    
    def check_backup_configuration(self, app: Dict):
        """Check backup configuration"""
        app_name = app.get("name")
        backup = app.get("backupConfig", [])
        
        plan = app.get("appServicePlan", {})
        sku = plan.get("sku", {}).get("tier", "").lower()
        
        # Backups are only available in Standard tier and above
        if sku in ["standard", "premium", "premiumv2", "premiumv3"] and not backup:
            self.findings.append(Finding(
                app_name=app_name,
                category="Reliability",
                severity=Finding.MEDIUM,
                title="Backup not configured",
                description="No backup schedule configured for the App Service.",
                recommendation="Configure automated backups for disaster recovery: az webapp config backup create",
                reference="https://learn.microsoft.com/en-us/azure/app-service/manage-backup"
            ))
    
    def check_deployment_slots(self, app: Dict):
        """Check deployment slots configuration"""
        app_name = app.get("name")
        slots = app.get("deploymentSlots", [])
        
        plan = app.get("appServicePlan", {})
        sku = plan.get("sku", {}).get("tier", "").lower()
        
        # Slots are available in Standard tier and above
        if sku in ["standard", "premium", "premiumv2", "premiumv3"] and not slots:
            self.findings.append(Finding(
                app_name=app_name,
                category="DevOps",
                severity=Finding.LOW,
                title="No deployment slots configured",
                description="Deployment slots enable zero-downtime deployments and easy rollback.",
                recommendation="Create a staging slot: az webapp deployment slot create --slot staging",
                reference="https://learn.microsoft.com/en-us/azure/app-service/deploy-staging-slots"
            ))
    
    def check_app_service_plan(self, app: Dict):
        """Check App Service Plan configuration"""
        app_name = app.get("name")
        plan = app.get("appServicePlan", {})
        
        sku = plan.get("sku", {})
        tier = sku.get("tier", "").lower()
        capacity = sku.get("capacity", 1)
        
        # Check for Free/Shared tier in production
        if tier in ["free", "shared"]:
            self.findings.append(Finding(
                app_name=app_name,
                category="Reliability",
                severity=Finding.HIGH,
                title="Using Free or Shared tier",
                description="Free/Shared tiers have limited resources, no SLA, and lack production features.",
                recommendation="Upgrade to at least Basic tier for production workloads: az appservice plan update --sku B1",
                reference="https://learn.microsoft.com/en-us/azure/app-service/overview-hosting-plans"
            ))
        
        # Check for single instance (no scale out)
        if tier not in ["free", "shared"] and capacity == 1:
            self.findings.append(Finding(
                app_name=app_name,
                category="Reliability",
                severity=Finding.MEDIUM,
                title="Single instance configuration",
                description="Running on a single instance - no redundancy for high availability.",
                recommendation="Scale to at least 2 instances or enable autoscaling for production apps",
                reference="https://learn.microsoft.com/en-us/azure/app-service/manage-scale-up"
            ))
        
        # Check for zone redundancy
        zone_redundant = plan.get("zoneRedundant", False)
        if tier in ["premiumv2", "premiumv3"] and not zone_redundant:
            self.findings.append(Finding(
                app_name=app_name,
                category="Reliability",
                severity=Finding.LOW,
                title="Zone redundancy not enabled",
                description="Zone redundancy provides higher availability across Azure availability zones.",
                recommendation="Consider enabling zone redundancy for critical production apps",
                reference="https://learn.microsoft.com/en-us/azure/app-service/how-to-zone-redundancy"
            ))
    
    def check_vnet_integration(self, app: Dict):
        """Check VNet integration"""
        app_name = app.get("name")
        vnet = app.get("vnetIntegration", [])
        
        if not vnet:
            self.findings.append(Finding(
                app_name=app_name,
                category="Security",
                severity=Finding.LOW,
                title="VNet integration not configured",
                description="App Service is not integrated with a Virtual Network, limiting network isolation options.",
                recommendation="Consider VNet integration for secure access to backend resources: az webapp vnet-integration add",
                reference="https://learn.microsoft.com/en-us/azure/app-service/overview-vnet-integration"
            ))
    
    def check_ip_restrictions(self, app: Dict):
        """Check IP restrictions"""
        app_name = app.get("name")
        ip_restrictions = app.get("ipRestrictions", {})
        
        main_site_rules = ip_restrictions.get("ipSecurityRestrictions", [])
        scm_rules = ip_restrictions.get("scmIpSecurityRestrictions", [])
        
        # Filter out default allow rules
        main_site_rules = [r for r in main_site_rules if r.get("action") != "Allow" or r.get("ipAddress") != "Any"]
        scm_rules = [r for r in scm_rules if r.get("action") != "Allow" or r.get("ipAddress") != "Any"]
        
        if not main_site_rules:
            self.findings.append(Finding(
                app_name=app_name,
                category="Security",
                severity=Finding.MEDIUM,
                title="No IP restrictions configured",
                description="App Service is accessible from any IP address on the internet.",
                recommendation="Configure IP restrictions to limit access: az webapp config access-restriction add",
                reference="https://learn.microsoft.com/en-us/azure/app-service/app-service-ip-restrictions"
            ))
        
        if not scm_rules and not ip_restrictions.get("scmIpSecurityRestrictionsUseMain", False):
            self.findings.append(Finding(
                app_name=app_name,
                category="Security",
                severity=Finding.MEDIUM,
                title="No SCM IP restrictions configured",
                description="Kudu/SCM site is accessible from any IP address.",
                recommendation="Configure SCM IP restrictions or use main site restrictions: az webapp config access-restriction add --scm-site true",
                reference="https://learn.microsoft.com/en-us/azure/app-service/app-service-ip-restrictions"
            ))
    
    def check_authentication(self, app: Dict):
        """Check authentication configuration"""
        app_name = app.get("name")
        auth = app.get("authConfig", {})
        
        enabled = auth.get("enabled", False)
        unauthenticated_action = auth.get("unauthenticatedClientAction")
        
        if not enabled:
            self.findings.append(Finding(
                app_name=app_name,
                category="Security",
                severity=Finding.LOW,
                title="App Service Authentication not enabled",
                description="Easy Auth/EasyAuth is not configured. Consider if authentication is needed.",
                recommendation="If the app requires authentication, enable App Service Authentication: az webapp auth update --enabled true",
                reference="https://learn.microsoft.com/en-us/azure/app-service/overview-authentication-authorization"
            ))
    
    def check_custom_domain_ssl(self, app: Dict):
        """Check custom domain and SSL configuration"""
        app_name = app.get("name")
        domains = app.get("customDomains", [])
        ssl_certs = app.get("sslCertificates", [])
        
        # Check for custom domains without SSL
        custom_domains = [d for d in domains if not d.get("hostName", "").endswith(".azurewebsites.net")]
        
        if custom_domains and not ssl_certs:
            self.findings.append(Finding(
                app_name=app_name,
                category="Security",
                severity=Finding.MEDIUM,
                title="Custom domain without SSL certificate",
                description="Custom domain(s) configured but no SSL certificates found.",
                recommendation="Add SSL certificates for custom domains: az webapp config ssl upload",
                reference="https://learn.microsoft.com/en-us/azure/app-service/configure-ssl-certificate"
            ))
    
    def check_runtime_version(self, app: Dict):
        """Check runtime version"""
        app_name = app.get("name")
        config = app.get("config", {})
        runtime_config = app.get("runtimeConfig", {})
        
        # Get runtime stack info
        linux_fx = config.get("linuxFxVersion", "") or runtime_config.get("linuxFxVersion", "")
        windows_fx = runtime_config.get("windowsFxVersion", "")
        
        # Check for specific deprecated versions (examples)
        deprecated_patterns = [
            "NODE|10", "NODE|12", "NODE|14",  # Node.js < 16
            "DOTNETCORE|2", "DOTNETCORE|3.0",  # .NET Core < 3.1
            "PYTHON|2", "PYTHON|3.6", "PYTHON|3.7",  # Python < 3.8
            "PHP|7.0", "PHP|7.1", "PHP|7.2", "PHP|7.3",  # PHP < 7.4
            "JAVA|8",  # Java 8 (consider upgrading)
        ]
        
        fx_version = linux_fx or windows_fx
        for pattern in deprecated_patterns:
            if pattern.lower() in fx_version.lower():
                self.findings.append(Finding(
                    app_name=app_name,
                    category="Security",
                    severity=Finding.HIGH,
                    title="Using deprecated or outdated runtime version",
                    description=f"Runtime version '{fx_version}' may be deprecated or lack security updates.",
                    recommendation="Update to a supported runtime version: az webapp config set --linux-fx-version or --windows-fx-version",
                    reference="https://learn.microsoft.com/en-us/azure/app-service/overview-patch-os-runtime"
                ))
                break
    
    def check_health_check(self, app: Dict):
        """Check health check configuration"""
        app_name = app.get("name")
        runtime_config = app.get("runtimeConfig", {})
        
        health_check_path = runtime_config.get("healthCheckPath", "")
        
        plan = app.get("appServicePlan", {})
        sku = plan.get("sku", {}).get("tier", "").lower()
        capacity = plan.get("sku", {}).get("capacity", 1)
        
        # Health check is most important for multi-instance deployments
        if sku not in ["free", "shared"] and capacity > 1 and not health_check_path:
            self.findings.append(Finding(
                app_name=app_name,
                category="Reliability",
                severity=Finding.MEDIUM,
                title="Health check not configured",
                description="No health check endpoint configured for multi-instance deployment.",
                recommendation="Configure health check path: az webapp config set --health-check-path /health",
                reference="https://learn.microsoft.com/en-us/azure/app-service/monitor-instances-health-check"
            ))
    
    def check_auto_heal(self, app: Dict):
        """Check auto-heal configuration"""
        app_name = app.get("name")
        runtime_config = app.get("runtimeConfig", {})
        
        auto_heal = runtime_config.get("autoHealEnabled", False)
        
        if not auto_heal:
            self.findings.append(Finding(
                app_name=app_name,
                category="Reliability",
                severity=Finding.LOW,
                title="Auto-heal not configured",
                description="Auto-heal can automatically recover from common failure scenarios.",
                recommendation="Consider enabling auto-heal with appropriate triggers and actions",
                reference="https://learn.microsoft.com/en-us/azure/app-service/overview-diagnostics#auto-healing"
            ))
    
    def check_cors_configuration(self, app: Dict):
        """Check CORS configuration"""
        app_name = app.get("name")
        runtime_config = app.get("runtimeConfig", {})
        
        cors = runtime_config.get("cors")
        if cors is None:
            return
            
        allowed_origins = cors.get("allowedOrigins", [])
        
        # Check for wildcard
        if "*" in allowed_origins:
            self.findings.append(Finding(
                app_name=app_name,
                category="Security",
                severity=Finding.MEDIUM,
                title="CORS configured with wildcard (*)",
                description="CORS is configured to allow all origins, which may expose the API to unauthorized access.",
                recommendation="Restrict CORS to specific origins: az webapp cors remove --allowed-origins * && az webapp cors add --allowed-origins https://example.com",
                reference="https://learn.microsoft.com/en-us/azure/app-service/app-service-web-tutorial-rest-api"
            ))


def main():
    """Main execution function"""
    if len(sys.argv) < 2:
        print("Usage: python3 analyze-app-services.py <data-file.json>")
        sys.exit(1)
    
    data_file = Path(sys.argv[1])
    
    if not data_file.exists():
        print(f"Error: File not found: {data_file}")
        sys.exit(1)
    
    print(f"Loading data from: {data_file}")
    with open(data_file, 'r') as f:
        data = json.load(f)
    
    # Run analysis
    analyzer = AppServiceAnalyzer(data)
    findings = analyzer.analyze()
    
    # Save findings to JSON
    output_file = data_file.parent / f"findings-{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    findings_data = {
        "subscription": data.get("subscription"),
        "subscriptionId": data.get("subscriptionId"),
        "assessmentDate": data.get("assessmentDate"),
        "analysisDate": datetime.now().isoformat(),
        "totalFindings": len(findings),
        "findingsBySeverity": {
            "Critical": len([f for f in findings if f.severity == Finding.CRITICAL]),
            "High": len([f for f in findings if f.severity == Finding.HIGH]),
            "Medium": len([f for f in findings if f.severity == Finding.MEDIUM]),
            "Low": len([f for f in findings if f.severity == Finding.LOW])
        },
        "findings": [f.to_dict() for f in findings]
    }
    
    with open(output_file, 'w') as f:
        json.dump(findings_data, f, indent=2)
    
    print(f"\nFindings saved to: {output_file}")
    print(f"\nSummary:")
    print(f"  Critical: {findings_data['findingsBySeverity']['Critical']}")
    print(f"  High:     {findings_data['findingsBySeverity']['High']}")
    print(f"  Medium:   {findings_data['findingsBySeverity']['Medium']}")
    print(f"  Low:      {findings_data['findingsBySeverity']['Low']}")
    print(f"  Total:    {findings_data['totalFindings']}")


if __name__ == "__main__":
    main()
