# Foamai API Testing Examples

You can use the following curl commands to test the Foamai bug detection API directly from your terminal.

## Basic API Test

### 1. Check if the API is running

```bash
curl http://localhost:8000/
```

### 2. Test with Uninitialized Variable

```bash
curl -X POST http://localhost:8000/detect-bugs \
  -H "Content-Type: application/json" \
  -d "{\"code\": \"def calculate_total(items):\\n    # Uninitialized variable\\n    total = total + sum(items)\\n    return total\"}"
```

### 3. Test with Infinite Loop

```bash
curl -X POST http://localhost:8000/detect-bugs \
  -H "Content-Type: application/json" \
  -d "{\"code\": \"def find_element(target, data):\\n    i = 0\\n    # Infinite loop - i is never incremented\\n    while i < len(data):\\n        if data[i] == target:\\n            return i\\n    return -1  # Unreachable code\"}"
```

### 4. Test with Type Error

```bash
curl -X POST http://localhost:8000/detect-bugs \
  -H "Content-Type: application/json" \
  -d "{\"code\": \"def process_data(numbers):\\n    # Type error - adding string to int\\n    result = \\\"Total: \\\" + len(numbers)\\n    return result\"}"
```

### 5. Test with Index Error

```bash
curl -X POST http://localhost:8000/detect-bugs \
  -H "Content-Type: application/json" \
  -d "{\"code\": \"def get_elements(data):\\n    # Potential index error if data is empty\\n    first = data[0]\\n    # Potential index error - hardcoded index\\n    last = data[10]\\n    return first, last\"}"
```

## Python Requests Examples

If you prefer using Python, here are some examples:

```python
import requests
import json

# API endpoint
url = "http://localhost:8000/detect-bugs"

# Example 1: Uninitialized Variable
code1 = """
def calculate_total(items):
    # Uninitialized variable
    total = total + sum(items)
    return total
"""

# Example 2: Class with Multiple Issues
code2 = """
class BankAccount:
    def __init__(self, initial_balance):
        # Missing self
        balance = initial_balance
    
    def deposit(self, amount):
        # Using attribute not initialized in __init__
        self.balance += amount
        
    def withdraw(self, amount):
        # Potential attribute error
        if amount <= self.balance:
            self.balance -= amount
            return True
        return False
"""

# Function to test the API
def test_api(code):
    response = requests.post(url, json={"code": code})
    if response.status_code == 200:
        return response.json()
    else:
        return f"Error: {response.status_code}, {response.text}"

# Run tests
result1 = test_api(code1)
print(json.dumps(result1, indent=2))

result2 = test_api(code2)
print(json.dumps(result2, indent=2))
```
