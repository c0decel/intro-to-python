import pickle

borders = '-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-'
def display_recipe(recipe):
    print(borders)
    print(f'Recipe: {recipe["name"]}')
    print(f'Cook time: {recipe["cook_time"]} minutes')
    print(f'Difficulty: {recipe["difficulty"]}')
    print('-=-')
    print('Ingredients: ')
    for ingredient in recipe['ingredients']:
        print(f'- {ingredient}')

def search_ingredient(data):
    ingredients_list = data["ingredients_list"]
    print('All Ingredients:')
    print(borders)
    for i, ingredient in enumerate(ingredients_list):
        print(f'{i+1}.) {ingredient}')

    try:
        while True:
            choice = int(input('>>> Number of ingredient to search: '))
            print(borders)
            if 1 <= choice <= len(ingredients_list):
                ingredient_searched = ingredients_list[choice - 1]
                break
            print(f'Enter a number between 1 and {len(ingredients_list)}.')

        recipes_with_ingredient = [recipe for recipe in data['recipe_list'] if ingredient_searched in recipe['ingredients']]
        num_recipes = len(recipes_with_ingredient)

        print(borders)
        print(f'{num_recipes} found containing {ingredient_searched.lower()}:')
        print(borders)

        for recipe in recipes_with_ingredient:
            display_recipe(recipe)
    except ValueError:
        print('Positive numbers only')

filename = input('>>> Filename of saved recipes: ')
recipe_file = (filename + '.bin')

try: 
    with open(recipe_file, 'rb') as file:
        data = pickle.load(file)
except FileNotFoundError:
    print('Not found. Try again.')
else: 
    search_ingredient(data)
