import os
import logging
from fastapi import APIRouter, HTTPException, Request
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# Load OpenAI API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY is not set in environment variables.")

# Instantiate OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Create FastAPI router
router = APIRouter(prefix="/chatbot", tags=["chatbot"])


@router.post("/query")
async def chatbot_query(request: Request):
    """
    Accept user queries in natural language and return a general response.
    """
    data = await request.json()
    user_query = data.get("query", "")

    if not user_query:
        raise HTTPException(status_code=400, detail="Query is required.")

    try:
        # Generate a general response using OpenAI API
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Ensure this is the correct model
            messages=[{"role": "user", "content": user_query}],
            temperature=0.7,
        )

        # Get the assistant's response
        general_response = response.choices[0].message.content.strip()

        return {"response": general_response}

    except Exception as e:
        logging.exception("Error during chatbot query.")
        raise HTTPException(status_code=500, detail=str(e))

