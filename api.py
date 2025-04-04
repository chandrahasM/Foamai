import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import uvicorn
from main import detect_bugs

# Load environment variables from .env file
load_dotenv()

# Verify the API key is available
api_key = os.environ.get("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY not found in environment variables")

# Create FastAPI app
app = FastAPI(
    title="Foamai - Python Bug Detection API",
    description="API for detecting and fixing bugs in Python code",
    version="1.0.0"
)

# Define request and response models
class CodeRequest(BaseModel):
    code: str
    strip_comments: Optional[bool] = True  # Make it optional with a default value
    
class BugInfo(BaseModel):
    type: str
    location: str
    description: str
    
class FixInfo(BaseModel):
    bug: str
    suggestion: str
    
class BugResponse(BaseModel):
    bugs: List[BugInfo]
    fixes: List[FixInfo]

@app.get("/")
async def root():
    return {"message": "Welcome to Foamai - Python Bug Detection API"}

@app.post("/detect-bugs", response_model=BugResponse)
async def api_detect_bugs(request: CodeRequest):
    try:
        # Handle the case where strip_comments might be None
        strip_comments = request.strip_comments if request.strip_comments is not None else True
        
        # Call the bug detection function from main.py with the strip_comments parameter
        result = detect_bugs(request.code, strip_comments=strip_comments)
        
        # Convert the result to the expected response format
        response = BugResponse(
            bugs=[BugInfo(**bug) for bug in result["bugs"]],
            fixes=[FixInfo(**fix) for fix in result["fixes"]]
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error detecting bugs: {str(e)}")

# Run the API server when the script is executed directly
if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
