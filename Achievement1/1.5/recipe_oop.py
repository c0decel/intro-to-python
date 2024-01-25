class Recipe:
    ingredients_list = set()

    def __init__(self, name, cook_time):
        self.name = name
        self.ingredients = []
        self.cook_time = cook_time
        self.difficulty = 0

    def calc_difficulty(self):
        if self.cook_time < 10 and len(self.ingredients) < 4:
            self.difficulty = 'Easy'
        elif self.cook_time < 10 and len(self.ingredients) >= 4:
            self.difficulty = 'Medium'
        elif self.cook_time >= 10 and len(self.ingredients) < 4:
            self.difficulty = 'Intermediate'
        else:
            self.difficulty = 'Hard'

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_ingredients(self):
        return self.ingredients

    def add_ingredients(self, *ingredients):
        for ingredient in ingredients:
            self.ingredients.append(ingredient)
        self.update_ingredients_list()

    def update_ingredients_list(self):
        for ingredient in self.ingredients:
            Recipe.ingredients_list.add(ingredient)

    def search_ingredient(self, ingredient):
        return ingredient in self.ingredients

    def get_cook_time(self):
        return self.cook_time
    
    def set_cook_time(self, cook_time):
        self.cook_time = cook_time

    def get_difficulty(self):
        if self.difficulty == 0:
            self.calc_difficulty()
        return self.difficulty 

    def __str__(self):
        return f"Recipe: {self.name}\nIngredients: {', '.join(self.ingredients)}\nCook Time: {self.cook_time} minutes\nDifficulty: {self.get_difficulty()}"


def search_recipe(data, search_query):
    for recipe in data:
        if recipe.search_ingredient(search_query):
            print(recipe)

borders = "=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-="

tea = Recipe('Tea', 5)  
tea.add_ingredients('Tea leaves', 'Sugar', 'Water')
print(tea)

coffee = Recipe('Coffee', 5)  
coffee.add_ingredients('Coffee grounds', 'Sugar', 'Water')
print(coffee)

cake = Recipe('Cake', 50)  
cake.add_ingredients('Butter', 'Sugar', 'Milk', 'Eggs', 'Vanilla', 'Flour', 'Baking Powder', 'Milk')
print(cake)

banana_smoothie = Recipe('Banana Smoothie', 5)  
banana_smoothie.add_ingredients('Bananas', 'Milk', 'Sugar', 'Ice Cubes', 'Peanut Butter')
print(banana_smoothie)

recipe_list = [tea, coffee, cake, banana_smoothie]

print('Recipes with water: ')
print(borders)
search_recipe(recipe_list, 'Water')

print('Recipes with sugar: ')
print(borders)
search_recipe(recipe_list, 'Sugar')

print('Recipes with bananas: ')
print(borders)
search_recipe(recipe_list, 'Bananas')