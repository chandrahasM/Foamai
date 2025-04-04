"""
Comprehensive API Test Script for Foamai Bug Detection Tool

This script tests the API with various code samples and saves the results to a file.
"""
import requests
import json
import os
from datetime import datetime

# API endpoint
API_URL = "http://localhost:8000/detect-bugs"
OUTPUT_DIR = "api_test_results"

# Create output directory if it doesn't exist
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Function to test the API with a code sample and save results to a file
def test_api(code, description):
    print(f"\nTesting: {description}")
    
    # Prepare the request
    payload = {"code": code}
    
    try:
        # Send the request
        response = requests.post(API_URL, json=payload)
        
        # Check if the request was successful
        if response.status_code == 200:
            result = response.json()
            
            # Save results to a file
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{OUTPUT_DIR}/{description.replace(' ', '_').lower()}_{timestamp}.json"
            
            with open(filename, 'w') as f:
                json.dump({
                    "description": description,
                    "code": code,
                    "result": result
                }, f, indent=2)
            
            # Print summary
            bug_count = len(result.get("bugs", []))
            fix_count = len(result.get("fixes", []))
            print(f"  Found {bug_count} bugs and {fix_count} fixes")
            print(f"  Results saved to: {filename}")
            
            return result
        else:
            print(f"  Error: Received status code {response.status_code}")
            print(f"  {response.text}")
            return None
    
    except Exception as e:
        print(f"  Error making request: {e}")
        return None

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
    print(f"Results will be saved to the '{OUTPUT_DIR}' directory")
    
    # Test if the API is running
    try:
        response = requests.get("http://localhost:8000/")
        if response.status_code == 200:
            print("API is running!")
            
            # Run the tests
            results = []
            results.append(test_api(sample1, "Uninitialized Variable"))
            results.append(test_api(sample2, "Infinite Loop"))
            results.append(test_api(sample3, "Type Error"))
            results.append(test_api(sample4, "Index Error"))
            results.append(test_api(sample5, "Class with Multiple Issues"))
            results.append(test_api(sample6, "Logic Errors"))
            results.append(test_api(sample7, "Complex Function with Multiple Issues"))
            
            # Print summary
            print("\nTest Summary:")
            for i, (sample, description) in enumerate(zip(
                [sample1, sample2, sample3, sample4, sample5, sample6, sample7],
                ["Uninitialized Variable", "Infinite Loop", "Type Error", "Index Error", 
                 "Class with Multiple Issues", "Logic Errors", "Complex Function with Multiple Issues"]
            )):
                if results[i]:
                    bug_count = len(results[i].get("bugs", []))
                    fix_count = len(results[i].get("fixes", []))
                    print(f"  {description}: {bug_count} bugs, {fix_count} fixes")
                else:
                    print(f"  {description}: Failed")
            
            print("\nAll test results have been saved to individual files in the '{OUTPUT_DIR}' directory.")
            print("You can open these files to see the complete API responses.")
        else:
            print(f"API returned status code {response.status_code}")
    except Exception as e:
        print(f"Error connecting to API: {e}")
        print("Make sure the API is running with 'python api.py'")
