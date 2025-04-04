import os
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
import json
import re

# Load environment variables from .env file
load_dotenv()

# Verify the API key is available
api_key = os.environ.get("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY not found in environment variables")

# Now create the OpenAI instance with the key from environment variables
llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.3)

# Chunking function
def chunk_code(code, max_length=500):
    if len(code) <= max_length:
        return [code]
    lines = code.split("\n")
    chunks = []
    current_chunk = ""
    for line in lines:
        if len(current_chunk) + len(line) > max_length and current_chunk:
            chunks.append(current_chunk)
            current_chunk = line
        else:
            current_chunk += "\n" + line if current_chunk else line
    if current_chunk:
        chunks.append(current_chunk)
    return chunks

# Prompt Templates with structured output format
detect_prompt = PromptTemplate(
    input_variables=["code"],
    template="""Analyze this Python code for common bugs:

{code}

Identify bugs such as:
- Uninitialized variables
- Infinite loops
- Unreachable code
- Type errors
- Logic errors

For each bug found, provide:
1. Bug type
2. Location (line number or function)
3. Description of the issue

Format your response as a JSON array of objects with the following structure:
[
  {{
    "type": "bug type",
    "location": "line number or function",
    "description": "detailed description"
  }},
  ...
]

If no bugs are found, return an empty array: []
"""
)

fix_prompt = PromptTemplate(
    input_variables=["bugs"],
    template="""Given these detected bugs:

{bugs}

Suggest fixes for each bug. Format your response as a JSON array of objects with the following structure:
[
  {{
    "bug": "brief description of the bug",
    "suggestion": "detailed fix instructions"
  }},
  ...
]

If no fixes are needed, return an empty array: []
"""
)

# Create chains using the LangChain structure
detect_chain = detect_prompt | llm | StrOutputParser()
fix_chain = fix_prompt | llm | StrOutputParser()

# Main function
def detect_bugs(code_snippet, strip_comments=False):
    """
    Detect bugs in Python code and suggest fixes.
    
    Args:
        code_snippet (str): The Python code to analyze
        strip_comments (bool): Whether to strip comments before analysis to avoid bias
        
    Returns:
        dict: A dictionary containing detected bugs and suggested fixes
    """
    # Optionally strip comments to avoid biasing the LLM
    if strip_comments:
        # Remove single-line comments
        code_without_comments = re.sub(r'#.*$', '', code_snippet, flags=re.MULTILINE)
        # Remove multi-line comments (docstrings)
        code_without_comments = re.sub(r'""".*?"""', '', code_without_comments, flags=re.DOTALL)
        code_without_comments = re.sub(r"'''.*?'''", '', code_without_comments, flags=re.DOTALL)
        chunks = chunk_code(code_without_comments)
    else:
        chunks = chunk_code(code_snippet)
        
    all_bugs = []
    all_fixes = []

    for i, chunk in enumerate(chunks):
        # Run the chains on each chunk
        try:
            bugs_raw = detect_chain.invoke({"code": chunk})
            
            # Try to parse as JSON
            try:
                bugs = json.loads(bugs_raw)
                # Add chunk information to location
                for bug in bugs:
                    if "location" in bug:
                        bug["location"] = f"chunk {i+1}: {bug['location']}"
                    else:
                        bug["location"] = f"chunk {i+1}"
                all_bugs.extend(bugs)
            except json.JSONDecodeError:
                # Fallback if JSON parsing fails - log error but don't print in API mode
                error_msg = f"Could not parse bugs as JSON. Raw output: {bugs_raw[:100]}..."
                all_bugs.append({
                    "type": "Unknown",
                    "location": f"chunk {i+1}",
                    "description": f"Error parsing output: {error_msg}"
                })
            
            # Only get fixes if we found bugs
            if all_bugs:
                fixes_raw = fix_chain.invoke({"bugs": bugs_raw})
                
                # Try to parse as JSON
                try:
                    fixes = json.loads(fixes_raw)
                    all_fixes.extend(fixes)
                except json.JSONDecodeError:
                    # Fallback if JSON parsing fails - log error but don't print in API mode
                    error_msg = f"Could not parse fixes as JSON. Raw output: {fixes_raw[:100]}..."
                    all_fixes.append({
                        "bug": "Unknown",
                        "suggestion": f"Error parsing output: {error_msg}"
                    })
        except Exception as e:
            error_msg = f"Error processing chunk {i+1}: {str(e)}"
            all_bugs.append({
                "type": "Error",
                "location": f"chunk {i+1}",
                "description": error_msg
            })

    return {"bugs": all_bugs, "fixes": all_fixes}

# Run the bug detection if this script is executed directly
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Detect bugs in Python code")
    parser.add_argument("-f", "--file", help="Path to Python file to analyze")
    parser.add_argument("-c", "--code", help="Python code string to analyze")
    parser.add_argument("--strip-comments", action="store_true", help="Strip comments before analysis to avoid bias")
    args = parser.parse_args()
    
    code_to_analyze = None
    
    if args.file:
        try:
            with open(args.file, 'r') as file:
                code_to_analyze = file.read()
            print(f"Analyzing code from file: {args.file}")
        except Exception as e:
            print(f"Error reading file: {str(e)}")
            exit(1)
    elif args.code:
        code_to_analyze = args.code
        print("Analyzing provided code string")
    else:
        # Example code for testing if no input is provided
        code_to_analyze = """def example_function(n):
    # Uninitialized variable
    result = x + n
    
    # Infinite loop
    i = 0
    while i < 10:
        print(result)
        
    return result"""
        print("No input provided. Analyzing example code:")
        print(code_to_analyze)
    
    # Run the bug detection
    result = detect_bugs(code_to_analyze, strip_comments=args.strip_comments)
    
    # Print the results - only in CLI mode
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
