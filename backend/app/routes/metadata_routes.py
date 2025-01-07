from fastapi import APIRouter, HTTPException
from app.rdf_utils import create_rdf_sample, save_rdf_to_graphdb, fetch_rdf_from_graphdb

# Define the API router
router = APIRouter(prefix="/metadata", tags=["metadata"])

@router.post("/add-sample")
def add_sample(sample_id: str, name: str, organism: str, library_type: str):
    """
    Endpoint to add RDF metadata for a sample.
    """
    try:
        # Create RDF graph
        graph = create_rdf_sample(sample_id, name, organism, library_type)

        # Save to GraphDB
        save_rdf_to_graphdb(graph)

        # Return success response
        return {"message": f"Sample {sample_id} added successfully!"}
    except Exception as e:
        # Handle errors
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/fetch-samples")
def fetch_samples():
    """
    Endpoint to fetch metadata samples stored in GraphDB.
    """
    try:
        # Fetch data from GraphDB
        results = fetch_rdf_from_graphdb()

        # Return query results
        return {"data": results}
    except Exception as e:
        # Handle errors
        raise HTTPException(status_code=500, detail=str(e))

