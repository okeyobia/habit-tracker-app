# Running Backend Tests

This guide explains how to run the backend tests for the FastAPI habit tracker project.

## 1. Install Dependencies

Make sure you have installed all dependencies using uv:

```sh
uv pip install -r pyproject.toml
```

Or, if using pip:

```sh
pip install -r requirements.txt
```

## 2. Set Up Environment Variables

Copy the example environment file:

```sh
cp .env.example .env
```

## 3. Run the Tests

From the backend directory, run:

```sh
pytest
```

This will discover and run all tests in the `tests/` folder.

---

If you encounter issues with the database, ensure you are using the test database configuration as in the provided test file.
