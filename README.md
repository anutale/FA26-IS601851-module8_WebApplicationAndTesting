# FA26-IS601851 Module 8: Web Application and Testing

A FastAPI-based calculator application that exposes arithmetic operations through REST endpoints and provides a simple browser-based interface for basic calculations. The project is designed as a practical example of building a web application, validating requests, returning structured responses, and running tests in a Python environment.

## Overview

This project demonstrates:

- A Python web API built with FastAPI
- Form validation using Pydantic models
- A simple HTML front-end served by Jinja2 templates
- Reusable arithmetic logic in a dedicated operations module
- Docker containerization for local development and deployment
- CI/CD automation through GitHub Actions

The application performs four fundamental arithmetic operations:

- Addition
- Subtraction
- Multiplication
- Division

## Tech Stack

- Python 3.10
- FastAPI
- Uvicorn
- Jinja2
- Pydantic
- pytest
- Docker / Docker Compose
- Playwright (included in dependencies for web testing support)

## Project Structure

```text
.
├── Dockerfile
├── LICENSE
├── README.md
├── docker-compose.yml
├── main.py
├── pytest.ini
├── requirements.txt
├── operations/
│   └── __init__.py
├── templates/
│   └── index.html
├── .github/
│   └── workflows/
│       └── test.yml
└── .vscode/
    └── settings.json
```

## Application Behavior

### Front-end UI

The root route (`GET /`) serves a simple calculator UI from `templates/index.html`. Users can enter two numeric values and click buttons to perform arithmetic operations in the browser.

### API Endpoints

The application exposes the following endpoints:

- `GET /` — returns the HTML calculator page
- `POST /add` — adds two numbers
- `POST /subtract` — subtracts one number from another
- `POST /multiply` — multiplies two numbers
- `POST /divide` — divides one number by another

Each operation accepts a JSON body in this format:

```json
{
  "a": 10,
  "b": 5
}
```

Example successful response:

```json
{
  "result": 15.0
}
```

Example error response:

```json
{
  "error": "Cannot divide by zero!"
}
```

## Arithmetic Module

The `operations` package contains reusable arithmetic functions:

- `add(a, b)`
- `subtract(a, b)`
- `multiply(a, b)`
- `divide(a, b)`

The division function raises a `ValueError` when the divisor is zero to prevent invalid calculations.

## Requirements

Make sure Python 3.10+ is installed before starting the project.

## Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/anutale/FA26-IS601851-module8_WebApplicationAndTesting.git
cd FA26-IS601851-module8_WebApplicationAndTesting
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate
```

On Windows PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the application

```bash
uvicorn main:app --reload
```

Then open:

```text
http://127.0.0.1:8000/
```

## Docker Setup

### Build the Docker image

```bash
docker build -t fastapi-calculator .
```

### Run the container

```bash
docker run -d -p 8000:8000 --name fastapi-calculator fastapi-calculator
```

Open the app in a browser at:

```text
http://localhost:8000/
```

### Docker Compose

This project includes a `docker-compose.yml` file for easier local orchestration:

```bash
docker compose up --build
```

To stop the container:

```bash
docker compose down
```

## API Examples

### Addition

```bash
curl -X POST "http://127.0.0.1:8000/add" \
  -H "Content-Type: application/json" \
  -d '{"a": 20, "b": 5}'
```

Response:

```json
{"result":25.0}
```

### Subtraction

```bash
curl -X POST "http://127.0.0.1:8000/subtract" \
  -H "Content-Type: application/json" \
  -d '{"a": 20, "b": 5}'
```

### Multiplication

```bash
curl -X POST "http://127.0.0.1:8000/multiply" \
  -H "Content-Type: application/json" \
  -d '{"a": 20, "b": 5}'
```

### Division

```bash
curl -X POST "http://127.0.0.1:8000/divide" \
  -H "Content-Type: application/json" \
  -d '{"a": 20, "b": 5}'
```

## Testing

The project is configured to use `pytest` with a `pytest.ini` setup. To run tests:

```bash
pytest
```

For more detailed reporting with coverage:

```bash
pytest --cov=.
```

The repository also includes a GitHub Actions workflow under `.github/workflows/test.yml` that runs automated validation for pushes and pull requests.

## CI/CD

The pipeline is designed to:

1. Install dependencies
2. Run test suites
3. Build the Docker image
4. Perform Trivy vulnerability scanning
5. Push a production image when code is merged to the main branch

## Notes

- The application uses FastAPI request validation to reject malformed input and return useful error details.
- The browser interface provides a simple way to interact with the API without using curl.
- The Docker setup exposes the application on port `8000`.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Summary

This project serves as a compact example of building a modern Python web application with FastAPI, containerizing it with Docker, and integrating testing and CI/CD workflows. It is suitable for learning API design, validation, UI integration, and deployment basics.
