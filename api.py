from flask import Flask
from flask_restful import Resource, Api, abort, reqparse

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument("name", type=str, help="recipe name", required=True)
parser.add_argument("ingredients", type=dict, help="ingredients needed for recipe", required=True)
parser.add_argument("instructions", type=str, help="instructions on how to prepare meal", required=True)

RECIPES = {}

def abort_mission(rec_id):
    if rec_id not in RECIPES:
        abort(404, message="Recipe {} does not exist".format(rec_id))

def abort_rec_id_exists(rec_id):
    if rec_id in RECIPES:
        abort(409, message="Recipe ID {} already exists".format(rec_id))

class Recipe(Resource):
    def get(self, rec_id):
        abort_mission(rec_id)
        return RECIPES[rec_id]
    
    def delete(self, rec_id):
        abort_mission(rec_id)
        del RECIPES[rec_id]
        return '', 204
    
    def put(self, rec_id):
        abort_rec_id_exists(rec_id)
        args = parser.parse_args()
        RECIPES[rec_id] = args
        return RECIPES[rec_id], 201
    
class Recipes(Resource):
    def get(self):
        return RECIPES
    
    def post(self, rec_id):
        args = parser.parse_args()
        RECIPES[rec_id] = args
        return RECIPES[rec_id], 201

api.add_resource(Recipes, '/')
api.add_resource(Recipe, '/recipes/<rec_id>')

if __name__ == '__main__':
    app.run(debug=True)