import os
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
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

# Prompt Templates
detect_prompt = PromptTemplate(
    input_variables=["code"],
    template="""Analyze this Python code for common bugs (e.g., uninitialized variables, infinite loops):

{code}

Return a list of bugs with type, location, and description. Format each bug as:
Type: [bug type], Location: [line or function], Description: [detailed description]
"""
)

fix_prompt = PromptTemplate(
    input_variables=["bugs"],
    template="""Given these detected bugs:
{bugs}

Suggest fixes for each bug. Format each fix as:
Bug: [brief description], Suggestion: [detailed fix instructions]
"""
)

# Create chains using the new LangChain structure
detect_chain = detect_prompt | llm | StrOutputParser()
fix_chain = fix_prompt | llm | StrOutputParser()

# Helper function to parse bug information using regex
def parse_bug_info(text):
    bugs = []
    # Look for patterns like "Type: X, Location: Y, Description: Z"
    bug_entries = re.split(r'\d+\.|\n\n|\n(?=Type:)', text)
    
    for entry in bug_entries:
        entry = entry.strip()
        if not entry:
            continue
            
        bug_info = {"type": "Unknown", "location": "Unknown", "description": "Unknown"}
        
        # Extract type
        type_match = re.search(r'Type:\s*([^,\n]+)', entry)
        if type_match:
            bug_info["type"] = type_match.group(1).strip()
            
        # Extract location
        location_match = re.search(r'Location:\s*([^,\n]+)', entry)
        if location_match:
            bug_info["location"] = location_match.group(1).strip()
            
        # Extract description
        description_match = re.search(r'Description:\s*(.+?)(?=$|\n\n|\n(?=Type:))', entry, re.DOTALL)
        if description_match:
            bug_info["description"] = description_match.group(1).strip()
        elif not type_match and not location_match:
            # If no structured info found, use the whole entry as description
            bug_info["description"] = entry
            
        bugs.append(bug_info)
    
    return bugs

# Helper function to parse fix information using regex
def parse_fix_info(text):
    fixes = []
    # Look for patterns like "Bug: X, Suggestion: Y"
    fix_entries = re.split(r'\d+\.|\n\n|\n(?=Bug:)', text)
    
    for entry in fix_entries:
        entry = entry.strip()
        if not entry:
            continue
            
        fix_info = {"bug": "Unknown", "suggestion": "Unknown"}
        
        # Extract bug
        bug_match = re.search(r'Bug:\s*([^,\n]+)', entry)
        if bug_match:
            fix_info["bug"] = bug_match.group(1).strip()
            
        # Extract suggestion
        suggestion_match = re.search(r'Suggestion:\s*(.+?)(?=$|\n\n|\n(?=Bug:))', entry, re.DOTALL)
        if suggestion_match:
            fix_info["suggestion"] = suggestion_match.group(1).strip()
        elif not bug_match:
            # If no structured info found, use the whole entry as suggestion
            fix_info["suggestion"] = entry
            
        fixes.append(fix_info)
    
    return fixes

# Main function
def detect_bugs(code_snippet):
    chunks = chunk_code(code_snippet)
    all_bugs = []
    all_fixes = []

    for i, chunk in enumerate(chunks):
        # Run the chains on each chunk
        bugs_raw = detect_chain.invoke({"code": chunk})
        fixes_raw = fix_chain.invoke({"bugs": bugs_raw})
        
        # Parse bugs and fixes using the helper functions
        bugs = parse_bug_info(bugs_raw)
        fixes = parse_fix_info(fixes_raw)
        
        # Add chunk information to the location
        for bug in bugs:
            if bug["location"] != "Unknown":
                bug["location"] = f"chunk {i+1}: {bug['location']}"
            else:
                bug["location"] = f"chunk {i+1}"
        
        all_bugs.extend(bugs)
        all_fixes.extend(fixes)

    return {"bugs": all_bugs, "fixes": all_fixes}

# Test with a buggy code example
code = """def process_data(n):
    # This function has several bugs
    
    # Bug 1: Uninitialized variable 'x'
    result = x + n
    
    # Bug 2: Infinite loop - 'i' is never incremented
    i = 0
    while i < 10:
        print(result)
    
    # Bug 3: Unreachable code due to infinite loop
    return result"""

result = detect_bugs(code)
print(json.dumps(result, indent=2))
