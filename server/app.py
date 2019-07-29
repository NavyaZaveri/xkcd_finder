from dotenv import load_dotenv
from sanic import Sanic
from sanic.response import json

import es_api.client

load_dotenv()

from pathlib import Path

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

app = Sanic()

# load configruration from .env configuration environment
es_client = es_api.client.ElasticEngine("stuff")


@app.route("/", methods=["GET"])
async def home(request):
    return json({"hello": "ffsz"})


@app.route("/insert", methods=["POST"])
async def insert_comic(request):
    a = request.json
    es_client.insert(a)
    return json({"msg": "insertion successful"})


@app.route("/search", methods=["GET"])
async def search_comic(request):
    query = request.json["query"]
    results = []
    for match in es_client.search_by(content=query).results():
        results.append(match)
    return json({"results": results})


@app.route("/random", methods=["GET"])
async def random_comic(request):
    """

    :param request:
    :return:
    """


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
