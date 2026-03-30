#!/bin/bash
# Run all backend tests for the FastAPI habit tracker project using uv
set -e

# Move to backend root directory
cd "$(dirname "$0")/.."

# Ensure uv is installed
if ! command -v uv &> /dev/null; then
  echo "uv is not installed. Please install uv: https://github.com/astral-sh/uv"
  exit 1
fi

# Create uv virtual environment if not present
if [ ! -d ".venv" ]; then
  echo "Creating uv virtual environment..."
  uv venv .venv
fi

# Activate virtual environment
source .venv/bin/activate

# Install dependencies if needed
if [ ! -f ".venv/.deps_installed" ]; then
  echo "Installing dependencies with uv..."
  uv pip install -r pyproject.toml
  touch .venv/.deps_installed
fi

# Export environment variables from .env if present
if [ -f .env ]; then
  export $(grep -v '^#' .env | xargs)
fi


# Run pytest using the venv's python explicitly
if [ ! -x ".venv/bin/python" ]; then
  echo "Python executable not found in .venv/bin/python."
  exit 1
fi

echo "Running tests with .venv/bin/python -m pytest..."
.venv/bin/python -m pytest tests
exit $?

# Run pytest
echo "Running backend tests..."
pytest
