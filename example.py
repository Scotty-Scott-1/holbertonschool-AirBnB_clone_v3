#!/usr/bin/python3
import os
os.environ["HBNB_TYPE_STORAGE"] = "db"
from models import storage
from models.state import State
from models.place import Place

print(os.environ["HBNB_TYPE_STORAGE"])



print(storage.all(State))


"""
result = storage.get(State, "f779ec7f-bca4-4049-ac33-80b75dae2f41")
print(result)
"""
