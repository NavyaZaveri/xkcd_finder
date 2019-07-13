from sanic import Sanic
from sanic.response import json

app = Sanic()


@app.route("/", methods=["GET"])
async def home(request):
    return json({"hello": "ffsz"})


@app.route("/insert", methods=["POST"])
async def insert_comic(request):
    pass


@app.route("/search", methods=["GET"])
async def insert_comic(request):
    pass


@app.route("/recommend", methods=["GET"])
async def recommend_comic(request):
    pass


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
