import requests
import json

# Test a single code sample with the API
def test_bug_detection(code_sample):
    url = "http://localhost:8000/detect-bugs"
    payload = {"code": code_sample}
    
    print("Sending code to API:")
    print(code_sample)
    print("\nAPI Response:")
    
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            result = response.json()
            print(json.dumps(result, indent=2))
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"Error: {str(e)}")

# Sample code with multiple bugs
code = """
def process_data(numbers):
    # Uninitialized variable
    total = sum + numbers[0]
    
    # Infinite loop
    i = 0
    while i < len(numbers):
        print(f"Processing {numbers[i]}")
        # Missing increment
    
    # Unreachable code
    return total
"""

if __name__ == "__main__":
    test_bug_detection(code)
