import os
from functools import wraps

from sanic import Sanic
from sanic.response import json

from es_api.client import ElasticEngine
from settings import Settings

app = Sanic()
app.config.from_object(Settings())

# load configruration from .env configuration environment
es_client = ElasticEngine("stuff1")


def check_request_for_authorization_status(request):
    return "password" in request.json and request.json["password"] == os.environ.get("PASSWORD")


def authorized():
    def decorator(f):
        @wraps(f)
        async def decorated_function(request, *args, **kwargs):
            # run some method that checks the request
            # for the client's authorization status
            is_authorized = check_request_for_authorization_status(request)

            if is_authorized:
                # the user is authorized.
                # run the handler method and return the response
                response = await f(request, *args, **kwargs)
                return response
            else:
                # the user is not authorized.
                return json({'status': 'not_authorized'}, 403)

        return decorated_function

    return decorator


@app.route("/", methods=["GET"])
async def home(request):
    return json({"hello": "world"})


@app.route("/insert", methods=["POST"])
@authorized()
async def insert_comic(request):
    doc = request.json["doc"]
    es_client.insert(doc)
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


@app.route("/view_all", methods=["GET"])
async def display_all_docs(request):
    results = [doc for doc in es_client.search_all().results()]
    return json(
        {"result": results}
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
