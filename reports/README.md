# Reports

This folder contains auto-generated HTML test reports.

## How Reports Are Generated

Reports are created automatically when you run the test suite:

```bash
pytest --html=reports/test-report.html --self-contained-html
```

The report file (`test-report.html`) is excluded from Git via `.gitignore`.
