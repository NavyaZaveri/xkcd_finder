from sanic import Sanic
from sanic.response import json

from es_api.client import ElasticEngine

app = Sanic()
es_client = ElasticEngine("stuff")


@app.route("/", methods=["GET"])
async def home(request):
    return json({"hello": "ffsz"})


@app.route("/insert", methods=["POST"])
async def insert_comic(request):
    pass


@app.route("/search", methods=["GET"])
async def search_comic(request):
    pass


@app.route("/recommend", methods=["GET"])
async def recommend_comic(request):
    pass


@app.route("/random", methods=["GET"])
async def random_comic(request):
    """

    :param request:
    :return:
    """
    pass


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
