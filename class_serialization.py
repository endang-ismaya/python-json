import json
from pprint import pprint
from typing import Union


class Person:
    def __init__(self, first_name: str, last_name: str, age: int) -> None:
        self.first_name = first_name
        self.last_name = last_name
        self.age = age

        self._name: Union[str, None] = None

    @property
    def name(self) -> str:
        if self._name is None:
            self._name = f"{self.first_name.title()} {self.last_name.title()}"

        return self._name


# create a function to serialize Person class
def serialize_person(obj: Person):
    if isinstance(obj, Person):
        return {
            "name": obj.name,
            "age": obj.age,
        }

    raise TypeError("Object is not a Person instance and not serializable")


john = Person(first_name="John", last_name="Doe", age=30)

json_data = json.dumps(john, default=serialize_person)
pprint(json_data)  # '{"name": "John Doe", "age": 30}'
