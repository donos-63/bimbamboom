from flask import Flask, jsonify
from src.database.db_access import DatabaseManager as db
import json
from bson.json_util import dumps
from flask import request
import ast

app = Flask(__name__)

@app.route("/")
def home():
    return {"welcome": "this is the home page, nothing to do"}


@app.route("/api/country/<name>", methods=['GET'])
def route_request(name: str):
    """Get country by name

    Args:
        name (str): country name

    Returns:
        json: country data
    """

    content = json.loads(dumps(db.getInstance().get_country_by_name(name)))
    return content

@app.route("/api/insert_random/<name>", methods=['GET'])
def  add_country(name: str):
    """Add a country generated randomly

    Returns:
        json: the country created
    """
    
    content = json.loads(dumps(db.getInstance().set_country(name)))

    return content

@app.route("/api/delete", methods=['DELETE'])
def  remove_country():
    """Delete a country from its name

    Returns:
        json: operation result
    """

    name=request.get_data().decode().split('=')[1]
    result = json.loads(dumps(db.getInstance().delete_country_by_name(name)))
    return result

@app.route("/api/update", methods=["POST"])
def  update_country():
    """Update a country

    Returns:
        json: the information of the updated country
    """

    name=request.form.get("name")
    updates=ast.literal_eval(request.form.get("tuples"))

    content = json.loads(dumps(db.getInstance().update_country_by_name(name, updates)))

    return content

@app.route("/api/density", methods=["POST"])
def  countries_by_density():
    """List countries by density rates

    Returns:
        json: countries by density
    """

    v_low=int(request.form.get("v_low"))
    low=int(request.form.get("low"))
    medium=int(request.form.get("medium"))

    content = json.loads(dumps(db.getInstance().get_countries_by_density(v_low, low, medium)))
    return content


if __name__ == "__main__":
     app.run(host='localhost', port = 8080, debug=False)