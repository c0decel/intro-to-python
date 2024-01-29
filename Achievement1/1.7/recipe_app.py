from sqlalchemy import create_engine, Column
from sqlalchemy.types import Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.orm.exc import NoResultFound

engine = create_engine("mysql://cf-python:password@localhost/my_database")

Base = declarative_base()

# Create and format table for recipes
class Recipe(Base):
    __tablename__ = "Recipe_Base"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    ingredients = Column(String(255))
    cook_time = Column(Integer)
    difficulty = Column(String(20))

    def __repr__(self):
        return ("<Recipe ID: " + str(self.id) + "-" + self.name + ">")

    # Calculate the difficulty
    def calc_difficulty(self):
        qty_ingredients = len(self.ingredients_as_list())
        if self.cook_time < 10 and qty_ingredients < 4:
            self.difficulty = 'Easy'
        elif self.cook_time < 10 and qty_ingredients >= 4:
            self.difficulty = 'Medium'
        elif self.cook_time >= 10 and qty_ingredients < 4:
            self.difficulty = 'Intermediate'
        else:
            self.difficulty = 'Hard'

    # Convert ingredients to a list
    def ingredients_as_list(self):
        if self.ingredients == "": return []
        return self.ingredients.split(", ")


Base.metadata.create_all(engine)

Session = sessionmaker(bind = engine)
session = Session()

# Format recipe to print
def format_recipe(recipe):
    print('-=+=+=+=+=+=+=+=+=+=+=-')
    print("ID: ", recipe.id, " | Name: ", recipe.name)
    print("Cook time: ", recipe.cook_time)
    print("Ingredients: ", recipe.ingredients)
    print("Difficulty: ", recipe.difficulty)
    print('-=+=+=+=+=+=+=+=+=+=+=-')

# Create a new recipe
def create_recipe():
    while True:
        try:
            name = input(">>> Recipe name: ").title()
            if name == "":
                print(">>> Cannot be blank.")
                return
            cook_time = int(input(">>> Cook time: "))
            if cook_time < 1 or cook_time == str:
                print(">>> Positive numbers only")
                return
            ingredients = []

            n = int(input(">>> How many ingredients to enter?: "))
            if n < 1:
                print(">>> Enter a positive number.")
            else:
                break
        except ValueError:
            print(">>> Enter a number.")
        
    # Allow an input for each ingredient
    for i in range(n):
        ingredient_input = input(f"{i + 1}.) ").title()
        ingredients.append(ingredient_input)

    # Format to insert into table
    new_recipe = Recipe(
        name = name,
        ingredients = ", ".join(ingredients),
        cook_time = cook_time
    )

    new_recipe.calc_difficulty()


    session.add(new_recipe)
    session.commit()
    format_recipe(new_recipe)

# Return a list of all recipes
def view_all_recipes():
    recipe_list = session.query(Recipe).all()

    if len(recipe_list) < 1:
        print(">>> No recipes.")
    else:
        for recipe in recipe_list:
            format_recipe(recipe)

# Search for recipe by ingredient
def search_by_ingredients():
    results = session.query(Recipe.ingredients).all()

    all_ingredients = set()

    if len(results) < 1:
        print(">>> No recipes.")
    else:
        for result in results:
            ingredients_list = result[0].split(", ")
            for ingredient in ingredients_list:
                all_ingredients.add(ingredient.strip())

    sort_ingredients = sorted(all_ingredients)

    # Format to return each ingredient in a numbered list
    for i, ingredient in enumerate(sort_ingredients):
        print(f'{i + 1}.) {ingredient}')

    while True:
        try:
            options = input(">>> Number of ingredients to search by number (spaces for multiples): ").split()
            selected_options = [int(option) for option in options]
            if all(1 <= choice <= len(all_ingredients) for choice in selected_options):
                break
            else:
                print(">>> Enter numbers between 1 and ", len(all_ingredients))
        except ValueError:
            print(">>> Invalid input. Number only.")

    search_ingredients = [sort_ingredients[index - 1] for index in selected_options]

    search_conditions = [Recipe.ingredients.like(f"%{ingredient}%") for ingredient in search_ingredients]
    search_results = session.query(Recipe).filter((*search_conditions)).all()

    if search_results:
        print(len(search_results), " found: ")

        for i, recipe in enumerate(search_results):
            print(format_recipe(recipe))
    else:
        print(">>> None found.")

# Edit a recipe
def edit_recipe():
    recipes = session.query(Recipe.id, Recipe.name).all()
    for recipe_id, recipe_name in recipes:
        print(f"{recipe_id} - {recipe_name}")

    try:
        id_to_edit = int(input(">>> ID of recipe to edit: "))
        recipe_to_edit = session.query(Recipe).filter(Recipe.id == id_to_edit).one()
    except ValueError:
        print(">>> Enter a number.")
        return
    except NoResultFound:
        print(">>> No results found.")
        return

    print("1.) Name")
    print("2.) Cook time")
    print("3.) Ingredients")

    try:
        part_to_edit = int(input(">>> Enter the number of which part to edit: "))
    except ValueError:
        print(">>> Numbers only.")
        return

    if part_to_edit == 1:
        while True:
            new_name = input(">>> New name: ").title()
            if len(new_name) > 50:
                print(">>> Name is too long.")
            else:
                break
        recipe_to_edit.name = new_name
    elif part_to_edit == 2:
        while True:
            new_cook_time = int(input(">>> New cook time in minutes: "))
            break
        recipe_to_edit.cook_time = new_cook_time
        recipe_to_edit.calc_difficulty()
    elif part_to_edit == 3:
        while True:
            new_ingredients = input(">>> Ingredients (separate with a comma): ").title()
            if len(new_ingredients) < 1:
                print(">>> Cannot be blank")
                return
            else:
                recipe_to_edit.ingredients = new_ingredients
                break
        recipe_to_edit.calc_difficulty()

    else:
        print(">>> Invalid number.")
        return

    session.commit()
    print(">>> DONE.")
    format_recipe(recipe_to_edit)

# Delete a recipe
def delete_recipe():
    recipes = session.query(Recipe.id, Recipe.name).all()
    for recipe_id, recipe_name in recipes:
        print(f"{recipe_id} - {recipe_name}")

    try:
        id_to_delete = int(input(">>> ID of recipe to delete: "))
        recipe_to_delete = session.query(Recipe).filter(Recipe.id == id_to_delete).one()
    except ValueError:
        print(">>> Enter a number.")
        return
    except NoResultFound:
        print(">>> None found.")
        return

    print(f">>> Are you sure you want to delete {recipe_to_delete.name}?")
    choice = input(">>> Type YES to confirm: ").lower()

    if choice == "yes":
        session.delete(recipe_to_delete)
        session.commit()
        print("DONE")

# Main menu
def main_menu():
    choice = ""
    while(choice != "quit"):
        print("What do you want to do?")
        print("1.) Create recipe")
        print("2.) View all recipes")
        print("3.) Search by ingredients")
        print("4.) Edit recipe")
        print("5.) Delete recipe")
        print("Type 'quit' to exit")

        choice = input(">>> Choice: ").lower()

        if choice in ["1", "2", "3", "4", "5"]:
            if choice == "1": create_recipe()
            elif choice == "2": view_all_recipes()
            elif choice == "3": search_by_ingredients()
            elif choice == "4": edit_recipe()
            elif choice == "5": delete_recipe()
        elif choice == "quit":
            break
        else:
            print(">>> Invalid choice.")

main_menu()