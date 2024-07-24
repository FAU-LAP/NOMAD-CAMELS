import yaml
import jsonschema
from jsonschema import validate
from openapi_schema_validator import OAS30Validator

# Load and parse the OpenAPI YAML file
with open(r'nomad_camels\api\api_schema.yaml', 'r') as file:
    openapi_spec = yaml.safe_load(file)

# Validate the OpenAPI 3.0.3 specification
oas30_validator = OAS30Validator(openapi_spec)
oas30_validator.validate(openapi_spec)

# Extract the schema for Protocols
protocols_schema = openapi_spec['components']['schemas']['Protocols']

# Example of valid input data
valid_data = {
    "name": "Example Protocol",
    "JSON_definition": {"key": "value"}
}

# Example of invalid input data (missing JSON_definition)
invalid_data = {
    "name": "Example Protocol"
    # Missing "JSON_definition"
}

# Example of invalid input data (wrong type for JSON_definition)
invalid_data_wrong_type = {
    "name": "Example Protocol",
    "JSON_definition": "this should be a dict"
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
validate_protocol(invalid_data_wrong_type)  # This should print a validation error message
