#!/usr/bin/python3
import os
os.environ["HBNB_TYPE_STORAGE"] = "db"
from models import storage
from models.state import State
from models.place import Place

print(os.environ["HBNB_TYPE_STORAGE"])




result = storage.get(State, "0e391e25-dd3a-45f4-bce3-4d1dea83f3c7")
print(result)
