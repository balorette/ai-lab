# AI Lab Development Guide

## Build/Test/Lint Commands
```bash
# Run main application
python3 main.py

# Run sales agent system
python3 src/salesAgent/openai-agents.py

# Run production tests
python3 src/salesAgent/test_production.py

# Syntax check all Python files
find . -name "*.py" -exec python3 -m py_compile {} \;

# Install dependencies
pip install -r requirements.txt
```

## Code Style Guidelines

### Imports
- Standard library imports first, then third-party, then local imports
- Use absolute imports, avoid relative imports
- Group imports with blank lines between groups

### Formatting
- Use 4 spaces for indentation (no tabs)
- Line length: 88-100 characters preferred
- Use double quotes for strings
- Add trailing commas in multi-line structures

### Types & Naming
- Use type hints for function parameters and return values
- Use dataclasses for configuration objects
- Class names: PascalCase (e.g., `SalesAgentSystem`)
- Function/variable names: snake_case (e.g., `generate_email`)
- Constants: UPPER_SNAKE_CASE (e.g., `DEFAULT_MODEL`)

### Error Handling
- Use structured logging with the `logging` module
- Catch specific exceptions, avoid bare `except:`
- Return structured error responses: `{"status": "error", "message": "..."}`
- Log errors with context and use appropriate log levels

### Environment & Configuration
- Use `.env` files for configuration (never commit secrets)
- Validate configuration on startup with descriptive error messages
- Use dataclasses with `from_env()` class methods for config objects