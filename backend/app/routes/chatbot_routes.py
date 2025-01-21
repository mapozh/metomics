import os
import openai
from fastapi import APIRouter, HTTPException, Request
from dotenv import load_dotenv
import requests

# Load environment variables
load_dotenv()

# Configuration
openai.api_key = os.getenv("OPENAI_API_KEY")
SPARQL_ENDPOINT = os.getenv("GRAPHDB_ENDPOINT")

# Create router
router = APIRouter(prefix="/chatbot", tags=["chatbot"])

@router.post("/query")
async def chatbot_query(request: Request):
    """
    Accept user queries in natural language, generate SPARQL, and return results.
    """
    data = await request.json()
    user_query = data.get("query", "")

    if not user_query:
        raise HTTPException(status_code=400, detail="Query is required.")

    try:
        # Generate SPARQL query using OpenAI GPT
        prompt = f"Generate a SPARQL query for the following natural language question: {user_query}"
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=300,
        )
        sparql_query = response["choices"][0]["text"].strip()

        # Execute SPARQL query on GraphDB
        headers = {"Accept": "application/json"}
        query_response = requests.post(SPARQL_ENDPOINT.replace("/statements", ""), data={"query": sparql_query}, headers=headers)

        if query_response.status_code != 200:
            raise HTTPException(status_code=500, detail="SPARQL query failed.")

        results = query_response.json()

        # Return SPARQL results
        return {"sparql_query": sparql_query, "results": results.get("results", {}).get("bindings", [])}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/insert")
async def insert_data(request: Request):
    """
    Insert missing data into the RDF store using SPARQL INSERT.
    """
    data = await request.json()
    if not data:
        raise HTTPException(status_code=400, detail="Data is required.")

    try:
        # Construct SPARQL INSERT query
        triples = "\n".join(
            [f'<{k}> <http://www.w3.org/2000/01/rdf-schema#{v["predicate"]}> "{v["value"]}" .' for k, v in
             data.items()])
        sparql_insert = f"""
        INSERT DATA {{
            {triples}
        }}
        """

        headers = {"Content-Type": "application/sparql-update"}
        response = requests.post(SPARQL_ENDPOINT, data=sparql_insert, headers=headers)

        if response.status_code != 204:  # 204 is the success status code for SPARQL updates
            raise HTTPException(status_code=500, detail="SPARQL INSERT failed.")

        return {"message": "Data inserted successfully."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
