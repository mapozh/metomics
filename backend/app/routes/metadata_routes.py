import os
import logging
from fastapi import APIRouter, HTTPException
from app.rdf_utils import (
    #create_rdf_sample,
    save_rdf_to_graphdb,
    fetch_rdf_from_graphdb,
    load_rdf,
    extract_form_metadata,
)

# Configure logging
logger = logging.getLogger(__name__)

# Define the API router
router = APIRouter(prefix="/metadata", tags=["metadata"])


@router.get("/fetch-samples")
def fetch_samples():
    """
    Endpoint to fetch RDF instances stored in GraphDB.
    """
    try:
        # Fetch data from a specific graph or related to a class
        results = fetch_rdf_from_graphdb()

        if not results:
            logger.warning("No samples found in the repository.")
            return {"data": [], "message": "No samples found."}

        logger.info("Successfully fetched samples from GraphDB.")
        return {"data": results}
    except Exception as e:
        logger.error(f"Error fetching samples: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/form-metadata")
def get_form_metadata():
    """
    Endpoint to dynamically extract and serve form metadata.
    """
    try:
        # Path to the ontology file
        file_path = os.path.join(os.path.dirname(__file__), "../ontologies/mesyto.owl")

        # Load ontology and extract metadata
        graph = load_rdf(file_path)
        metadata = extract_form_metadata(graph)

        if not metadata:
            logger.warning("No metadata extracted from ontology.")
            return {"metadata": [], "message": "No metadata found in ontology."}

        logger.info("Successfully extracted metadata from mesyto.owl.")
        return {"metadata": metadata}
    except FileNotFoundError:
        logger.error("Ontology file mesyto.owl not found.")
        raise HTTPException(status_code=404, detail="Ontology file not found.")
    except Exception as e:
        logger.error(f"Error extracting metadata: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))



@router.post("/add-instance")
def add_instance(instance_data: dict):
    """
    Create an instance in the ontology.
    """
    try:
        # Validate input
        if not instance_data.get("id") or not instance_data.get("class"):
            raise HTTPException(status_code=400, detail="Instance 'id' and 'class' are required.")

        graph = Graph()
        graph.bind("mesyto", URIRef("http://www.ufz.de/ontologies/2025/mesyto#"))

        # Create instance URI
        instance_uri = URIRef(f"http://www.ufz.de/ontologies/2025/mesyto#{instance_data['id']}")
        graph.add((instance_uri, RDF.type, URIRef(instance_data['class'])))

        # Add properties
        for key, value in instance_data.items():
            if key not in ["id", "class"]:
                graph.add((instance_uri, URIRef(key), Literal(value)))

        # Save to GraphDB
        save_rdf_to_graphdb(graph)
        logger.info(f"Instance {instance_data['id']} added successfully.")
        return {"message": f"Instance {instance_data['id']} added successfully!"}
    except HTTPException as e:
        logger.error(f"Validation error: {str(e)}")
        raise e
    except Exception as e:
        logger.error(f"Error adding instance: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

