# Contributing to Azure App Service Assessment Toolkit

Thank you for your interest in contributing! This toolkit helps organizations assess their Azure App Services against Microsoft best practices.

## How to Contribute

### Reporting Issues

If you find a bug or have a suggestion:

1. Check if the issue already exists in the Issues tab
2. If not, create a new issue with:
   - Clear description of the problem/suggestion
   - Steps to reproduce (for bugs)
   - Expected vs actual behavior
   - Your environment (OS, Azure CLI version, Python version)

### Adding New Assessment Checks

The toolkit is designed to be extensible. To add new checks:

1. **Fork the repository**

2. **Edit `analyze-app-services.py`**
   - Add a new method to the `AppServiceAnalyzer` class
   - Follow the existing pattern:
   ```python
   def check_your_new_check(self, app: Dict):
       """Check description"""
       app_name = app.get("name")
       config = app.get("config", {})
       
       # Your check logic here
       if condition_not_met:
           self.findings.append(Finding(
               app_name=app_name,
               category="Security|Performance|Reliability|Monitoring",
               severity=Finding.CRITICAL|HIGH|MEDIUM|LOW,
               title="Short descriptive title",
               description="What's wrong and why it matters",
               recommendation="How to fix it (include az cli commands)",
               reference="https://learn.microsoft.com/... (official docs)"
           ))
   ```

3. **Call your check from the `analyze()` method**
   ```python
   def analyze(self) -> List[Finding]:
       for app_service in self.data.get("appServices", []):
           # ... existing checks ...
           self.check_your_new_check(app_service)
   ```

4. **Test your changes**
   ```bash
   # Run against sample data
   python3 analyze-app-services.py app-service-assessment/app-services-data-*.json
   ```

5. **Submit a Pull Request**
   - Include description of what the check does
   - Reference any Microsoft documentation
   - Include test results if possible

### Improving Documentation

Documentation improvements are always welcome:

- Fix typos or unclear instructions
- Add examples
- Improve troubleshooting guides
- Translate to other languages

### Enhancing Reports

To improve the HTML or text reports:

- **HTML**: Edit the `HTML_TEMPLATE` in `generate-report.py`
- **Text**: Modify `generate-summary.py`
- **New formats**: Create new generator scripts (e.g., PDF, CSV, JSON)

## Development Guidelines

### Code Style

- **Python**: Follow PEP 8 guidelines
- **Shell**: Use shellcheck for linting
- **Comments**: Explain why, not what
- **Docstrings**: Required for all functions

### Commit Messages

Use clear, descriptive commit messages:

```
Add check for App Service Plan SKU tier

- Identifies Free/Shared tiers in production
- Recommends minimum Basic tier for SLA
- Severity: High
- References: Microsoft SLA documentation
```

### Testing

Before submitting:

1. Test with real Azure subscriptions (if possible)
2. Test with sample JSON data
3. Verify generated reports render correctly
4. Check for Python/shell errors

## Pull Request Process

1. Update documentation (README.md, comments)
2. Add your check to the list in README-Assessment.md
3. Test thoroughly
4. Submit PR with clear description
5. Respond to review feedback

## Questions?

Open an issue for questions or discussion!

## Code of Conduct

- Be respectful and constructive
- Focus on the code and ideas, not the person
- Help newcomers get started
- Give credit where credit is due

Thank you for contributing! 🎉
