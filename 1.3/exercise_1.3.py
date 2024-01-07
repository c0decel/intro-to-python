recipe_list = []
ingredients_list = []

def new_recipe():
    name = input("Name of recipe: ").title()

    prep_time = int(input("Time to prep in minutes: "))
    if prep_time > 59:
        prep_time_hours = str(prep_time / 60) + " hours"
    else:
        prep_time_hours = str(prep_time) + " minutes"

    cook_time = int(input("Time to cook in minutes: "))
    if cook_time > 59:
        cook_time_hours = str(cook_time / 60) + " hours"
    else:
        cook_time_hours = str(cook_time) + " minutes"

    total_time = int((prep_time + cook_time) / 60)
    total_time_hours = str((prep_time + cook_time) / 60) + " hours"

    ingredients = [ingredient.title() for ingredient in input("Ingredients (comma in between): ").split(", ")]
    recipe = {
        'name': name,
        'prep_time': prep_time_hours,
        'cook_time': cook_time_hours,
        'total_time': total_time,
        'total_time_hours': total_time_hours,
        'ingredients': ingredients,
    }
    return recipe

n = int(input("How many recipes to enter?: "))

for i in range(n):
    recipe = new_recipe()
    for ingredient in recipe['ingredients']:
        if ingredient not in ingredients_list:
            ingredients_list.append(ingredient)
    recipe_list.append(recipe)

for recipe in recipe_list:
    if recipe['total_time'] > 0 and len(recipe['ingredients']) < 4:
        recipe['difficulty'] = 'Easy'
    elif recipe['total_time'] < 1 and len(recipe['ingredients']) >= 4:
        recipe['difficulty'] = 'Medium'
    elif recipe['total_time'] < 2 and len(recipe['ingredients']) >= 6:
        recipe['difficulty'] = 'Hard'
    else:
        recipe['difficulty'] = 'You will probably fail'

for recipe in recipe_list:
    print("Recipe: " + recipe['name'])
    print("Prep time: " + recipe['prep_time'])
    print("Cook time: " + recipe['cook_time'])
    print("Total time: " + recipe['total_time_hours'])
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
