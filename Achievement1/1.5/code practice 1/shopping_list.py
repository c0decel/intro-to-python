class ShoppingList:
    def __init__(self, list_name):
        self.list_name = list_name
        self.shopping_list = []

    def add_item(self, item):
        if item not in self.shopping_list:
            self.shopping_list.append(item)
            print(f"{item} added to shopping list.")

    def remove_item(self, item):
        if item in self.shopping_list:
            self.shopping_list.remove(item)
            print(f"{item} removed from shopping list.")
        else:
            print("Item isn't in list yet.")

    def view_list(self):
        if not self.shopping_list:
            print(f"{self.list_name} is empty.")
        else:
            print(f"Items in {self.list_name}:")
            for item in self.shopping_list:
                print(f"- {item}")

pet_store_list = ShoppingList("Pet Store Shopping List")

pet_store_list.add_item("Dog food")
pet_store_list.add_item("Frisbee")
pet_store_list.add_item("Bowl")
pet_store_list.add_item("Collars")
pet_store_list.add_item("Flea collars")

pet_store_list.remove_item("Flea collars")

pet_store_list.add_item("Frisbee")

pet_store_list.remove_item("Bone")

pet_store_list.view_list()