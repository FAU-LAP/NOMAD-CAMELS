import yaml
from openapi_spec_validator import openapi_v3_spec_validator
import jsonschema
from jsonschema import validate

import os
print("Current Working Directory:", os.getcwd())
# Load and parse the OpenAPI YAML file
with open(r'nomad_camels\api\api_schema.yaml', 'r') as file:
    openapi_spec = yaml.safe_load(file)

# Validate the OpenAPI specification
openapi_v3_spec_validator.validate(openapi_spec)

# Extract the schema for Protocols
protocols_schema = openapi_spec['components']['schemas']['Protocols']

# Example of valid input data
valid_data = {
    "name": "Example Protocol",
    "JSON_definition": "{\"key\": \"value\"}"
}

# Example of invalid input data
invalid_data = {
    "name": "Example Protocol"
    # Missing "JSON_definition"
}

# Function to validate input data
def validate_protocol(data):
    try:
        validate(instance=data, schema=protocols_schema)
        print("Validation successful!")
    except jsonschema.exceptions.ValidationError as e:
        print(f"Validation error: {e.message}")

# Validate the example data
validate_protocol(valid_data)  # This should print "Validation successful!"
validate_protocol(invalid_data)  # This should print a validation error message