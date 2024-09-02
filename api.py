from flask import Flask, request, make_response, jsonify
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)
db = SQLAlchemy(app)

class Ingredients(db.Model):
    __tablename__ = 'ingredients'

    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'))
    ingredient_name = db.Column(db.String(), nullable=False)
    quantity = db.Column(db.String(255))

class Recipe(db.Model):
    __tablename__ = 'recipe'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    description = db.Column(db.String())
    category = db.Column(db.String(), db.ForeignKey('categories.id'))
    ingredients = db.relationship('Ingredients', backref='recipe')
    servings = db.Column(db.Integer)
    
class Categories(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)

class CategoriesList(Resource):
    def get(self):
        categories = Categories.query.all()
        cat_list = []
        for cat in categories:
            cat_data = {'name': cat.name}
            cat_list.append(cat_data)
        return {'Categories': cat_list}, 200

    def post(self):
        if request.is_json:
            category = Categories(name=request.json['name'])
            db.session.add(category)
            db.session.commit()
            return make_response(jsonify({'name': category.name}), 201)
        else:
            return {'error': 'request must be JSON'}, 400
    
class CategoriesItem(Resource):
    def get(self, cat_id):
        category = Categories.query.get(cat_id)
        if category is None:
            return {'error': 'Category not found'}, 404
        else:
            category_data = {'name': category.name}
            return {'Category': category_data}, 200

    def put(self, cat_id):
        if request.is_json:
            category = Categories.query.get(cat_id)
            if category is None:
                return {'error': 'Category not found'}, 404
            else:
                category.name = request.json['name']
                db.session.commit()
                return 'Categories updated', 200
        else:
            return {'error': 'request must be JSON'}, 400
        
    def delete(self, cat_id):
        category = Categories.query.get(cat_id)
        if category is None:
            return {'error': 'Category not found'}, 404
        
        db.session.delete(category)
        db.session.commit()
        return 'Category deleted', 200

class RecipeList(Resource):
    def get(self):
        recipes = Recipe.query.all()
        if recipes is None:
            return {'error': 'No recipes found'}, 404
        else:
            recipe_list = []
            ingredient_list = []
            for recipe in recipes:
                if recipe.ingredients:
                    # because Ingredients table is not serializable, convert ingredient items into list:
                    ingredients = Ingredients.query.filter_by(recipe_id=recipe.id)
                    for ingredient in ingredients:
                        ingredients_jsonified = {"quantity": ingredient.quantity, "name": ingredient.ingredient_name}
                        ingredient_list.append(ingredients_jsonified)
                    recipe_data = {'name': recipe.name, 
                                'description': recipe.description, 
                                'category': recipe.category, 
                                'ingredients': ingredient_list,
                                'servings': recipe.servings
                                }
                    recipe_list.append(recipe_data)
                else:
                    recipe_data = {'name': recipe.name, 
                                'description': recipe.description, 
                                'category': recipe.category, 
                                'servings': recipe.servings
                                }
                    recipe_list.append(recipe_data)
            return {"Recipes": recipe_list}, 200

    def post(self):
        if request.is_json:
            recipe = Recipe(name=request.json['name'], 
                            description=request.json['description'],
                            category=request.json['category'],
                            servings=request.json['servings']
                        )
            db.session.add(recipe)
            db.session.commit()
            return make_response(jsonify(
                {'name': recipe.name, 'description': recipe.description, 'category': recipe.category, 
                 'ingredients': recipe.ingredients, 'servings': recipe.servings}), 201)
        else:
            return {'error': 'request must be JSON'}, 400
        
class RecipeByCategory(Resource):
    def get(self, cat):
        get_recipes_by_category = Recipe.query.filter_by(category=cat)
        if not get_recipes_by_category:
            return {"Error": "Could not find category"}, 404
        else:
            recipe_list = []
            ingredient_list = []
            for recipe in get_recipes_by_category:
                if recipe.ingredients:
                    ingredients = Ingredients.query.filter_by(recipe_id=recipe.id)
                    for ingredient in ingredients:
                        ingredients_jsonified = {"quantity": ingredient.quantity, "name": ingredient.ingredient_name}
                        ingredient_list.append(ingredients_jsonified)
                    recipe_data = {'name': recipe.name, 
                                'description': recipe.description, 
                                'category': recipe.category, 
                                'ingredients': ingredient_list, 
                                'servings': recipe.servings
                                }
                    recipe_list.append(recipe_data)
                else:
                    recipe_data = {'name': recipe.name, 
                                'description': recipe.description, 
                                'category': recipe.category, 
                                'servings': recipe.servings
                                }
                    recipe_list.append(recipe_data)
            return {"Recipes": recipe_list}, 200

class RecipeItem(Resource):
    def get(self, rec_id):
        recipe = Recipe.query.filter_by(id=rec_id)
        if recipe is None:
            return {'error': 'Recipe not found'}, 404
        else:
            recipe_list = []
            ingredient_list = []
            for r in recipe:
                if r.ingredients:
                    ingredients = Ingredients.query.filter_by(recipe_id=rec_id)
                    for ingredient in ingredients:
                        ingredients_jsonified = {"quantity": ingredient.quantity, "name": ingredient.ingredient_name}
                        ingredient_list.append(ingredients_jsonified)
                    recipe_data = {'name': r.name, 
                                    'description': r.description, 
                                    'category': r.category, 
                                    'ingredients': ingredient_list, 
                                    'servings': r.servings
                                    }
                    recipe_list.append(recipe_data)
                    return {'Recipe': recipe_list}, 200
                else:
                    recipe_data = {'name': r.name, 
                                    'description': r.description, 
                                    'category': r.category, 
                                    'ingredients': {}, 
                                    'servings': r.servings
                                    }
                    recipe_list.append(recipe_data)
                    return {'Recipe': recipe_list}, 200

    def put(self, rec_id):
        if request.is_json:
            recipe = Recipe.query.get(rec_id)
            if recipe is None:
                return {'error': 'Recipe not found'}, 404
            else:
                recipe.name = request.json['name']
                recipe.description = request.json['description']
                recipe.category = request.json['category']
                recipe.servings = request.json['servings']
                db.session.commit()
                return 'Recipe updated', 200
        else:
            return {'error': 'request must be JSON'}, 400

    def delete(self, rec_id):
        recipe = Recipe.query.get(rec_id)
        if recipe is None:
            return {'error': 'Recipe not found'}, 404
        
        db.session.delete(recipe)
        db.session.commit()
        return 'Recipe deleted', 200

class IngredientsSource(Resource):
    def get(self, ing_id):
        ingredients = Ingredients.query.filter_by(recipe_id=ing_id)
        if ingredients is None:
            return {'error': 'Ingredients not found'}, 404
        else:
            ing_list = []
            for ingredient in ingredients:
                ing_data = {
                    'recipe_id': ingredient.recipe_id, 
                    'ingredient_name': ingredient.ingredient_name, 
                    'quantity': ingredient.quantity
                    }
                ing_list.append(ing_data)
            return {'Ingredients': ing_list}, 200

    def post(self, ing_id):
        if request.is_json:
            ingredient = Ingredients(
                recipe_id=request.json['recipe_id'], 
                ingredient_name=request.json['ingredient_name'],
                quantity=request.json['quantity']
            )
            db.session.add(ingredient)
            db.session.commit()
            return make_response(jsonify(
                {'recipe_id': ingredient.recipe_id, 
                 'ingredient_name': ingredient.ingredient_name, 
                 'quantity': ingredient.quantity}), 201)
        else:
            return {'error': 'request must be JSON'}, 400
    
class IngredientsItem(Resource):
    def delete(self, ing_id):
        ingredient = Ingredients.query.get(ing_id)
        if ingredient is None:
            return {'error': 'Ingredient not found'}, 404
        
        db.session.delete(ingredient)
        db.session.commit()
        return 'Ingredient deleted', 200

    def put(self, ing_id):
        if request.is_json:
            ingredients = Ingredients.query.get(ing_id)
            if ingredients is None:
                return {'error': 'Ingredients from recipe not found'}, 404
            else:
                ingredients.ingredient_name = request.json['ingredient_name']
                ingredients.quantity = request.json['quantity']
                db.session.commit()
                return 'Ingredients updated'.format(ing_id), 200
        else:
            return {'error': 'request must be JSON'}, 400

api.add_resource(CategoriesList, '/categories')
api.add_resource(CategoriesItem, '/categories/<cat_id>')
api.add_resource(RecipeByCategory, '/categories/recipe/<cat>')
api.add_resource(RecipeList, '/recipe')
api.add_resource(RecipeItem, '/recipe/<rec_id>')
api.add_resource(IngredientsSource, '/recipe/<ing_id>/ingredients')
api.add_resource(IngredientsItem, '/ingredients/<ing_id>')

if __name__ == '__main__':
    app.run(debug=True)