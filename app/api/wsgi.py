from flask import Flask
from app.lib.HttpResult.StatusCodeResult import OkObjectResult, NotFoundResult

app = Flask(__name__)

data = {"response": ["data", "data", "data", "data"]}


@app.get("/")
def get_ok():
    return OkObjectResult(data)()


if __name__ == "__main__":
    app.run(debug=True)
