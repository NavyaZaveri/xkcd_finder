from functools import wraps
import os

from sanic import Sanic
from sanic.response import json

from es_api.client import ElasticEngine
from utils import cleanup

app = Sanic(__name__)


async def setup_es_client(app, loop):
    app.es_client = ElasticEngine.from_bonsai("xkcd_production", test_instance=False)


def check_request_for_authorization_status(request):
    return "password" in request.json \
           and request.json["password"] == os.environ.get("PASSWORD")


def validate_request(attr, keys):
    def inner(f):
        @wraps(f)
        async def decorated_function(request, *args, **kwargs):
            if hasattr(request, attr):
                request_attr = getattr(request, attr)
                if all(key in request_attr for key in keys):
                    response = await f(request, *args, **kwargs)
                    return response
                else:
                    missing_keys = [key for key in keys if key not in request_attr]
                    return json(
                        {f"{attr} in request missing params: {missing_keys}"},
                        400
                    )
            else:
                raise Exception(f"request has no attribute {attr}")

        return decorated_function

    return inner


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
    return json({"hello": "world"})


@app.route("/insert", methods=["POST"])
@authorized()
@validate_request(attr="json", keys=["doc"])
async def insert_comic(request):
    doc = request.json["doc"]
    app.es_client.insert(doc)
    return json({"msg": "insertion successful"},
                status=201)


@app.route("/search", methods=["GET"])
@validate_request(attr="args", keys=["query"])
async def search_comic(request):
    query = request.args.get("query")
    clean_query = cleanup(query)
    results = app.es_client.search_by(content=clean_query).results()
    return json({"results": results})


@app.route("/random", methods=["GET"])
async def random_comic(request):
    doc = app.es_client.get_random_doc()
    return json({
        "results": doc
    })


@app.route("/all", methods=["GET"])
async def display_all_docs(request):
    results = app.es_client.search_all().results()
    return json(
        {"results": results}
    )


@app.route("/size", methods=["GET"])
async def display_size(request):
    sz = app.es_client.index_size()
    return json({"size": str(sz)})


@app.route("/delete", methods=["POST"])
@authorized()
@validate_request(attr="json", keys=["doc"])
async def delete_document(request):
    doc_to_delete = request.json["doc"]
    app.es_client.delete_document_by(id=doc_to_delete["id"])
    return json({
        "result": "document deleted"}
    )


@app.route("/bulk-insert", methods=["POST"])
@authorized()
@validate_request(attr="json", keys=["docs"])
async def bulk_insert_docs(request):
    docs = request.json["docs"]
    success, failed = app.es_client.bulk_insert(docs)
    return json({
        "success": success,
        "failed": failed
    })


if __name__ == "__main__":
    app.register_listener(setup_es_client, "before_server_start")
    app.run(host="0.0.0.0", port=8000, debug=True, workers=20)
