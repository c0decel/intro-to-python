# Task 1.2
## Goals
- Explain variables and data types in Python
- Summarize the use of objects in Python
- Create a data structure for your Recipe app
## Files
- All code practice 1-5 folders with screenshots of steps
- Screenshots of steps to create recipes
## Journal
### Recipe exercise
> Decide what data structure you would use for this purpose, and in your README file in the repository for this task, describe in approx. 50-75 words why you’ve chosen to use it.
The individual recipes would be a dictionary so it can hold multiple keys and a list of ingredients. I would also make the cooking time a string to specify whether the amount of time is in minutes or hours.

If it were a more detailed recipe list, `cooking_time` would be a nested dictionary specifying steps like `prep_time`, `wait_time`, and `cook_time`, to allow for more complicated and detailed recipes. `ingredients` would also be a nested dictionary to show the name and quantity, which would be a string to show different measurement sizes. If it were even more detailed, it would also include a list of steps to take while making the recipe if it is more particular.

>  Figure out what type of structure you would consider for all_recipes, and briefly note down your justification in the README file. Ideally, this outer structure should be sequential in nature, where multiple recipes can be stored and modified as required.

I would make `all_recipes` a list so it can hold all of the recipe dictionaries.
