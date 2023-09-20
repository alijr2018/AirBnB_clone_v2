#!/usr/bin/python3
"""This module to change storage type directly by
using an environment variable"""


import os

storage = os.getenv('HBNB_TYPE_STORAGE')
if storage == 'db':
    from models.engine.db_storage import DBStorage
    storage = DBStorage()

else:
    from models.engine.file_storage import FileStorage
    storage = FileStorage()
storage.reload()