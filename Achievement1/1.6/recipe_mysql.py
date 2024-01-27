import mysql.connector

conn = mysql.connector.connect(
    host='localhost',
    user='cf-python',
    passwd='password'
)

cursor = conn.cursor()

cursor.execute("CREATE DATABASE IF NOT EXISTS task_database")

cursor.execute("USE task_database")

cursor.execute('''CREATE TABLE IF NOT EXISTS Recipes(
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50),
    ingredients VARCHAR(255),
    cook_time INT,
    difficulty VARCHAR(20)
)''')

def main_menu(conn, cursor):
    choice = ""
    while(choice != 'quit'):

        print('What do you want to do?')
        print('1.) Create a recipe')
        print('2.) Search by ingredient')
        print('3.) Update a recipe')
        print('4.) Delete a recipe')
        print('Type quit to exit.')

        choice = input('Choice: ').lower()

        if choice in ['1', '2', '3', '4']:

            if choice == '1':
                create_recipe(conn, cursor)
            elif choice == '2':
                search_recipe(conn, cursor)
            elif choice == '3':
                update_recipe(conn, cursor)
            elif choice == '4':
                delete_recipe(conn, cursor)
        elif choice == 'quit':
            break
        else:
            print('Invalid choice.')

    conn.close()

def create_recipe(conn, cursor):
    while True:
        try:
            n = int(input('How many recipes to enter?: '))
            if n < 1:
                print('Enter a positive number.')
            else:
                break
        except ValueError:
            print('Enter a number.')

    for i in range(n):
        name = input('Recipe name: ').title()
        cook_time = int(input('Cook time: '))
        ingredients_input = input('Ingredients seperated by commas: ').title()
        ingredients = ingredients_input.split(', ')

        difficulty = calc_difficulty(cook_time, ingredients)

        ingredients_str = ', '.join(ingredients)

        try:
            insert_query = "INSERT INTO Recipes (name, ingredients, cook_time, difficulty) VALUES (%s, %s, %s, %s)"
            cursor.execute(insert_query, (name, ingredients_str, cook_time, difficulty))
            conn.commit()
            print('DONE')
        except mysql.connector.Error as err:
            print('Error: ', err)


def calc_difficulty(cook_time, ingredients):
    qty_ingredients = len(ingredients)
    if cook_time < 10 and qty_ingredients < 4:
        return 'Easy'
    elif cook_time < 10 and qty_ingredients >= 4:
        return 'Medium'
    elif cook_time >= 10 and qty_ingredients < 4:
        return 'Intermediate'
    else:
        return 'Hard'

def format_recipe(recipe):
    print('-=+=+=+=+=+=+=+=+=+=+=-')
    print('-=+=+=+=+=+=+=+=+=+=+=-')
    print(f"\nRecipe: {recipe[1].title()}")
    print('-=+=+=+=+=+=+=+=+=+=+=-')
    print(f"  Time: {recipe[3]} mins")
    print('-=+=+=+=+=+=+=+=+=+=+=-')
    print("  Ingredients:")
    for ingredient in recipe[2].split(", "):
        print(f"  - {ingredient.title()}")
    print('-=+=+=+=+=+=+=+=+=+=+=-')
    print(f"  Difficulty: {recipe[4]}")   
    print('-=+=+=+=+=+=+=+=+=+=+=-')
    print('-=+=+=+=+=+=+=+=+=+=+=-') 


def search_recipe(conn, cursor):
    cursor.execute("SELECT ingredients FROM Recipes")
    results = cursor.fetchall()

    if not results:
        print('No results yet')
        return

    all_ingredients = set()

    for result in results:
        ingredients_list = result[0].split(', ')
        for ingredient in ingredients_list:
            all_ingredients.add(ingredient.strip())
    
    for i, ingredient in enumerate(sorted(all_ingredients)):
        print(f'{i + 1}.) {ingredient}')
    
    print()

    while True:
        try:
            choice = int(input('Enter number for ingredient: '))
            if 1 <= choice <= len(all_ingredients):
                break
            else:
                print(f'Enter a number between 1 and {len(all_ingredients)}.')
        except ValueError:
            print('Enter a number only.')

    selected_ingredient = sorted(all_ingredients)[choice - 1]

    search_query = "SELECT * FROM Recipes WHERE ingredients LIKE %s"
    cursor.execute(search_query, ("%" + selected_ingredient + "%",))
    search_results = cursor.fetchall()

    if search_results:
        print(f'{len(search_results)} results found containing {(selected_ingredient).lower()}:')
        for recipe in search_results:
            format_recipe(recipe)


def update_recipe(conn, cursor):
    cursor.execute("SELECT * FROM Recipes")
    results = cursor.fetchall()

    if not results:
        print('No results yet')
        return

    print('Enter ID to update recipe.')
    for result in results:
        ingredients_list = result[2].split(', ')
        print(f"ID: {result[0]}, Name: {result[1]}")
        print(f"Ingredients: {ingredients_list}\nCook time: {result[3]}\nDifficulty: {result[4]}")

    while True:
        try:
            recipe_id = int(input('Enter number ID of recipe to update: '))

            cursor.execute("SELECT COUNT(*) FROM Recipes WHERE id = %s", (recipe_id,))
            if cursor.fetchone()[0] == 0:
                print("No recipe found with the entered ID. Please try again.\n")
            else:
                break
        except ValueError:
            print()
            print("Invalid input. Please enter a numeric value.\n")

    recipe_choice = next((recipe for recipe in results if recipe[0] == recipe_id), None)
    if recipe_choice:
        print(f"What to update for {recipe_choice[1]}?")
    else:
        print("Not found.")
        return
    print("Name")
    print("Cook time")
    print("Ingredients")

    update_info = input("Your choice: ").lower()

    if update_info not in ['name', 'cook time', 'ingredients']:
        print("Enter 'name', 'cook time', or 'ingredients'")

    if update_info == 'cook time':
        while True:
            try:
                new_value = int(input("New cook time in minutes: "))
                break
            except ValueError:
                print("Input must be a number.")
    else:
        new_value = input(f"Update the value for {update_info}: ").title()

    update_query = f"UPDATE Recipes SET {update_info.replace(' ', '_')} = %s WHERE id = %s"
    cursor.execute(update_query, (new_value, recipe_id))

    if update_info in ["cook_time", "ingredients"]:
        cursor.execute("SELECT cook_time, ingredients FROM Recipes WHERE id = %s", (recipe_id,))
        updated_recipe = cursor.fetchone()
        new_difficulty = calc_difficulty(int(updated_recipe[0]), updated_recipe[1].split(", "))

        cursor.execute("UPDATE Recipes SET difficulty = %s WHERE id = %s", (new_difficulty, recipe_id,))

    conn.commit()

    
    
def delete_recipe(conn, cursor):
    cursor.execute("SELECT * FROM Recipes")
    results = cursor.fetchall()

    if not results:
        print('No results yet')
        return

    print("Enter ID of recipe to remove")
    for result in results:
        ingredients_list = result[2].split(', ')

        print(f"ID: {result[0]}, Name: {result[1]}")
        print(f"Ingredients: {ingredients_list}\nCook time: {result[3]}\nDifficulty: {result[4]}")

    while True:
        try:
            recipe_id = int(input('Enter number ID of recipe to delete: '))

            cursor.execute("SELECT COUNT(*) FROM Recipes WHERE id = %s", (recipe_id,))
            if cursor.fetchone()[0] == 0:
                print("No recipe found with the entered ID. Please try again.\n")
            else:
                cursor.execute("SELECT name FROM Recipes WHERE id = %s", (recipe_id,))
                recipe_name = cursor.fetchone()[0]
                confirmation = input(f"Delete '{recipe_name} FOREVER?? Y/N: ").lower()

                if confirmation == "y" or "yes":
                    break
                elif confirmation == "n" or "no":
                    print("I knew you were too weak to pull the trigger.")
                    print("Deletion cancelled")
                    return
                else:
                    print("Bad input. Enter y/yes or n/no")
        except ValueError:
            print()
            print("Invalid input. Please enter a numeric value.\n")
    cursor.execute("DELETE FROM Recipes WHERE id = %s", (recipe_id,))

    conn.commit()
    
main_menu(conn, cursor)