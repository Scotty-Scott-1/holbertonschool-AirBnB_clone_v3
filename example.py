#!/usr/bin/python3
import os
os.environ["HBNB_TYPE_STORAGE"] = "file"
from models import storage
from models.state import State
from models.place import Place

print(os.environ["HBNB_TYPE_STORAGE"])




result = storage.count()
print(result)
