# Assessment Methodology

Detail on what the toolkit checks, how findings are ranked, and how to extend it.
For installation and usage, see the [README](../README.md).

## Checks by category

### Security

- Minimum TLS version (1.2+)
- HTTPS-only enforcement
- Managed Identity usage
- Remote debugging disabled
- FTPS enforcement
- Client certificate configuration
- IP restrictions
- VNet integration
- Authentication / authorization
- Custom domain SSL certificates
- Runtime version currency
- CORS configuration

### Reliability

- App Service Plan tier (production-ready)
- Instance count (redundancy)
- Zone redundancy
- Health check configuration
- Auto-heal settings
- Backup configuration

### Performance

- Always On enabled
- HTTP/2 enabled
- Auto-scaling configuration

### Monitoring

- Diagnostic logging enabled
- Application Insights integration

### DevOps

- Deployment slots (staging)
- Deployment best practices

## Severity levels

| Severity | Meaning |
|----------|---------|
| **Critical** | Security vulnerabilities or compliance issues requiring immediate attention |
| **High** | Significant risks to security, availability, or performance |
| **Medium** | Important improvements for production readiness |
| **Low** | Recommendations for optimization and best practices |

## Scoping the assessment to one resource group

`assess-app-services.sh` enumerates every App Service in the current subscription.
To narrow it, add a `--resource-group` filter to the `az webapp list` call:

```bash
# Default
APP_SERVICES=$(az webapp list --query "[].{name:name, resourceGroup:resourceGroup, id:id}" -o json)

# Scoped
APP_SERVICES=$(az webapp list --resource-group "your-rg-name" --query "[].{name:name, resourceGroup:resourceGroup, id:id}" -o json)
```

## Adding a custom check

Add a check method to the `AppServiceAnalyzer` class in `analyze-app-services.py`,
then call it from `analyze()`:

```python
def check_custom_setting(self, app: Dict):
    """Check custom configuration"""
    app_name = app.get("name")
    if condition_not_met:
        self.findings.append(Finding(
            app_name=app_name,
            category="Custom",
            severity=Finding.MEDIUM,
            title="Your check title",
            description="Description",
            recommendation="What to do",
            reference="https://learn.microsoft.com/...",
        ))
```

## Restyling the report

The HTML report's CSS lives in the `HTML_TEMPLATE` variable in `generate-report.py`.

## References

- [Azure App Service best practices](https://learn.microsoft.com/en-us/azure/app-service/app-service-best-practices)
- [Azure App Service security](https://learn.microsoft.com/en-us/azure/app-service/overview-security)
- [Azure Well-Architected Framework](https://learn.microsoft.com/en-us/azure/well-architected/)
