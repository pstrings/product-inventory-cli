from product_inventory_cli import db

instructions = """
===== Product Inventory =====

1. Add product
2. Get product
3. List products
4. Update product
5. Delete product
6. Buy product
7. Exit

Choose an option:
"""


def main():
    while True:
        print(instructions)
        choice = input("Enter your choice: ")

        if choice == '1':
            product = input("Enter the product name to add: ")
            price = int(input("Enter price of the product: "))
            stock = int(input("Enter the available stock for the product: "))

            product = db.add_product(product, price, stock)
            print(product)

        elif choice == '2':
            product_id = int(input("Enter the product id: "))

            product = db.get_product(product_id)
            print(product)

        elif choice == '3':
            products = db.list_products()
            print(products)

        elif choice == '4':
            product_id = int(
                input("Enter the product id of product to update: "))
            price = int(input("Enter the updated price: "))
            stock = int(input("Enter the udpated stock: "))

            updated_product = db.update_product(product_id, price, stock)
            print(updated_product)

        elif choice == '5':
            product_id = int(
                input("Enter the product id to delete the product: "))

            deleted_product = db.delete_product(product_id)
            print(deleted_product)

        elif choice == '6':
            product_id = int(
                input("Enter the product id to buy the product: "))
            quantity = int(input("Enter the quantity of product: "))

            bought_product = db.buy_product(product_id, quantity)
            print(bought_product)

        elif choice == '7':
            break


if __name__ == "__main__":
    main()
