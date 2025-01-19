import os
from rdflib import Graph, Namespace
from rdflib.namespace import RDF, RDFS, OWL, XSD
import json

# Define paths
script_dir = os.path.dirname(os.path.abspath(__file__))
ontology_path = os.path.join(script_dir, "../ontologies/mesyto.owl.jsonld")
frontend_data_dir = os.path.abspath(os.path.join(script_dir, "../../../frontend/src/data"))
output_file = os.path.join(frontend_data_dir, "form_metadata.json")

# Load ontology
g = Graph()
g.parse(ontology_path, format="json-ld")

# Define namespace
MESYTO = Namespace("http://www.ufz.de/ontologies/2025/mesyto#")

def extract_form_metadata(graph):
    form_metadata = {}

    # Identify all classes in the ontology
    for s, _, _ in graph.triples((None, RDF.type, OWL.Class)):
        class_name = s.split("#")[-1]
        form_metadata[class_name] = {"data_properties": [], "object_properties": []}

        # Extract intrinsic data properties
        for prop, _, domain in graph.triples((None, RDFS.domain, s)):
            range_uri = graph.value(prop, RDFS.range)
            if range_uri and range_uri.startswith(str(XSD)):  # Literal type
                form_metadata[class_name]["data_properties"].append({
                    "name": prop.split("#")[-1],
                    "type": range_uri.split("#")[-1],
                    "label": prop.split("#")[-1].replace("_", " ").capitalize(),
                })

        # Extract object properties (relationships)
        for prop, _, domain in graph.triples((None, RDFS.domain, s)):
            range_uri = graph.value(prop, RDFS.range)
            if range_uri and (range_uri.startswith(str(MESYTO)) or range_uri.startswith(str(OWL))):  # Class type
                form_metadata[class_name]["object_properties"].append({
                    "name": prop.split("#")[-1],
                    "target_class": range_uri.split("#")[-1],
                    "label": prop.split("#")[-1].replace("_", " ").capitalize(),
                })

    return form_metadata

# Generate metadata
form_metadata = extract_form_metadata(g)

# Ensure the frontend data directory exists
os.makedirs(frontend_data_dir, exist_ok=True)

# Save to JSON for frontend
with open(output_file, "w") as f:
    json.dump(form_metadata, f, indent=4)

print(f"Form metadata saved to {output_file}")
