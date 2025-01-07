import requests
from rdflib import Graph, Namespace, Literal, RDF, URIRef
from SPARQLWrapper import SPARQLWrapper, POST, JSON

# GraphDB Configuration
GRAPHDB_ENDPOINT = "http://localhost:7200/repositories/mesyto_repo/statements"

# Namespace
EX = Namespace("http://example.org/rna-seq#")


def create_rdf_sample(sample_id: str, name: str, organism: str, library_type: str) -> Graph:
    """
    Create RDF data for a sample.
    """
    g = Graph()
    # Explicitly bind namespace prefix
    g.bind("ex", EX)

    sample = URIRef(f"http://example.org/rna-seq/{sample_id}")
    g.add((sample, RDF.type, EX.Sample))
    g.add((sample, EX.name, Literal(name)))
    g.add((sample, EX.organism, Literal(organism)))
    g.add((sample, EX.library_type, Literal(library_type)))
    return g


def save_rdf_to_graphdb(graph: Graph):
    """
    Save RDF data to GraphDB repository using raw HTTP requests.
    """
    # Serialize RDF data in Turtle format
    triples = graph.serialize(format="turtle").strip()

    # Remove any @prefix declarations
    triples = "\n".join([line for line in triples.splitlines() if not line.startswith("@prefix")])

    # Format the SPARQL Update query
    query = f"""
    PREFIX ex: <http://example.org/rna-seq#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    INSERT DATA {{
        GRAPH <http://example.org/rna-seq> {{
            {triples}
        }}
    }}
    """.strip()

    # Print query for debugging
    print("\nSPARQL Update Query:")
    print(query)

    # HTTP Headers
    headers = {
        "Content-Type": "application/sparql-update",
        "Content-Length": str(len(query.encode('utf-8')))
    }

    # Send HTTP POST request
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
    SELECT ?s ?p ?o
    FROM <http://example.org/rna-seq>
    WHERE {
        ?s ?p ?o
    }
    LIMIT 10
    """

    # SPARQL Query Endpoint
    sparql = SPARQLWrapper("http://localhost:7200/repositories/mesyto_repo")
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    sparql.addCustomHttpHeader("Content-Type", "application/sparql-query")

    # Execute query and process results
    try:
        results = sparql.query().convert()
        for result in results["results"]["bindings"]:
            print(result)
    except Exception as e:
        print(f"Failed to fetch data: {str(e)}")


if __name__ == "__main__":
    # Create RDF Sample Data
    sample_graph = create_rdf_sample(
        sample_id="sample123",
        name="RNA Sample 1",
        organism="Homo sapiens",
        library_type="Paired-End"
    )

    # Save to GraphDB
    save_rdf_to_graphdb(sample_graph)

    # Query and display data from GraphDB
    print("\nQuery Results:")
    fetch_rdf_from_graphdb()








