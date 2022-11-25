from flask import Flask
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)

args = {"bpm": "0", "condition": "Regular", "shutdown": "No"}
class database(Resource):
  def post(self):
    parser = reqparse.RequestParser()

    parser.add_argument("bpm", required = False)
    parser.add_argument("condition", required = False)
    parser.add_argument("shutdown", required = False)

    global args
    args = parser.parse_args()
    
    return args
  def get(self):
    global args
    return args

api.add_resource(database, "/database")
app.run(port = 5000, host="192.168.1.51")
