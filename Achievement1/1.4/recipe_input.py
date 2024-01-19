import pickle

recipe_list = []
ingredients_list = []

def calc_difficulty(cook_time, ingredients):
    if cook_time < 10 and ingredients < 4:
        return 'Easy'
    elif cook_time < 10 and ingredients >= 4:
        return 'Medium'
    elif cook_time >= 10 and ingredients < 4:
        return 'Intermediate'
    else:
        return 'Hard'

def take_recipe():
    while True:
        name = input('Name of recipe: ').title()
        if name:
            break
        print('Name cannot be empty')

    while True:
        try:
            cook_time = int(input('Time to cook in minutes: '))
            if cook_time >= 0:
                break
            print('Cook time must be over a minute')
        except ValueError:
            print('Bad input, enter a number above zero')

    while True:
        ingredients = [ingredient.title() for ingredient in input('Ingredients (comma in between): ').split(', ')]
        if ingredients:
            break
        print('Enter at least one ingredient')
    
    difficulty = calc_difficulty(cook_time, len(ingredients))

    return {
        'name': name,
        'cook_time': cook_time,
        'ingredients': ingredients,
        'difficulty': difficulty
    }

filename = input('Name of file to export recipes: ')
recipe_file = (filename + '.bin')
def save_recipes(): 
    try:
        with open(recipe_file, 'rb') as file:
            data = pickle.load(file)
    except FileNotFoundError:
        data = {"recipe_list": [], "ingredients_list": []}
    finally:
        print(data)

n = int(input('How many recipes to enter?: '))
for i in range(n):
    recipe = take_recipe()
    for ingredient in recipe['ingredients']:
        if ingredient not in ingredients_list:
            ingredients_list.append(ingredient)
    recipe_list.append(recipe)

data = {"recipe_list": recipe_list, "ingredients_list": ingredients_list}

with open(recipe_file, 'wb') as file:
    pickle.dump(data, file)


print('Recipes saved successfully!')
