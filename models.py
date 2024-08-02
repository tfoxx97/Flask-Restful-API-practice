# from api import app
# from flask_sqlalchemy import SQLAlchemy

# db = SQLAlchemy(app)

class Measurement:
    id = None
    name = None
    quantity = None
    recipe_ingredient = None

class Ingredients:
    recipe_id = None
    name = None
    quantity = None
    ingredient_name = None

class Receipe_Ingredients:
    recipe_id = None
    recipe_name = None
    quantity = None
    ingredients = None

class Recipe:
    id = None
    name = None
    description = None
    category = None
    ingredients = None
    servings = None
    
class Categories:
    id = None
    name = None
    recipe = None

# with app.app_context():
#     db.create_all()