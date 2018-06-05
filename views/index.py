import datetime
from flask import Blueprint, render_template, make_response, Response, request, jsonify
from funcs.run_osabie import OsabieRunner

app = Blueprint('index', __name__)


@app.route("/", methods=["GET"])
def index():
    expiration_date = datetime.datetime.now() + datetime.timedelta(days=7200)

    response = make_response(render_template("index.html"))  # type: Response

    if "test-cookie" not in request.cookies.keys():
        response.set_cookie("test-cookie", value="Hello, World", expires=expiration_date)

    return response


@app.route("/api/run", methods=["POST"])
def run_code():
    """
    Runs the code given as a parameter and returns the result after running that code.
    :return: A JSON object containing the result of that code.
    """
    osabie_code = request.args.get("code", default="")
    osabie_input = request.args.get("input", default="")

    # Run the code with osabie and get the output and the status.
    output, is_terminated, is_truncated = OsabieRunner.run_code(osabie_code, osabie_input)

    return jsonify({"result": output, "status": {"code": is_terminated, "truncated": is_truncated}})
