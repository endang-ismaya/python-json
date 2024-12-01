import json
from typing import List

from validate_json_class import validate_object_json


class Product:
    def __init__(
        self,
        productId: int,
        title: str,
        price: "Price",
        inStock: bool,
        categories: List[str],
        reviews: List["Review"],
    ):
        self.productId: int = productId
        self.title: str = title
        self.price: "Price" = price
        self.inStock: bool = inStock
        self.categories: List[str] = categories
        self.reviews: List["Review"] = reviews


class Price:
    def __init__(self, amount: float, currency: str):
        self.amount: float = amount
        self.currency: str = currency


class Review:
    def __init__(self, rating: float, comment: str):
        self.rating: float = rating
        self.comment: str = comment


# Test json file with correct data/schema
# Load JSON data from file
# with open("product_ok.json", "r") as f:
#     product_json = json.load(f)

# # Validate the JSON data against the Product class
# validation_result = validate_object_json(product_json, Product)
# if validation_result is True:
#     print("Valid JSON data")
#     # ... (create Product object if needed) ...
# else:
#     print("Invalid JSON data. Errors:")
#     for error in validation_result:
#         print(f"- {error}")


# Test json file with in-correct data/schema
with open("product_nok1.json", "r") as f:
    product_json1 = json.load(f)
    print(type(product_json1))

validation_result1 = validate_object_json(product_json1, Product)
if validation_result1 is True:
    print("Valid JSON data")
    # ... (create Product object if needed) ...
else:
    print("Invalid JSON data. Errors:")
    for error in validation_result1:
        print(f"- {error}")
