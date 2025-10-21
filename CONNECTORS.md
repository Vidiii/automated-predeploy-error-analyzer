# Connectors Specification

### Goal
Easily add new log parsers for other CI/CD tools.

### Contract
Each connector:
- Lives under `src-python/connectors/{tool_name}.py`
- Implements:
  ```python
  def parse(text: str):
      """Yield normalized log events as per docs/log_schema.json"""
