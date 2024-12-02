from jsonschema import Draft202012Validator, ValidationError, validate

schema = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "type": "object",
    "properties": {"date": {"type": "string", "format": "date"}},
}

document = {"date": "2024-07-18"}

try:
    validate(
        document, schema, format_checker=Draft202012Validator.FORMAT_CHECKER
    )
    print("The document is valid against the schema")
except ValidationError as e:
    print(f"The document is not valid against the schema: {e}")
