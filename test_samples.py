"""
Test script to demonstrate how to use the bug detection tool with different code samples.
"""
import os
import subprocess
import json

def run_bug_detection_cli(code_file=None, code_string=None):
    """
    Run the bug detection tool using the command line interface.
    
    Args:
        code_file (str): Path to a Python file to analyze
        code_string (str): Python code string to analyze
    
    Returns:
        dict: The detected bugs and fixes
    """
    command = ["python", "main.py"]
    
    if code_file:
        command.extend(["-f", code_file])
    elif code_string:
        command.extend(["-c", code_string])
    
    # Run the command and capture output
    result = subprocess.run(command, capture_output=True, text=True)
    
    print("Command:", " ".join(command))
    print("Exit code:", result.returncode)
    print("Output:")
    print(result.stdout)
    
    if result.stderr:
        print("Errors:")
        print(result.stderr)
    
    return result.stdout

def test_file_sample(file_path):
    """Test bug detection on a file"""
    print(f"\n{'='*50}")
    print(f"Testing bug detection on file: {file_path}")
    print(f"{'='*50}")
    
    # Print the file contents
    with open(file_path, 'r') as f:
        content = f.read()
    
    print("File contents:")
    print(content)
    print()
    
    # Run the bug detection
    run_bug_detection_cli(code_file=file_path)

def test_string_sample(code_string, description):
    """Test bug detection on a code string"""
    print(f"\n{'='*50}")
    print(f"Testing bug detection on: {description}")
    print(f"{'='*50}")
    
    print("Code:")
    print(code_string)
    print()
    
    # Run the bug detection
    run_bug_detection_cli(code_string=code_string)

def test_api_sample(code_string, description):
    """Test bug detection using the API"""
    import requests
    
    print(f"\n{'='*50}")
    print(f"Testing API with: {description}")
    print(f"{'='*50}")
    
    print("Code:")
    print(code_string)
    print()
    
    # Prepare the request
    url = "http://localhost:8000/detect-bugs"
    payload = {"code": code_string}
    
    try:
        # Send the request
        response = requests.post(url, json=payload)
        
        print(f"API Response (Status: {response.status_code}):")
        if response.status_code == 200:
            result = response.json()
            
            print("\nDetected Bugs:")
            for i, bug in enumerate(result["bugs"], 1):
                print(f"Bug #{i}:")
                print(f"  Type: {bug['type']}")
                print(f"  Location: {bug['location']}")
                print(f"  Description: {bug['description']}")
                print()
            
            print("Suggested Fixes:")
            for i, fix in enumerate(result["fixes"], 1):
                print(f"Fix #{i}:")
                print(f"  Bug: {fix['bug']}")
                print(f"  Suggestion: {fix['suggestion']}")
                print()
        else:
            print(response.text)
    
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    # Ensure the samples directory exists
    samples_dir = os.path.join(os.path.dirname(__file__), "samples")
    
    # Test file samples
    for sample_file in os.listdir(samples_dir):
        if sample_file.endswith(".py"):
            test_file_sample(os.path.join(samples_dir, sample_file))
    
    # Test string samples
    recursive_function = """
def factorial(n):
    # Recursive function without proper base case
    return n * factorial(n-1)
"""
    test_string_sample(recursive_function, "Recursive function without base case")
    
    index_error = """
def get_first_element(lst):
    # Potential index error
    return lst[0]
"""
    test_string_sample(index_error, "Potential index error")
    
    # Test API samples (if API is running)
    try:
        import requests
        response = requests.get("http://localhost:8000/")
        if response.status_code == 200:
            print("\nAPI is running. Testing API samples...")
            
            # Test the API with a complex example
            complex_example = """
class BankAccount:
    def __init__(self, balance):
        # Missing self
        balance = balance
    
    def withdraw(self, amount):
        # Using attribute not initialized in __init__
        if amount <= self.balance:
            self.balance -= amount
            return True
        return False
"""
            test_api_sample(complex_example, "Class with initialization issues")
        else:
            print("\nAPI is not running. Skipping API tests.")
    except:
        print("\nCould not connect to API. Skipping API tests.")
