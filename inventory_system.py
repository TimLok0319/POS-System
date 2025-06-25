import os
from os import system, name


#creating the inventory files if it does not exist
if not os.path.isfile('inventory.txt'):
    with open('inventory.txt', 'w') as file:
        file.write('id,name,price,quantity\n')  # Writing the header line to the file

# Constants for easy configuration and maintenance
INVENTORY_FILE = 'inventory.txt'
STOCK_THRESHOLD = 5

# Function to clear the screen for better readability in the console
def clear_screen():
    # Check the operating system
    if name == 'nt':  # 'nt' represents Windows
        _ = system('cls')  # Clear screen command for Windows
    else:  # For Unix-like systems (macOS, Linux)
        _ = system('clear')  # Clear screen command for Unix/Linux/Mac
        

def is_valid_input(id, price, quantity):
    try:
        with open('inventory.txt', 'r') as txt_file:
            for line in txt_file:
                row = line.strip().split(',')
                if row and id == row[0]:
                    print(f'Error: ID {id} already exists.')
                    return False  # Duplicate ID, so return False

        # Check if price and quantity are numbers
        float(price)  # Convert price to float for validation
        int(quantity)  # Convert quantity to integer for validation

    except ValueError:
        # If conversion fails, it means price and quantity are not proper numbers
        print('Error: Price and quantity must be numbers.')
        return False
    
    return True  # Validation passed, return True
    

# Function to validate if the provided price and quantity are numbers, used in updating items
def is_valid_price_and_quantity(price, quantity):
    print(f"Checking price: {price}, quantity: {quantity}")  # Debugging line
    try:
        float(price)
        int(quantity)
    except ValueError:
        print('Error: Price and quantity must be numbers.')
        return False
    return True


# Function to display the main menu of the application
def display_main_menu():
    clear_screen()  # Clear the screen for better visibility
    print('=' * 50)
    print('NIKE INVENTORY SYSTEM'.center(50))
    print('=' * 50)
    print('\nMain Menu:\n')
    print('(1)Add Item')
    print('(2)View Items')
    print('(3)Update Item')
    print('(4)Delete Item')
    print('(5)Stock Alert')
    print('\n(X)Exit')
    print('-' * 50)

# Function to get the user's choice from the main menu
def get_user_choice():
    while True:
        display_main_menu()  # Show the main menu
        choice = input("Enter your option >> ").strip().upper()  # Get user input
        if choice in ['1', '2', '3', '4', '5', '6','X']:
            return choice  # Valid choice, return it
        else:
            print("Invalid choice. Please try again.")  # Invalid choice, prompt again


def create_item(id, name, price, quantity):
    # Format the item's data
    item_data = f"{id},{name},{price},{quantity}\n"

    # Append the new item to the inventory file
    with open('inventory.txt', 'a') as txt_file:
        txt_file.write(item_data)  # Write the new item data into the text file
        print(f'Item {name} with ID {id} added successfully.')

    input("\nPress Enter to continue...")  # Wait for user acknowledgment
    
    
# Function to read and display the entire inventory
def read_inventory():
    clear_screen()
    try:
        with open('inventory.txt', 'r') as txt_file:
            # Read all lines from the file
            lines = txt_file.readlines()

            # Display the header with fixed width
            print("="*55)
            print(f'{"Inventory":>29}')
            print("="*55)
            print('-' * 55)
            print('{:<10} {:<24} {:<10} {:<10}'.format('ID', 'Name', 'Price(RM)', 'Qty'))
            print('-' * 55)  

            # Iterate through lines starting from the second line (skipping header)
            for line in lines[1:]:
                # Split the line by commas to get individual elements
                row = line.strip().split(',')
                if len(row) == 4:  # Check if there are four elements (ID, Name, Price, Quantity)
                    # Ensure price has two decimal places
                    row[2] = '{:.2f}'.format(float(row[2]))
                    print('{:<10} {:<25} {:<10} {:<10}'.format(*row))
                else:
                    print("Error: Malformed data in inventory file")

            # Add a newline after the table for better separation
            print()

    except FileNotFoundError:  # Check whether the file is in the expected directory
        print("Error: The inventory file does not exist.")
    except IOError: 
        print("Error: An I/O error occurred while handling the inventory file.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def update_item(file_name, id_to_update, new_name, new_price, new_quantity):
    if not is_valid_price_and_quantity(new_price, new_quantity):
        print('Invalid input, the item was not updated.')
        return

    inventory = []  # Temporary list to hold inventory data
    updated = False  # Flag to check if the item was updated

    with open(file_name, 'r') as txt_file:
        for line in txt_file:
            row = line.strip().split(',')
            if row[0] == id_to_update:
                updated = True  # Item found and flag set to True
                row[1], row[2], row[3] = new_name, new_price, new_quantity  # Update the item details
            inventory.append(row)  # Add each row to the inventory list

    # Write the updated inventory back to the file
    with open(file_name, 'w') as txt_file:
        for row in inventory:
            txt_file.write(','.join(row) + '\n')  # Write each row to the text file

    if updated:
        print(f"Item with id {id_to_update} has been updated.")
    else:
        print('Item not found, no update made.')


def delete_item(file_name, id_to_delete):
    inventory = []  # Temporary list to hold inventory data
    item_found = False  # Flag to check if the item was found

    with open(file_name, 'r') as txt_file:
        for line in txt_file:
            row = line.strip().split(',')
            if row[0] == id_to_delete:
                item_found = True  # Item found and flag set to True
            else:
                inventory.append(row)  # Add other items to the temporary inventory list

    # If the item was not found, inform the user
    if not item_found:
        print(f'Item with id {id_to_delete} is not found')
        input("\nPress Enter to continue...")
        return

    # Write the updated inventory without the deleted item back to the file
    with open(file_name, 'w') as txt_file:
        for row in inventory:
            txt_file.write(','.join(row) + '\n')  # Write each row to the text file
        print(f'Item with id {id_to_delete} has been deleted')

    input("\nPress Enter to continue...")  # Wait for user input before returning
    

def stock_check_alert(file_name, threshold=5):
    clear_screen()
    print()
    print(">>Stock Alert<<")
    try:
        with open(file_name, 'r') as txt_file:
            lines = txt_file.readlines()
            for line in lines[1:]:  # Skip the header line
                data = line.strip().split(',')
                # Check if the stock is below the threshold
                if data[3].isdigit() and int(data[3]) < threshold:
                    print(f'Stock alert for product ID {data[0]}: only {data[3]} left in stock.')
    except FileNotFoundError:
        print("Error: The inventory file does not exist.")
    except IOError:
        print("Error: An I/O error occurred while handling the inventory file.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    input("\nPress Enter to continue...")  # Wait for user input before returning

# Main loop of the program
if __name__ == "__main__":
    while True:
        choice = get_user_choice()  # Get the user's choice from the main menu
    
        if choice == '1':  # Option to add a new item
            # Collect item details from the user
            read_inventory()
            item_id = input('>>Enter ITEM ID to be ADDED (e.g., 001): ')
            item_name = input('>>Enter ITEM NAME: ')
            item_price = input('>>Enter ITEM PRICE(RM): ')
            item_quantity = input('>>Enter ITEM QUANTITY: ')
    
    
            # Validate and add the item
            if is_valid_input(item_id, item_price, item_quantity):
                create_item(item_id, item_name, item_price, item_quantity)
            else:
                print('Invalid input, the item was not added.')
                input("\nPress Enter to continue...")
    
        elif choice == '2':  # Option to view the inventory
            read_inventory()
            input("\nPress Enter to continue...")
    
     
    
        elif choice == '3':  # Option to update an existing item
            # Collect new details for the item
            read_inventory()
            item_id_to_update = input('>>Enter the ITEM ID to UPDATE (e.g., 001): ')
            new_name = input('>>Enter NEW NAME(press enter if unchanged): ')
            new_price = input('>>Enter NEW PRICE(RM) (press enter if unchanged): ')
            new_quantity = input('>>Enter NEW QUANTITY (press enter if unchanged): ')
            update_item(INVENTORY_FILE, item_id_to_update, new_name, new_price, new_quantity)
        
            input("\nPress Enter to continue...")
    
        elif choice == '4':  # Option to delete an item
            read_inventory()
            item_id_to_delete = input('>>Enter the ITEM ID to DELETE (e.g., 001): ')
            delete_item('inventory.txt', item_id_to_delete)
    
        elif choice == '5':  # Option to check stock alert
            read_inventory()
            stock_check_alert('inventory.txt')
    
        elif choice == 'X':  # Option to exit the program
            print('Exiting the program.')
            break 
