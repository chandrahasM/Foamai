# Foamai - Python Bug Detection Tool

A Python tool that uses LangChain and OpenAI to detect and fix bugs in Python code snippets.

## Setup

1. Clone this repository
2. Create a virtual environment:
   ```
   python -m venv venv
   ```
3. Activate the virtual environment:
   - Windows: `.\venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`
4. Install the required packages:
   ```
   pip install -r requirements.txt
   ```
5. Set your OpenAI API key in a `.env` file in the project root:
   ```
   OPENAI_API_KEY=your-api-key-here
   ```

## Usage

### Command Line Interface

Run the `main.py` script to analyze a Python code snippet for bugs:

```
python main.py
```

The script will analyze the provided code snippet and output detected bugs and suggested fixes in JSON format.

### REST API

Foamai also provides a REST API using FastAPI. To start the API server:

```
python api.py
```

This will start a server at http://localhost:8000.

#### API Endpoints

- `GET /` - Welcome message
- `POST /detect-bugs` - Detect bugs in Python code

Example API request using curl:

```bash
curl -X 'POST' \
  'http://localhost:8000/detect-bugs' \
  -H 'Content-Type: application/json' \
  -d '{
    "code": "def process_data(n):\n    result = x + n\n    i = 0\n    while i < 10:\n        print(result)\n    return result"
  }'
```

You can also access the interactive API documentation at http://localhost:8000/docs.

## Features

- Detects common Python bugs (uninitialized variables, infinite loops, etc.)
- Provides detailed bug information including type, location, and description
- Suggests fixes for each detected bug
- Handles large code snippets by chunking them into manageable pieces
- REST API for integration with other applications
- Interactive API documentation with Swagger UI
