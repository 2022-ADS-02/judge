from flask import Flask
from flask import request
from flask import json
import execute
from secure_test import execute_secure

app = Flask(__name__)


@app.route('/')
def home():
    return 'Hello, World!'


@app.route('/judge', methods=['POST'])
def judge():
    data = request.get_json()

    language = data["language"]
    code = data["code"]
    samples_text = data["samples_text"]

    result = execute_secure(code, language, samples_text)
    return json.dumps(result)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=9001)

"""
import execute
from typing import List
from pydantic import BaseModel
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


class SampleData(BaseModel):
    input: str
    out: str


class Samples_text(BaseModel):
    language: str
    code: str
    sample: List[SampleData]


@app.post("/judge")
async def get_body(data: Samples_text):
    
"""
