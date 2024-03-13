import sqlite3

class Product:
    def __init__(self, table_name):
        self.table_name = table_name
        self.conn = sqlite3.connect('restaurant.db')
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS {self.table_name} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                price REAL NOT NULL
            )
        ''')
        self.conn.commit()

    def add_product(self, name, price):
        self.cursor.execute(f"INSERT INTO {self.table_name} (name, price) VALUES (?, ?)", (name, price))
        self.conn.commit()
        print(f"{name} added.")

    def delete_proudct(self, product_id):
        self.cursor.execute(f"DELETE FROM {self.table_name} WHERE id=?", (product_id,))
        self.conn.commit()
        print(f"Product with {product_id} id has been deleted.")

    def update_product(self, product_id, name, price):
        self.cursor.execute(f"UPDATE {self.table_name} SET name=?, price=? WHERE id=?", (name, price, product_id))
        self.conn.commit()
        print(f"Product with {product_id} ID has been updated.")

    def list_the_products(self):
        self.cursor.execute(f"SELECT id, name, price FROM {self.table_name}")
        products = self.cursor.fetchall()
        print(f"\n***** {self.table_name.upper()} *****")
        for product in products:
            print(f"ID: {product[0]}, Name: {product[1]}, Price: {product[2]} TL")


class Food(Product):
    def __init__(self):
        super().__init__('food')


class Drink(Product):
    def __init__(self):
        super().__init__('drink')


class Orders:
    def __init__(self):
        self.conn = sqlite3.connect('restaurant.db')
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                food_id INTEGER NOT NULL,
                drink_id INTEGER NOT NULL,
                food_amount INTEGER NOT NULL,
                drink_amount INTEGER NOT NULL,
                total_price REAL NOT NULL,
                FOREIGN KEY (food_id) REFERENCES food(id),
                FOREIGN KEY (drink_id) REFERENCES drink(id)
            )
        ''')
        self.conn.commit()

    def give_order(self, food_id, drink_id, food_amount, drink_amount):
        food_price = self.get_product_price('food', food_id)
        drink_price = self.get_product_price('drink', drink_id)
        total_price = (food_price * food_amount) + (drink_price * drink_amount)

        self.cursor.execute("INSERT INTO orders (food_id, drink_id, food_amount, drink_amount, total_price) VALUES (?, ?, ?, ?, ?)",
                            (food_id, drink_id, food_amount, drink_amount, total_price))
        self.conn.commit()

        print(f"{food_amount} amount {self.get_product_name('food', food_id)} and {drink_amount} amount {self.get_product_name('drink', drink_id)} "
              f"products have been ordered. Total Price: {total_price} TL")

    def show_orders(self):
        self.cursor.execute('''
            SELECT orders.id, food.name AS food, drink.name AS drink, 
            orders.food_amount, orders.drink_amount, orders.total_price
            FROM orders
            INNER JOIN food ON orders.food_id = food.id
            INNER JOIN drink ON orders.drink_id = drink.id
        ''')
        orders = self.cursor.fetchall()

        if not orders:
            print("Have not received orders yet.")
        else:
            print("\n***** ORDERS *****")
            for order in orders:
                print(f"ID: {order[0]}, Food: {order[1]}, Drink: {order[2]}, "
                      f"Food Amount: {order[3]}, Drink Amount: {order[4]}, Total Price: {order[5]} TL")

    def get_product_price(self, table, product_id):
        self.cursor.execute(f"SELECT price FROM {table} WHERE id=?", (product_id,))
        price = self.cursor.fetchone()
        if price:
            return price[0]
        else:
            print("Could not found any product.")
            return 0

    def get_product_name(self, table, product_id):
        self.cursor.execute(f"SELECT name FROM {table} WHERE id=?", (product_id,))
        name = self.cursor.fetchone()
        if name:
            return name[0]
        else:
            print("Could not found any product.")
            return ""


class RestaurantManagementSystem:
    def __init__(self):
        self.food = Food()
        self.drink = Drink()
        self.orders = Orders()
        
    def give_order(self):
        self.food.list_the_products()
        food_id = int(input("Enter the ID of the product you want to order: "))
        food_amount = int(input("Enter amount of products: "))

        self.drink.list_the_products()
        drink_id = int(input("Enter the ID of the product you want to order:  "))
        drink_amount = int(input("Enter amount of products:  "))

        self.orders.give_order(food_id, drink_id, food_amount, drink_amount)

    def show_menu(self):
        while True:
            print("\n***** RESTAURANT MENU *****")
            print("1. Add Food")
            print("2. Add Drink")
            print("3. Delete Food")
            print("4. Delete Drink")
            print("5. Update Food")
            print("6. Update Drink")
            print("7. Show Foods")
            print("8. Show Drinks")
            print("9. Show Orders")
            print("10. Give Order")
            print("0. Exit")

            action = input("Please enter an action: ")

            if action == "1":
                self.food.add_product(input("Food Name: "), float(input("Food Price: ")))
            elif action == "2":
                self.drink.add_product(input("Drink Name: "), float(input("Drink Price: ")))
            elif action == "3":
                self.food.list_the_products()
                self.food.delete_product(int(input("Enter the ID of product you want to delete: ")))
            elif action == "4":
                self.drink.list_the_products()
                self.drink.delete_product(int(input("Enter the ID of product you want to delete: ")))
            elif action == "5":
                self.food.list_the_products()
                product_id = int(input("Enter the ID of product you want to update: "))
                self.food.update_product(product_id, input("New Food name: "), float(input("New Food Price: ")))
            elif action == "6":
                self.drink.list_the_products()
                product_id = int(input("Enter the ID of product you want to update "))
                self.drink.update_product(product_id, input("New Drink Name: "), float(input("New Drink Price: ")))
            elif action == "7":
                self.food.list_the_products()
            elif action == "8":
                self.drink.list_the_products()
            elif action == "9":
                self.orders.show_orders()
            elif action == "10":
                self.give_order()
            elif action == "0":
                break
            else:
                print("Invalid action, please try again.")


if __name__ == "__main__":
    restaurant = RestaurantManagementSystem()
    restaurant.show_menu()
