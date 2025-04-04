"""
API Test Samples for Foamai Bug Detection Tool

This script contains various code samples with different types of bugs
that you can use to test the Foamai API.
"""
import requests
import json

# API endpoint
API_URL = "http://localhost:8000/detect-bugs"

# Function to test the API with a code sample
def test_api(code, description):
    print(f"\n{'='*60}")
    print(f"Testing: {description}")
    print(f"{'='*60}")
    
    print("Code sample:")
    print(code)
    print()
    
    # Prepare the request
    payload = {"code": code}
    
    try:
        # Send the request
        response = requests.post(API_URL, json=payload)
        
        # Check if the request was successful
        if response.status_code == 200:
            result = response.json()
            
            # Print the results
            print("API Response:")
            print(json.dumps(result, indent=2))
            
            # Print in a more readable format
            print("\nDetected Bugs:")
            if result["bugs"]:
                for i, bug in enumerate(result["bugs"], 1):
                    print(f"Bug #{i}:")
                    print(f"  Type: {bug['type']}")
                    print(f"  Location: {bug['location']}")
                    print(f"  Description: {bug['description']}")
                    print()
            else:
                print("No bugs detected.")
            
            print("Suggested Fixes:")
            if result["fixes"]:
                for i, fix in enumerate(result["fixes"], 1):
                    print(f"Fix #{i}:")
                    print(f"  Bug: {fix['bug']}")
                    print(f"  Suggestion: {fix['suggestion']}")
                    print()
            else:
                print("No fixes suggested.")
        else:
            print(f"Error: Received status code {response.status_code}")
            print(response.text)
    
    except Exception as e:
        print(f"Error making request: {e}")

# Sample 1: Uninitialized Variable
sample1 = """
def calculate_total(items):
    # Uninitialized variable
    total = total + sum(items)
    return total
"""

# Sample 2: Infinite Loop
sample2 = """
def find_element(target, data):
    i = 0
    # Infinite loop - i is never incremented
    while i < len(data):
        if data[i] == target:
            return i
    return -1  # Unreachable code
"""

# Sample 3: Type Error
sample3 = """
def process_data(numbers):
    # Type error - adding string to int
    result = "Total: " + len(numbers)
    return result
"""

# Sample 4: Index Error
sample4 = """
def get_elements(data):
    # Potential index error if data is empty
    first = data[0]
    # Potential index error - hardcoded index
    last = data[10]
    return first, last
"""

# Sample 5: Class with Multiple Issues
sample5 = """
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

# Sample 6: Logic Errors
sample6 = """
def find_max(numbers):
    # Logic error in initialization
    max_value = 0
    
    for num in numbers:
        # Logic error in comparison (should be >)
        if num < max_value:
            max_value = num
    
    return max_value
"""

# Sample 7: Complex Function with Multiple Issues
sample7 = """
def process_user_data(users):
    results = []
    
    for i in range(len(users)):
        # Uninitialized variable
        user_data = previous_data
        
        # Type error
        user_id = "ID: " + i
        
        # Potential index error
        next_user = users[i+1]
        
        # Logic error - condition always True
        if user_id != None:
            # Infinite loop
            counter = 0
            while counter < 10:
                print(f"Processing {user_id}")
                # Missing increment
                
            # Unreachable code
            results.append(user_data)
    
    return results
"""

# Run the tests
if __name__ == "__main__":
    print("Testing Foamai Bug Detection API...")
    print("API URL:", API_URL)
    
    # Test if the API is running
    try:
        response = requests.get("http://localhost:8000/")
        if response.status_code == 200:
            print("API is running!")
            
            # Run the tests
            test_api(sample1, "Uninitialized Variable")
            test_api(sample2, "Infinite Loop")
            test_api(sample3, "Type Error")
            test_api(sample4, "Index Error")
            test_api(sample5, "Class with Multiple Issues")
            test_api(sample6, "Logic Errors")
            test_api(sample7, "Complex Function with Multiple Issues")
        else:
            print(f"API returned status code {response.status_code}")
    except Exception as e:
        print(f"Error connecting to API: {e}")
        print("Make sure the API is running with 'python api.py'")
