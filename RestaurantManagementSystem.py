from abc import ABC, abstractmethod
class MenuItem(ABC):
    def __init__(self, name, price, cuisine):
        self.name = name
        self.price = price
        self.cuisine = cuisine
        
    def __str__(self):
        return f"""
            Name: {self.name}
            Price: {self.price} TL
            cuisine: {self.cuisine}
        """
    @abstractmethod
    def display_info(self):
        pass
    
    @abstractmethod
    def update_info(self):
        pass
        
class FoodItem(MenuItem):
    def __init__(self, name, price, cuisine, ingredients):
        super().__init__(name, price, cuisine)
        self.ingredients = ingredients
        
    def __str__(self):
        return super().__str__() + f"""
            Ingredients: {','.join(self.ingredients)}
        """
    
    def display_info(self):
        print(self.__str__())
        
    def update_info(self):
        print("\nEnter new information (leave blank to keep current):")
        new_name = input(f"New Name ({self.name}): ") or self.name
        new_price = float(input(f"New Price ({self.price} TL): ") or self.price)
        new_cuisine = input(f"New Cuisine ({self.cuisine}): ") or self.cuisine
        new_ingredients = input(f"New Ingredients ({','.join(self.ingredients)}): ") or self.ingredients
        
        self.name = new_name
        self.price = new_price
        self.cuisine = new_cuisine
        self.ingredients = new_ingredients.split(',')
        
        print("Menu item information updated successfully.")
        
class DrinkItem(MenuItem):
    def __init__(self, name, price, cuisine, is_alcoholic):
        super().__init__(name, price, cuisine)
        self.is_alcoholic = is_alcoholic
        
    def __str__(self):
        return super().__str__() + f"""
            Alcoholic: {'Yes' if self.is_alcoholic else 'No'}
        """
    
    def display_info(self):
        print(self.__str__())
        
    def update_info(self):
        print("\nEnter new information (leave blank to keep current):")
        new_name = input(f"New Name ({self.name}): ") or self.name
        new_price = float(input(f"New Price ({self.price} TL): ") or self.price)
        new_cuisine = input(f"New Cuisine ({self.cuisine}): ") or self.cuisine
        new_alcoholic = input(f"Is it Alcoholic? (Yes/No) ({'Yes' if self.is_alcoholic else 'No'}): ") or self.is_alcoholic
        
        
        self.name = new_name
        self.price = new_price
        self.cuisine = new_cuisine
        self.is_alcoholic = new_alcoholic.lower() == "yes"
        
        print("Menu item information updated successfully.")
        

class Order:
    def __init__(self):
        self.items = []
        
    def add_item(self, item):
        self.items.append(item)
        
    def display_order(self):
        for item in self.items:
            item.display_info()
            
class Restaurant:
    def __init__(self):
        self.menu = []
        self.orders = []
        
    def display_menu(self):
        print("\nRestaurant Menu: ")
        if len(self.menu) == 0:
            print("The menu is empty for now.")
        else:  
            for index, item in enumerate(self.menu, start=1):
                print(f"{index}.", end="")
                item.display_info()
            
    def take_order(self):
        order = Order()
        while True:
            self.display_menu()
            choice = input("\nEnter the item number to add to the order (or 'done' to finish): ")
            if choice.lower() == "done":
                break
            
            try:
                choice_index = int(choice) - 1
                selected_item = self.menu[choice_index]
                order.add_item(selected_item)
                print(f"{selected_item.name} added to the order.")
            except (ValueError, IndexError):
                print("Invalid item number. Please try again.")
                
        self.orders.append(order)
        print("\nOrder placed successfully!")
        
    def display_orders(self):
        print("\nAll Orders: ")
        if len(self.orders) == 0:
            print("There are currently no orders")
        else:
            for index, order in enumerate(self.orders, start=1):
                print(f"\nOrder {index}: ")
                order.display_order()
            
    def add_menu_item(self):
        print("\nAdding a new menu item: ")
        item_type = input("Enter item type (food or drink): ").lower()
        if item_type == "food":
            name = input("Enter food name: ")
            price = float(input("Enter price: "))
            cuisine = input("Enter cuisine: ")
            ingredients = input("Enter ingredients (comma-separated): ").split(",")
            new_item = FoodItem(name, price, cuisine, ingredients)
        elif item_type == "drink":
            name = input("Enter drink name: ")
            price = float(input("Enter price: "))
            cuisine = input("Enter cuisine: ")
            is_alcoholic = input("Is it alcoholic? (yes or no): ").lower() == 'yes'
            new_item = DrinkItem(name, price, cuisine, is_alcoholic)
        else:
            print("Invalid item type. Please enter 'food' or 'drink'.")
            return
        self.menu.append(new_item)
        print(f"Menu item '{new_item.name}' added successfully.")
        
    def remove_menu_item(self):
        print("\nRemoving a menu item: ")
        item_name = input("Enter the name of the item to remove: ")
        for item in self.menu:
            if item.name.lower() == item_name.lower():
                self.menu.remove(item)
                print(f"Menu item '{item_name}' removed successfully.")
                return
        print(f"Menu item '{item_name}' not found.")
        
    def update_menu_item(self):
        print("\nUpdating a menu item: ")
        item_name = input("Enter the name of the item to update: ")
        for item in self.menu:
            if item.name.lower() == item_name.lower():
                item.update_info()
                return
        print(f"Menu item '{item_name}' not found.")
        

restaurant = Restaurant()

while True:
    print("\nRestaurant Management System Menu:")
    print("1. Display Menu")
    print("2. Take Order")
    print("3. Display Orders")
    print("4. Add Menu Item")
    print("5. Remove Menu Item")
    print("6. Update Menu Item")
    print("7. Exit")

    choice = input("Enter your choice (1-7): ")

    if choice == "1":
        restaurant.display_menu()
    elif choice == "2":
        restaurant.take_order()
    elif choice == "3":
        restaurant.display_orders()
    elif choice == "4":
        restaurant.add_menu_item()
    elif choice == "5":
        restaurant.remove_menu_item()
    elif choice == "6":
        restaurant.update_menu_item()
    elif choice == "7" or choice == "q" or choice == "Q":
        print("Exiting the Restaurant Management System. Goodbye!")
        break
    else:
        print("Invalid choice. Please enter a number between 1 and 7.")

