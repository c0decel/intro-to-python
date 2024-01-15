recipe_list = []
ingredients_list = []

def take_recipe():
    name = input("Name of recipe: ").title()

    cook_time = int(input("Time to cook in minutes: "))

    ingredients = [ingredient.title() for ingredient in input("Ingredients (comma in between): ").split(", ")]
    
    recipe = {
        'name': name,
        'cook_time': cook_time,
        'ingredients': ingredients,
    }
    return recipe

n = int(input("How many recipes to enter?: "))

for i in range(n):
    recipe = take_recipe()
    for ingredient in recipe['ingredients']:
        if ingredient not in ingredients_list:
            ingredients_list.append(ingredient)
    recipe_list.append(recipe)

for recipe in recipe_list:
    if recipe['cook_time'] < 10 and len(recipe['ingredients']) < 4:
        recipe['difficulty'] = 'Easy'
    elif recipe['cook_time'] < 10 and len(recipe['ingredients']) >= 4:
        recipe['difficulty'] = 'Medium'
    elif recipe['cook_time'] >= 10 and len(recipe['ingredients']) < 4:
        recipe['difficulty'] = 'Intermediate'
    else:
        recipe['difficulty'] = 'Hard'

for recipe in recipe_list:
    print("Recipe: " + recipe['name'])
    print("Cook time: " + str(recipe['cook_time']))
    print("Ingredients: ")
    for ingredient in recipe['ingredients']:
        print("- " + ingredient)
    print("Difficulty: " + recipe['difficulty'])
    print(" ... ... ... ")

def print_all():
    ingredients_list.sort()
    print("All ingredients")
    print("--------------")
    for ingredient in ingredients_list:
        print(ingredient)

print_all()
