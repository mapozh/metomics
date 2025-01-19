import os
import requests
from rdflib import Graph, Namespace, Literal, RDF, URIRef
from SPARQLWrapper import SPARQLWrapper, JSON
from pyshacl import validate

# GraphDB Configuration
GRAPHDB_ENDPOINT = (
    "http://localhost:7200/repositories/mesyto_repo/statements"
)

# Updated Namespace
MESYTO = Namespace("http://www.ufz.de/ontologies/2025/mesyto#")


def create_rdf_sample(sample_id: str, name: str, organism: str, library_type: str) -> Graph:
    """
    Create RDF data for a sample.
    """
    g = Graph()
    g.bind("mesyto.owl", MESYTO)

    sample = URIRef(f"http://www.ufz.de/ontologies/2025/mesyto#Sample/{sample_id}")
    g.add((sample, RDF.type, MESYTO.Sample))
    g.add((sample, MESYTO.name, Literal(name)))
    g.add((sample, MESYTO.organism, Literal(organism)))
    g.add((sample, MESYTO.library_type, Literal(library_type)))
    return g


def save_rdf_to_graphdb(graph: Graph):
    """
    Save RDF data to GraphDB repository using raw HTTP requests.
    """
    triples = graph.serialize(format="turtle").strip()
    triples = "\n".join(
        [line for line in triples.splitlines() if not line.startswith("@prefix")]
    )

    query = f"""
    PREFIX mesyto.owl: <http://www.ufz.de/ontologies/2025/mesyto#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    INSERT DATA {{
        GRAPH <http://www.ufz.de/ontologies/2025/mesyto> {{
            {triples}
        }}
    }}
    """

    headers = {
        "Content-Type": "application/sparql-update",
        "Content-Length": str(len(query.encode("utf-8"))),
    }

    try:
        response = requests.post(GRAPHDB_ENDPOINT, data=query, headers=headers)
        response.raise_for_status()
        print("RDF data successfully saved to GraphDB.")
    except requests.exceptions.HTTPError as e:
        print(f"Failed to save RDF data: {e}")
        print(f"Response: {response.text}")


def fetch_rdf_from_graphdb():
    """
    Fetch data from GraphDB repository.
    """
    query = """
    PREFIX mesyto.owl: <http://www.ufz.de/ontologies/2025/mesyto#>
    SELECT ?s ?p ?o
    FROM <http://www.ufz.de/ontologies/2025/mesyto>
    WHERE {
        ?s ?p ?o
    }
    LIMIT 10
    """

    sparql = SPARQLWrapper("http://localhost:7200/repositories/mesyto_repo")
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    sparql.addCustomHttpHeader("Content-Type", "application/sparql-query")

    try:
        results = sparql.query().convert()
        for result in results["results"]["bindings"]:
            print(result)
    except Exception as e:
        print(f"Failed to fetch data: {str(e)}")


def load_rdf(file_name: str) -> Graph:
    """
    Load RDF/OWL file into an RDF graph.
    """
    # Ensure the file path is absolute
    file_path = os.path.abspath(file_name)
    g = Graph()

    try:
        g.parse(file_path, format="xml")
        print(f"Successfully loaded OWL file: {file_name}")
    except Exception as e:
        print(f"Failed to load OWL file: {e}")
        raise e

    return g



import logging

logger = logging.getLogger(__name__)

def extract_form_metadata(graph: Graph):
    """
    Extract classes, subclasses, and properties from the OWL ontology.
    """
    query = """
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    PREFIX mesyto: <http://www.ufz.de/ontologies/2025/mesyto#>

    SELECT ?type ?entity ?domain ?range ?label ?comment ?superclass
    WHERE {
        {
            ?entity a owl:Class .
            BIND("Class" AS ?type)
            OPTIONAL { ?entity rdfs:label ?label . }
            OPTIONAL { ?entity rdfs:comment ?comment . }
            OPTIONAL { ?entity rdfs:subClassOf ?superclass . }
        }

    }
    """
    logger.info("Executing SPARQL query...")
    try:
        query_results = graph.query(query)
    except Exception as e:
        logger.error(f"Error during SPARQL query execution: {e}")
        raise

    logger.info("Query executed successfully, processing results...")
    results = []
    for row in query_results:
        logger.debug(f"Processing row: {row}")
        results.append({
            "type": str(row.type),
            "name": str(row.entity),
            "domain": str(row.domain) if row.domain else None,
            "range": str(row.range) if row.range else None,
            "label": str(row.label) if row.label else None,
            "comment": str(row.comment) if row.comment else None,
            "superclass": str(row.superclass) if row.superclass else None,
        })

    logger.info("Metadata extraction completed successfully.")
    return results





import json

if __name__ == "__main__":
    graph = load_rdf("mesyto.owl")
    metadata = extract_form_metadata(graph)
    with open("form_metadata.json", "w") as f:
        json.dump(metadata, f, indent=4)
    print("Metadata saved to form_metadata.json.")










