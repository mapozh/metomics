import os
import requests
from rdflib import Graph, Namespace, Literal, RDF, URIRef
from SPARQLWrapper import SPARQLWrapper, JSON
#from pyshacl import validate
from dotenv import load_dotenv
import json

# GraphDB Configuration
load_dotenv()

# GraphDB Configuration
GRAPHDB_ENDPOINT = os.getenv("GRAPHDB_ENDPOINT")
if not GRAPHDB_ENDPOINT:
    raise ValueError("GRAPHDB_ENDPOINT environment variable is not set")

# Namespace Configuration
MESYTO_NAMESPACE = os.getenv("NAMESPACE_MESYTO")
if not MESYTO_NAMESPACE:
    raise ValueError("NAMESPACE_MESYTO environment variable is not set")

MESYTO = Namespace(MESYTO_NAMESPACE)


def create_rdf_sample(sample_id: str, name: str, organism: str, library_type: str) -> Graph:
    """
    Create RDF data for a sample.
    """
    g = Graph()
    g.bind("mesyto.owl", MESYTO)

    sample = URIRef(f"{MESYTO_NAMESPACE}Sample/{sample_id}")
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
    PREFIX mesyto.owl: <{MESYTO_NAMESPACE}>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    INSERT DATA {{
        GRAPH <{MESYTO_NAMESPACE}> {{
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
    query = f"""
    PREFIX mesyto.owl: <{MESYTO_NAMESPACE}>
    SELECT ?s ?p ?o
    FROM <{MESYTO_NAMESPACE}>
    WHERE {{
        ?s ?p ?o
    }}
    LIMIT 10
    """

    sparql = SPARQLWrapper(GRAPHDB_ENDPOINT.replace("/statements", ""))
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    sparql.addCustomHttpHeader("Content-Type", "application/sparql-query")

    try:
        results = sparql.query().convert()
        for result in results["results"]["bindings"]:
            print(result)
    except Exception as e:
        print(f"Failed to fetch data: {str(e)}")

import os
from rdflib import Graph

def load_rdf(file_name: str) -> Graph:
    """
    Load RDF/OWL file into an RDF graph.
    """
    # Construct the absolute path
    file_path = os.path.abspath(file_name)
    print(f"Resolved file path: {file_path}")  # Debug statement

    g = Graph()
    try:
        g.parse(file_path, format="xml")
        print(f"Successfully loaded OWL file: {file_path}")
    except Exception as e:
        print(f"Failed to load OWL file: {e}")
        raise e

    return g


def extract_form_metadata(graph: Graph):
    """
    Extract classes, subclasses, and properties from the OWL ontology.
    """
    query = f"""
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    PREFIX mesyto: <{MESYTO_NAMESPACE}>

    SELECT ?type ?entity ?domain ?range ?label ?comment ?superclass
    WHERE {{
        {{
            ?entity a owl:Class .
            BIND("Class" AS ?type)
            OPTIONAL {{ ?entity rdfs:label ?label . }}
            OPTIONAL {{ ?entity rdfs:comment ?comment . }}
            OPTIONAL {{ ?entity rdfs:subClassOf ?superclass . }}
        }}
    }}
    """.strip()  # Ensures no trailing whitespace

    # Debugging statements for query verification
    print("==== DEBUG: SPARQL Query Length ====")
    print(f"Query Length: {len(query)}")
    print("==== DEBUG: SPARQL Query ====")
    print(query)
    print("===================================")

    try:
        query_results = graph.query(query)
        print("==== DEBUG: Raw Query Results ====")
        print(query_results)
        print("==================================")

        results = []
        for row in query_results:
            print(f"==== DEBUG: Processing Row ====\nRow: {row}")
            results.append({
                "type": str(row.type),
                "name": str(row.entity),
                "domain": str(row.domain) if row.domain else None,
                "range": str(row.range) if row.range else None,
                "label": str(row.label) if row.label else None,
                "comment": str(row.comment) if row.comment else None,
                "superclass": str(row.superclass) if row.superclass else None,
            })

        print("==== DEBUG: Processed Results ====")
        print(results)
        print("==================================")

        return results
    except Exception as e:
        print("==== ERROR: During SPARQL Query Execution ====")
        print(f"Error: {e}")
        print("=============================================")
        raise


if __name__ == "__main__":
    graph = load_rdf("app/ontologies/mesyto.owl")
    print(f"Number of triples in graph: {len(graph)}")

    # Print all triples for debugging
    for s, p, o in graph:
        print(f"Triple: {s} {p} {o}")










