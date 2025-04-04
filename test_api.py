import requests
import json

def test_bug_detection_api(code_snippet):
    """
    Test the bug detection API by sending a code snippet and printing the results.
    
    Args:
        code_snippet (str): Python code to analyze for bugs
    """
    url = "http://localhost:8000/detect-bugs"
    
    # Prepare the payload
    payload = {"code": code_snippet}
    
    try:
        # Send the request
        response = requests.post(url, json=payload)
        
        # Check if the request was successful
        if response.status_code == 200:
            # Parse the response
            result = response.json()
            
            # Pretty print the results
            print("\n=== DETECTED BUGS ===")
            if result["bugs"]:
                for i, bug in enumerate(result["bugs"], 1):
                    print(f"Bug #{i}:")
                    print(f"  Type: {bug['type']}")
                    print(f"  Location: {bug['location']}")
                    print(f"  Description: {bug['description']}")
                    print()
            else:
                print("No bugs detected.")
            
            print("=== SUGGESTED FIXES ===")
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
    
    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
    except json.JSONDecodeError:
        print("Error: Could not parse the response as JSON")
    except Exception as e:
        print(f"Unexpected error: {e}")

# Example buggy code to test
buggy_code = """def calculate_sum(n):
    # Uninitialized variable
    total = total + n
    
    # Infinite loop
    i = 0
    while i < 10:
        print(f"Iteration {i}")
    
    return total"""

# Run the test
if __name__ == "__main__":
    print("Testing bug detection API with example code...")
    test_bug_detection_api(buggy_code)
