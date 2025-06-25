import os
import random

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
subtotal = 0
taxed_amount = 0
rounded_amount = 0
price_RM = 0
payment_method = 0
total_price = 0
total_price_with_discount = 0
final_price = 0
order_number_list = []

sc_product_id_dict = {}
sc_customer_details_dict = {"customer_name": None,
                            "customer_contact": None
    }

order_number = ()
discount_rates_list = {"P": 0.5, "G": 0.25, "N": 0.1}
order_history = {}
purchase_list = []

# function to refresh the inventory when a any changes is made to the inventory
def refresh_inventory():
    global product_dict  # Assuming product_dict is used to hold inventory data
    
    # Read the inventory.txt file and update product_dict
    product_dict = {}
    with open("inventory.txt", "r") as file:
        lines = file.readlines()[1:]  # Skip the header line

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

    print("Inventory data refreshed.\n")


#self-defined function to add product into shopping cart                  
def add_product():
    global total_price 
    
    while True: 
        print("\n>>>>ADD PRODUCT<<<<") 
        sc_product_id = str(input(">Enter product ID to add into shopping cart (0 to option):")).upper() #enter the id of the item to add to the shopping cart
        if sc_product_id == "0": #sentinals "0"
            break
        elif sc_product_id in product_dict: #check whether the id is repeated and prompt error
            if sc_product_id in sc_product_id_dict:
                print("\n*ERROR* - Product already exist in the shopping cart\n")
                
            elif product_dict[sc_product_id]["quantity"] == 0: #check whether there is at least 1 qty available for the item
                print("\n*ERROR* - Product out of stock")
                
            else:
                sc_product_id_dict[sc_product_id] = { #store the product details into the shopping cart dictionary 
                    "name":product_dict[sc_product_id]["name"],
                    "qty": 1,
                    "price": product_dict[sc_product_id]["price"],
                    "total_price": product_dict[sc_product_id]["price"]
                    }
                display_shoppingcart() #display any changes made
        else:
            print("*ERROR* - Product does not exist in inventory ") #prompt error if item does not exist in inventory


#self define function to display shopping cart
def display_shoppingcart(discount=0):
    global subtotal,taxed_amount,rounded_amount,price_RM,total_price
    os.system('cls' if os.name == 'nt' else 'clear') #clear screen for better visibility
    
    print("\n")
    print("="*73)
    print(" "*31,"SALES MODEDULES"," "*20)
    print("="*73)
    print(f'Customer Name: {sc_customer_details_dict["customer_name"]}')
    print(f'Customer Contact: {sc_customer_details_dict["customer_contact"]}')
    print("-"*73)
    print(f'{"Product ID":<15}{"Product Name":<22}{"UnitPrice(RM)":<19}{"Qty":<7}{"Price(RM)"}')
    print("-"*73)

    total_quantity = 0 

    if not bool(sc_product_id_dict): #check if the shopping cart is empty (bool function will return a "False" if dict is empty)
        print("\n(empty shopping cart)\n") #if yes, display a message 
    else:
        for product_id in sc_product_id_dict: #display every item details in the shopping cart dict
            total_price = (sc_product_id_dict[product_id]["price"] * sc_product_id_dict[product_id]["qty"])
            sc_product_id_dict[product_id]["total_price"] = total_price
            print(f'{product_id:<14} {sc_product_id_dict[product_id]["name"]:<24} {sc_product_id_dict[product_id]["price"]:<16} {sc_product_id_dict[product_id]["qty"]:<7}{sc_product_id_dict[product_id]["total_price"]}')
            total_quantity += sc_product_id_dict[product_id]["qty"]
        
        
        
    #to calculate subtotal of the product in shopping cart
    subtotal = sum(float(product_dict[product_id]["price"]) * sc_product_id_dict[product_id]["qty"] for product_id in sc_product_id_dict)
    subtotal = float(subtotal)
    
    #to calculate tax amount
    tax = float(0.06)
    taxed_amount = float(subtotal*tax)
    taxed_price = float(subtotal + taxed_amount)
    
    #to round the total price to nearest 5 cents
        
    price_cent = float(round(taxed_price*100))
    rounding = round(price_cent/5)*5
    price_RM = float(rounding/100)
    rounded_amount = float(price_RM - taxed_price)
             
    print("-"*73)
    print(f'{"Subtotal : RM":>64}{subtotal:.2f}\n{"Sales Tax: RM":>64}{taxed_amount:.2f}\n{"Rounding: RM":>64}{rounded_amount:.2f}')
    print(f'\n\nTotal Qty: {total_quantity:<16}{"BALANCE: RM":>37}{price_RM:.2f}')
    print("-"*73)
    
    return subtotal,taxed_amount,rounded_amount,price_RM
    
            
    
#self-defined function to change quantity of product in shopping cart
def quantity_changer ():
    if not bool(sc_product_id_dict): #check if the shopping cart is empty, if yes,prompt an error and go back to sales menu
        display_shoppingcart()
        print("\n*ERROR* - Shopping Cart is empty! No quantity can be changed\n")
        option()
    else: 
        while True:
            print(">>>>EDIT QUANTITY<<<<") #ask for item's id that quantity need to be change
            product_to_change = str(input(">Please enter the ID of the product that you want to add (0 to option):")).upper()
            if product_to_change == "0": #sentinals "0"
                break
            else:
                while product_to_change not in sc_product_id_dict : #check whether ID entered is in shopping cart
                    print("\n*ERROR* - Please enter a valid product ID \n") #if yes prompt error, loop back to ask for id
                    product_to_change = str(input("Please enter the ID of the product that you want to add:")).upper()

                #enter the amount 
                print("[",product_dict[product_to_change]["name"],"]","had been chosen") 
                while True:
                    try: #try except to check for ValueError if string is entered
                        amount = int(input(">>Please enter the quantity that you want to purchase (min. 1 unit)/(0 to option):"))
                        if amount > product_dict[product_to_change]["quantity"]: #check whether quantity in inventory is sufficient for the change
                            print("\n")
                            print(f'*ERROR* - Insufficient stocks(only {product_dict[product_to_change]["quantity"]} unit(s) left)')
                            print("\n")   
                        elif amount == 0: #sentinals "0"
                            break
                        elif amount < 0: #prompt eror when quantity entered is smaller than 0
                            print("*\nERROR* - Please enter a valid quantity (min.1)\n")
                        elif amount > 0: #change the quantity according to user's input by updating the sc dict
                            sc_product_id_dict[product_to_change]["qty"] =  amount
                            display_shoppingcart()
                            break
                            
                    except ValueError: 
                        print("*\nERROR* - Please enter a valid quantity (min.1)\n")
                    
                
            



#self_defined function to delete product from the shopping cart
def del_product():
    while True:
        print("\n>>>>DELTE PRODUCT<<<<")
        sc_delete_id = str(input(">Enter product ID to DELETE from shopping cart (0 to option):")) #user input for id to delete
        
        if sc_delete_id == "0": #sentinals "0"
            break
        
        elif sc_delete_id in sc_product_id_dict: #check if item exist in sc dictionary
            sc_product_id_dict.pop(sc_delete_id)
            display_shoppingcart()
            
        else:
            print("\n*ERROR* - Product not found in shopping cart\n")  #prompt error if item does not exist in sc dict
            
            
#self defined function to add/edit customer details
def add_customer_details():
        while True:
            print("\n>>>>ADD/EDIT CUSTOMER's DETAILS<<<<") 
            customer_name = str(input("Enter Customer Name (0 to option):")) #enter name
            if customer_name != "0": #sentinals "0"
                sc_customer_details_dict.update({"customer_name":customer_name}) #update the customer_details dict with the input
                customer_contact = str(input("Enter Customer Contacts no (0 to option):"))
                if customer_contact != "0":
                    sc_customer_details_dict.update({"customer_contact":customer_contact})
                    break
                else:
                    break
            else:
                break


# Function to calculate membership discount
def calculate_discount(total_price, membership_id):
    if membership_id[0] not in discount_rates_list:
        print("Invalid ID!")
        return total_price
    else:
        discount_rate = discount_rates_list[membership_id[0]]
        discounted_price = total_price * (1 - discount_rate)
        discounted_price_in_cents = float(round(discounted_price*100))
        rounding2 = round(discounted_price_in_cents/5)*5
        discounted_price_rounded = float(rounding2/100)
        
        return discounted_price_rounded
    

#SDF to make payment
def payment():
    global payment_method,total_price_with_discount
    if not bool(sc_product_id_dict): #check if sc is empty
        print("*ERROR* - Shopping Cart is empty ")
        option()
    else:
        membership_id = input("Enter membership ID (first digit must be P, G, or N): ") #membership check
        total_price_with_discount = calculate_discount(price_RM, membership_id)
        payment_choice = str(input("Choose a Payment Method: \n(1)Credit/Debit Card \n(2)E-Wallet \n(3)Cash\nEnter your payment method >> "))
        
        while True:
            #choose payment method
            if payment_choice == "1":
                payment_method = str("CreditDebit Card")
                return payment_choice
            elif payment_choice == "2":
                payment_method = str("E-Wallet")
                return payment_choice
            elif payment_choice == "3":
                payment_method = str("Cash")
                return payment_choice
            else: #check for invalid input
                print("*Error* - Please Enter a valid option")
                payment_method = str(input("\nChoose a Payment Method: \n(1)Credit/Debit Card \n(2)E-Wallet \n(3)Cash\nEnter your payment method:"))
                
                
#self-define function to update the quantity of the inventory after a purchase in made                
def quantity_update (): 
    global subtotal,taxed_amount,rounded_amount,price_RM,payment_method,total_price,total_price_with_discount,sc_product_id_dict,sc_customer_details_dict,order_number #ask the function to alter the global function
    
    for sc_product_id in sc_product_id_dict: #update the qty of every item purchase in the sc dict
        product_dict[sc_product_id]["quantity"] -= sc_product_id_dict[sc_product_id]["qty"]

    with open('inventory.txt', 'w') as file:
        
        file.write('id,name,price,quantity\n') #write the header for the txt.file

        for product_id, details in product_dict.items():
            file.write(f'{product_id},{details["name"]},{details["price"]},{details["quantity"]}\n') #update the inventory.txt files with the new quantity


    #initialize the whole shopping cart for next purchase
    subtotal = 0
    taxed_amount = 0
    rounded_amount = 0
    price_RM = 0
    payment_method = 0
    total_price = 0
    total_price_with_discount = 0
            
    sc_product_id_dict = {}
    sc_customer_details_dict = {"customer_name": None,
                                                "customer_contact": None
                        }
    order_number = ()
    order_history = {}
    purchase_list = []

    

#SDF to create a order number 
def order_number_generator(): 
    global order_number
    from datetime import datetime
    import random
    
    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime("%Y%m%d%H%M")
    
    order_random = random.randint(1,9999)
    order_number = f'NK-{formatted_datetime}{order_random:04}'
    return order_number


    print(f'Generated Order Number: {order_number}')

#SDF to display the receipt after payment is made
def receipt_generator():
    import random
    from datetime import datetime
 
    # Receipt header
    print("\n Receipt will be shown below")
    print("-------------------------------------------------")
    print()
    print(' /$$   /$$ /$$$$$$ /$$   /$$ /$$$$$$$$')
    print('| $$$ | $$|_  $$_/| $$  /$$/| $$_____/')
    print('| $$$$| $$  | $$  | $$ /$$/ | $$      ')
    print('| $$ $$ $$  | $$  | $$$$$/  | $$$$$   ')
    print('| $$  $$$$  | $$  | $$  $$  | $$__/   ')
    print('| $$|  $$$  | $$  | $$|  $$ | $$      ')
    print('| $$ |  $$ /$$$$$$| $$ |  $$| $$$$$$$$')
    print('|__/  |__/|______/|__/  |__/|________/')
    print()
    print("          Nike Malaysia      ")
    print("-------------------------------------------------")
    print("              SALES INVOICE                   ")
    print("-------------------------------------------------")

    # Store information
    print("  Store Name: Nike Malaysia                   ")
    print("  Address: 123, Jalan Perak 4                 ")
    print("  Phone: +60 4399101                          ")
    print("  Date: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "                   ")
    print(f'  Transaction #:{order_number}                         ')
    print(f' \n  Customer Name: {sc_customer_details_dict["customer_name"]}\n  Customer Contact: {sc_customer_details_dict["customer_contact"]}')

    # Product details
    print("-------------------------------------------------")
    print("                ITEMS PURCHASED               ")
    print("-------------------------------------------------")
    print(f'{"ITEMS":<14}{"NAME":<23}{"AMOUNT(RM)":>11}')
    for product_id in sc_product_id_dict:
        print(f'{product_id:<11}{sc_product_id_dict[product_id]["name"] + " x" + str(sc_product_id_dict[product_id]["qty"]):<20}{sc_product_id_dict[product_id]["total_price"]:>16}')

    # Subtotal and taxes
    print("-------------------------------------------------")
    print(f"  Subtotal: RM{subtotal:.2f}                        ")
    print(f"  Taxes : RM{taxed_amount:.2f}                          ")
    print(f'  Rounding: RM{rounded_amount:.2f}')
    print(f'  Discount(Membership): RM -{price_RM - total_price_with_discount:.2f}')
    print("-------------------------------------------------")
    print(f"  Balance: RM{price_RM - (price_RM - total_price_with_discount):.2f}             ")

    # Payment information
    print(f'  Payment Method: {payment_method}                    ')

    # Receipt footer
    print("-------------------------------------------------")


# SDF to exit the sales modules
def exit_modules():
    
    exit_option = str(input("Do you want to exit the sales modules (Y/N) >>")).upper()
    
            
    if exit_option == "Y":
        print("Thank you for using the program")
    elif exit_option == "N":
        display_shoppingcart ()
        option ()
    else:
        print("\n*ERROR* - Please enter a valid option")
        exit_option = str(input("Do you want to exit the sales modules (Y/N) >>")).upper()

        
        

def save_receipt():
    global order_history,order_number,purchase_list,price_RM,total_price_with_discount,payment_method

    for product_id in sc_product_id_dict:
        item_to_save = (f'{product_id}|{sc_product_id_dict[product_id]["name"] + " x" + str(sc_product_id_dict[product_id]["qty"])}')
        purchase_list.append(item_to_save)

    final_price = price_RM - (price_RM - total_price_with_discount)        

    order_history[order_number] = {
        "items": purchase_list,
        "payment_amount": final_price,
        "payment_method": payment_method,
        "customer_details": sc_customer_details_dict
    }

    if not os.path.isfile('sales_history.txt'):
        with open('sales_history.txt', 'w') as file:
            file.write('order_number/item_purchased/payment_amount/payment_method/customer_details\n')

            
    with open('sales_history.txt', 'a') as file:
        for order_num, order_details in order_history.items():
            items_purchased = str(purchase_list)
            payment_amount = str(order_details['payment_amount'])
            payment_method = order_details['payment_method']
            customer_details = ', '.join(f"{key}: {value}" for key, value in order_details['customer_details'].items())
            file.write(f"{order_num}/{items_purchased}/RM{payment_amount}/{payment_method}/{customer_details}\n")
        
    print("Order had been updated to file:'order_history'.txt")
    order_history = {}
    purchase_list = []
    
    

    

#self-defined function for sales menu 
def option ():
    option_choice = str(input("Option:\n(1)Change Quantity \n(2)Add Product \n(3)Delete Product \n(4)Edit Customer's Details \n\n(X)Exit\n(P)AY\n\n>>> Enter your Option:")).upper()
    while True:
        if option_choice == "1":
            refresh_inventory()
            quantity_changer ()
            display_shoppingcart()
            option_choice = str(input("Option:\n(1)Change Quantity \n(2)Add Product \n(3)Delete Product \n(4)Edit Customer's Details \n\n(X)Exit\n(P)AY\n\n>>> Enter your Option:")).upper()
        elif option_choice == "2":
            refresh_inventory()
            add_product ()
            display_shoppingcart()
            option_choice = str(input("Option:\n(1)Change Quantity \n(2)Add Product \n(3)Delete Product \n(4)Edit Customer's Details \n\n(X)Exit\n(P)AY\n\n>>> Enter your Option:")).upper()
        elif option_choice == "3":
            refresh_inventory()
            del_product()
            display_shoppingcart()
            option_choice = str(input("Option:\n(1)Change Quantity \n(2)Add Product \n(3)Delete Product \n(4)Edit Customer's Details \n\n(X)Exit\n(P)AY\n\n>>> Enter your Option:")).upper()
        elif option_choice == "4":
            add_customer_details()
            display_shoppingcart()
            option_choice = str(input("Option:\n(1)Change Quantity \n(2)Add Product \n(3)Delete Product \n(4)Edit Customer's Details \n\n(X)Exit\n(P)AY\n\n>>> Enter your Option:")).upper()
        elif option_choice == "X":
            exit_modules()
            return
        elif option_choice == "P":
            payment()
            order_number_generator()
            receipt_generator()
            save_receipt()
            quantity_update()
            refresh_inventory()
            exit_modules()
            return
        else:
            print("*\nERROR* - Please enter a valid option\n")
            option_choice = str(input("Option:\n(1)Change Quantity \n(2)Add Product \n(3)Delete Product \n(4)Edit Customer's Details \n\n(X)Exit\n(P)AY\n\n>>> Enter your Option:")).upper()
                    
            
    
    
    
        
#-------------------------------------------------------------FLOW START HERE----------------------------------------------------------------------------------------------------------------------------------------------------------#
#-------------------------------------------------------------FLOW START HERE----------------------------------------------------------------------------------------------------------------------------------------------------------#

if __name__ == "__main__":
    display_shoppingcart()
    refresh_inventory()
    if not bool(product_dict): #check if inventory is empty
        print(">>EMPTY INVENTORY<<")
        print("Please add product in the inventory before using sales modules")
        exit_modules()
    else:
        option()
        
        


