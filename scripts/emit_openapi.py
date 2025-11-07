from fastapi import FastAPI
from app.main import app  # assumes app is defined there

import json
print(json.dumps(app.openapi(), indent=2))
