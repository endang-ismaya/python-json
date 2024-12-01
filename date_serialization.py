import json
from json import JSONEncoder
from datetime import datetime, date


# create custom encoder for date
class CustomEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, date) or isinstance(obj, datetime):
            return obj.isoformat()

        return super().default(obj)


dog_data = {"name": "Spot", "breed": "Dalmatian", "birthday": date(2019, 5, 12)}

# json.dumps(dog_data) # this will catch an error for the date
json_data = json.dumps(dog_data, cls=CustomEncoder)
print(json_data)  # {"name": "Spot", "breed": "Dalmatian", "birthday": "2019-05-12"}
