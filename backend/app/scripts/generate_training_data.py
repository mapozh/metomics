import json
from app.rdf_utils import load_rdf, extract_form_metadata

MESYTO_NAMESPACE = "http://example.org/mesyto#"

def generate_training_data(ontology_file: str, output_file: str):
    graph = load_rdf(ontology_file)
    metadata = extract_form_metadata(graph)

    training_data = []

    for entity in metadata:
        if entity["type"] == "Class":
            prompt = f"What are all instances of {entity['label']}?"
            completion = f"SELECT ?instance WHERE {{ ?instance a <{entity['name']}> . }}"
            training_data.append({
                "messages": [
                    {"role": "system", "content": "You are a SPARQL assistant for the MESYTO ontology."},
                    {"role": "user", "content": prompt},
                    {"role": "assistant", "content": completion}
                ]
            })

        elif entity["type"] == "ObjectProperty":
            prompt = f"What is the {entity['label']} of a {entity['domain']}?"
            completion = f"SELECT ?value WHERE {{ ?instance <{entity['name']}> ?value . FILTER EXISTS {{ ?instance a <{entity['domain']}> . }} }}"
            training_data.append({
                "messages": [
                    {"role": "system", "content": "You are a SPARQL assistant for the MESYTO ontology."},
                    {"role": "user", "content": prompt},
                    {"role": "assistant", "content": completion}
                ]
            })

    with open(output_file, "w") as f:
        for item in training_data:
            f.write(json.dumps(item) + "\n")

output_file = "rdf_data/training_data.jsonl"
generate_training_data("app/ontologies/mesyto.owl", output_file)
print(f"Training data has been saved to {output_file}")
