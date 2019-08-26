import os
from functools import wraps

from sanic import Sanic
from sanic.response import json

from es_api.client import ElasticEngine
from settings import Settings
from scraper.xkcd_scraper import cleanup

app = Sanic()


def check_request_for_authorization_status(request):
    return "password" in request.json \
           and request.json["password"] == os.environ.get("PASSWORD")


def authorized():
    def decorator(f):
        @wraps(f)
        async def decorated_function(request, *args, **kwargs):
            is_authorized = check_request_for_authorization_status(request)

            if is_authorized:
                response = await f(request, *args, **kwargs)
                return response
            else:
                return json({'status': 'not_authorized'}, 403)

        return decorated_function

    return decorator


@app.route("/", methods=["GET"])
async def home(request):
    print(request.app.config)
    return json({"hello": "world"})


@app.route("/insert", methods=["POST"])
@authorized()
async def insert_comic(request):
    doc = request.json["doc"]
    app.config.es_client.insert(doc)
    return json({"msg": "insertion successful"},
                status=201)


@app.route("/search", methods=["GET"])
async def search_comic(request):
    query = request.args.get("query")
    clean_query = cleanup(query)
    results = app.config.es_client.search_by(content=clean_query).results()
    return json({"results": results})


@app.route("/random", methods=["GET"])
async def random_comic(request):
    doc = app.config.es_client.get_random_doc()
    return json({
        "results": doc
    })


@app.route("/all", methods=["GET"])
async def display_all_docs(request):
    results = app.config.es_client.search_all().results()
    return json(
        {"results": results}
    )


@app.route("/delete", methods=["POST"])
@authorized()
async def delete_document(request):
    doc_to_delete = request.json["doc"]
    app.config.es_client.delete_document_by(id=doc_to_delete["id"])
    return json({
        "result": "document deleted"}
    )


if __name__ == "__main__":
    app.config.from_object(Settings())
    app.config.es_client = ElasticEngine.from_bonsai("xkcd_production", test_instance=False)
    app.run(host="0.0.0.0", port=8000, debug=True)
