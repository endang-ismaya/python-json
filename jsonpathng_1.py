from jsonpath_ng import parse

document = {
    "person": {
        "name": "Alice Johnson",
        "age": 28,
        "gender": "female",
        "contact": {"email": "alice@example.com", "phone": "555-123-4567"},
        "address": {
            "street": "456 Oak Avenue",
            "city": "Somewhereville",
            "zipcode": "12345",
            "country": "USA",
        },
        "interests": ["reading", "traveling", "gardening"],
    },
    "spouse": {
        "name": "Bob Johnson",
        "age": 32,
        "gender": "male",
        "contact": {"email": "bob@example.com", "phone": "555-987-6543"},
        "address": {
            "street": "789 Pine Street",
            "city": "Anywhere",
            "zipcode": "67890",
            "country": "USA",
        },
        "interests": ["cooking", "photography", "music"],
    },
}

var = "spouse"
result = parse(f"$.{var}.address.zipcode").find(document)
if result:
    # print(result)
    print(result[0].value)  # 67890


addresses = parse("$..address").find(document)
for address in addresses:
    print(address.value)
