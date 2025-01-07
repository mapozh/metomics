from fastapi import APIRouter, HTTPException
from app.rdf_utils import create_rdf_sample

router = APIRouter(prefix="/metadata", tags=["metadata"])

@router.post("/add-sample")
def add_sample(sample_id: str, name: str, organism: str, library_type: str):
    try:
        graph = create_rdf_sample(sample_id, name, organism, library_type)
        graph.serialize(f"./rdf_data/{sample_id}.ttl", format="turtle")
        return {"message": f"Sample {sample_id} added successfully!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
