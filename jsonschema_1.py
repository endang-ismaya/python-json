from jsonschema import ValidationError, validate

document = {
    "name": "S&P 500 Index Fund",
    "symbol": "SPY",
    "price": 420.50,
    "currency": "USD",
    "inceptionDate": "1993-01-22",
}

schema = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "symbol": {"type": "string"},
        "price": {"type": "number"},
        "currency": {"type": "string"},
        "inceptionDate": {"type": "string", "format": "date"},
    },
    "required": ["name", "symbol", "price", "currency", "inceptionDate"],
}

try:
    validate(document, schema)
    print("The document is valid against the schema")
except ValidationError as e:
    print(f"The document is not valid against the schema: {e}")
