# Properly Formatted JSON Examples for Foamai API

When testing the API in the Swagger UI or sending requests via curl or other clients, you need to properly format the JSON with escaped newlines. Here are some correctly formatted examples:

## Example 1: Uninitialized Variable

```json
{
  "code": "def calculate_total(items):\n    total = total + sum(items)\n    return total",
  "strip_comments": true
}
```

## Example 2: Infinite Loop

```json
{
  "code": "def find_element(target, data):\n    i = 0\n    while i < len(data):\n        if data[i] == target:\n            return i\n    return -1",
  "strip_comments": true
}
```

## Example 3: Type Error

```json
{
  "code": "def process_data(numbers):\n    result = \"Total: \" + len(numbers)\n    return result",
  "strip_comments": true
}
```

## Example 4: Class with Initialization Issues

```json
{
  "code": "class User:\n    def __init__(self, name):\n        username = name\n    \n    def greet(self):\n        return f'Hello, {self.username}!'",
  "strip_comments": true
}
```

## Your Example (Fixed)

```json
{
  "code": "def calculate_total(items):\n    \n    total = total + sum(items)\n    return total",
  "strip_comments": true
}
```

## Important Notes:

1. All newlines must be replaced with `\n` in the JSON string
2. All quotes within the code must be escaped with a backslash (`\"`)
3. The entire JSON must be valid - no unescaped control characters
4. When using the Swagger UI, paste the entire JSON object including the curly braces
