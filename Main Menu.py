import os
import inventory_system
import Sales_modules


def sales():
#creating the inventory files if it does not exist
    if not os.path.isfile('inventory.txt'):
        with open('inventory.txt', 'w') as file:
            file.write('id,name,price,quantity\n')  # Writing the header line to the file

    #reading txt files and convert to a dictionary
    product_dict = {}

    with open("inventory.txt", "r") as file:
        lines = file.readlines()[1:] #skip the hedear line

        # Iterate over rows and print data
        for line in lines:
            row = line.strip().split(',')
            product_id = row[0]
            name = row[1]
            price = float(row[2])
            quantity = int(row[3])

            product_dict[product_id] = {
                "name": name,
                "price": price,
                "quantity": quantity
            }
    


        
    #initilization
    Sales_modules.subtotal = 0
    Sales_modules.taxed_amount = 0
    Sales_modules.rounded_amount = 0
    Sales_modules.price_RM = 0
    
    Sales_modules.payment_method = 0
    Sales_modules.total_price = 0
    Sales_modules.total_price_with_discount = 0
    Sales_modules.order_number_list = []
        
    Sales_modules.sc_product_id_dict = {}
    Sales_modules.sc_customer_details_dict = {"customer_name": None,
                                    "customer_contact": None
            }
        
    Sales_modules.order_number = ()
    Sales_modules.discount_rates_list = {"P": 0.5, "G": 0.25, "N": 0.1}
        
    Sales_modules.display_shoppingcart()
    Sales_modules.refresh_inventory()
    if not bool(Sales_modules.product_dict):
        print(">>EMPTY INVENTORY<<")
        print("Please add product in the inventory before using sales modules")
        Sales_modules.exit_modules()
    else:
        Sales_modules.option()





def inventory ():
    if not os.path.isfile('inventory.txt'):
        with open('inventory.txt', 'w') as file:
            file.write('id,name,price,quantity\n')  # Writing the header line to the file

    inventory_system.INVENTORY_FILE = 'inventory.txt'
    inventory_system.STOCK_THRESHOLD = 5
    
    while True:
        inventory_system.choice = inventory_system.get_user_choice()  # Get the user's choice from the main menu

        if inventory_system.choice == '1':  # Option to add a new item
            # Collect item details from the user
            inventory_system.read_inventory()
            inventory_system.item_id = input('>>Enter ITEM ID to be ADDED (e.g., 001): ')
            inventory_system.item_name = input('>>Enter ITEM NAME : ')
            inventory_system.item_price = input('>>Enter ITEM PRICE(RM): ')
            inventory_system.item_quantity = input('>>Enter ITEM QUANTITY: ')
    
    
            # Validate and add the item
            if inventory_system.is_valid_input(inventory_system.item_id, inventory_system.item_price, inventory_system.item_quantity):
                inventory_system.create_item(inventory_system.item_id, inventory_system.item_name, inventory_system.item_price, inventory_system.item_quantity)
            else:
                print('Invalid input, the item was not added.')
                input("\nPress Enter to continue...")
    
        elif inventory_system.choice == '2':  # Option to view the inventory
            inventory_system.read_inventory()
            input("\nPress Enter to continue...")
    
     
    
        elif inventory_system.choice == '3':  # Option to update an existing item
            # Collect new details for the item
            inventory_system.read_inventory()
            inventory_system.item_id_to_update = input('>>Enter the ITEM ID to UPDATE (e.g., 001): ')
            inventory_system.new_name = input('>>Enter NEW NAME(remain if unchanged): ')
            inventory_system.new_price = input('>>Enter NEW PRICE(RM)(remain if unchanged): ')
            inventory_system.new_quantity = input('>>Enter NEW QUANTITY(remain if unchanged): ')
            inventory_system.update_item(inventory_system.INVENTORY_FILE, inventory_system.item_id_to_update, inventory_system.new_name, inventory_system.new_price, inventory_system.new_quantity)
        
            input("\nPress Enter to continue...")
    
        elif inventory_system.choice == '4':  # Option to delete an item
            inventory_system.read_inventory()
            inventory_system.item_id_to_delete = input('>>Enter the ITEM ID to DELETE (e.g., 001): ')
            inventory_system.delete_item('inventory.txt', inventory_system.item_id_to_delete)
    
        elif inventory_system.choice == '5':  # Option to check stock alert
            inventory_system.read_inventory()
            inventory_system.stock_check_alert('inventory.txt')
    
        elif inventory_system.choice == 'X':  # Option to exit the program
            print('Exiting the program.')
            break 
    
    
    
    
    


def logo():
    os.system('cls' if os.name == 'nt' else 'clear') #clear the screen for better visibility
    
    print("="*42)
    print(f'{"NIKE MALAYSIA SDN. BHD":>30}')
    print("="*42)

    print()
    print("/$$   /$$ /$$$$$$ /$$   /$$ | $$$$$$$$ ")
    print("| $$$ | $$|_  $$_/| $$  /$$/| $$_____/")
    print("| $$$$| $$  | $$  | $$ /$$/ | $$      ")
    print("| $$ $$ $$  | $$  | $$$$$/  | $$$$$   ")
    print("| $$  $$$$  | $$  | $$  $$  | $$__/   ")
    print("| $$|  $$$  | $$  | $$|  $$ | $$      ")
    print("| $$ |  $$ /$$$$$$| $$ | $$| $$$$$$$$")
    print("|__/  |__/|______/|__/  |__/|________/")
    print()
    print("-"*42)
    print("Welcome to NIKE MALAYSIA POS SYSTEM!")
    print("-"*42)
    print(">>>MAIN MENU<<<")
    print("\n(1)SALES MODULES\n  -Make a purchase\n\n(2)INVENTORY SYSTEM\n  -Add Item\n  -Edit stocks\n  -Delete Item\n  -Stock Alerts\n\n(3)SALES HISTORY\n  -Check Sales history\n\n(X)EXIT program\n")
    print("-"*42)


    
def display_history():
    
    os.system('cls' if os.name == 'nt' else 'clear') #clear the screen for better visibility

    print("="*42)
    print(f'{"Order History":>25}')
    print("="*42)

    # Creating the inventory file if it does not exist
    if not os.path.isfile('sales_history.txt'):
        with open('sales_history.txt', 'w') as file:
            file.write('id,name,price,quantity\n')  # Writing the header line to the file
    
    # Read the content of the order history file
    with open('sales_history.txt', 'r') as file:
        # Skip the header line
        next(file)
        
        # Read all lines and process each order
        for line in file:
            order_data = line.strip().split('/')  # Split the content by '/'
            
            # Assuming each line has fixed data structure
            order_number = order_data[0]
            items_purchased = order_data[1]
            payment_amount = order_data[2]
            payment_method = order_data[3]
            customer_details = order_data[4]
            
            print("Order Number:", order_number)
            print("Items Purchased:", items_purchased)
            print("Payment Amount:", payment_amount)
            print("Payment Method:", payment_method)
            print("Customer Details:", customer_details)
            print()
            
    input("Press enter to go back to main menu.......")
    
    

def main_menu (): #SDF to get user's option for the main menu
    mm_option = str(input("Enter your option >>"))
    while mm_option != "X": #ask for option when sentinal "X" was not entered
        
        if mm_option == "2": #option to run the inventory system
            inventory()
            logo()
            mm_option = str(input("Enter your option >>"))
    
        elif mm_option == "1": #option to run the sales modules
            sales()
            logo()
            mm_option = str(input("Enter your option >>"))
            
        elif mm_option == "3":
            display_history()
            logo()
            mm_option = str(input("Enter your option >>"))
    
        else: #prompt error if invalid option was entered an ask again
            print("*ERROR* - Please enter a valid option")
            logo()
            mm_option = str(input("Enter your option >>"))
            
    print("Thanks for using the program")
            
           
if __name__ == "__main__": #state the main_menu .py as the main files to run first
    logo()
    main_menu ()
