from product_inventory_cli import db
from product_inventory_cli.exceptions import (
    InsufficientStockError,
    InvalidQuantityError,
    NegativePriceError,
    NegativeStockError,
    ProductHasOrdersError,
    ProductNotFoundError,
)

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
        try:
            choice = int(input("Enter your choice: "))
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue

        if choice == 1:
            try:
                product = input("Enter the product name to add: ")
                price = int(input("Enter price of the product: "))
                stock = int(
                    input("Enter the available stock for the product: "))

                product = db.add_product(product, price, stock)
                print(product)
            except ValueError:
                print("Invalid input. Please enter a number.")
            except NegativePriceError:
                print("Price cannot be negative")
            except NegativeStockError:
                print("Stock cannot be negative")

        elif choice == 2:
            try:
                product_id = int(input("Enter the product id: "))

                product = db.get_product(product_id)
                print(product)
            except ValueError:
                print("Invalid input. Please enter a number.")
            except ProductNotFoundError:
                print("Selected product id doesn't exist.")

        elif choice == 3:
            products = db.list_products()
            print(products)

        elif choice == 4:
            try:
                product_id = int(
                    input("Enter the product id of product to update: "))
                price = int(input("Enter the updated price: "))
                stock = int(input("Enter the udpated stock: "))

                updated_product = db.update_product(product_id, price, stock)
                print(updated_product)
            except ValueError:
                print("Invalid input. Please enter a number.")
            except NegativePriceError:
                print("Price cannot be negative")
            except NegativeStockError:
                print("Stock cannot be negative")
            except ProductNotFoundError:
                print("Selected product id doesn't exist.")

        elif choice == 5:
            try:
                product_id = int(
                    input("Enter the product id to delete the product: "))

                deleted_product = db.delete_product(product_id)
                print(deleted_product)
            except ValueError:
                print("Invalid input. Please enter a number.")
            except ProductNotFoundError:
                print("Cannot delete product as it doesn't exist.")
            except ProductHasOrdersError:
                print("Cannot delete product as it has existing orders")

        elif choice == 6:
            try:
                product_id = int(
                    input("Enter the product id to buy the product: "))
                quantity = int(input("Enter the quantity of product: "))

                order = db.buy_product(product_id, quantity)
                print(order)
            except ValueError:
                print("Invalid input. Please enter a number.")
            except InvalidQuantityError:
                print("Quantity must be 1 or more")
            except InsufficientStockError:
                print("Not enough stock for this product")
            except ProductNotFoundError:
                print("Selected product id doesn't exist.")

        elif choice == 7:
            break


if __name__ == "__main__":
    main()
