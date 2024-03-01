import csv
import os

def read_csv_file(file_path):
    """
    Reads data from a CSV file and returns it as a dictionary, along with a list of keys (town names)

    Args:
        file_path (str): Path to the CSV file.

    Returns:
        dict: A dictionary containing the data read from the file.
        list: A list containing the list of every town in the CSV.
    """

    # Dictionary to store each piece of data
    trade_data = {}

    with open(file_path, 'r') as tradefile:
        reader = csv.DictReader(tradefile)
        for row in reader:
            town_name = row['town']
            good = row['good']
            sell_price = int(row['sell']) if row['sell'] != "???" else None
            buy_price = int(row['buy']) if row['buy'] != "???" else None
            quantity = int(row['qty']) if row['qty'] != "???" else None

            # Create a nested dictionary for each town and goods
            if town_name not in trade_data:
                trade_data[town_name] = {}
            trade_data[town_name][good] = {
                'Sell Price': sell_price,
                'Buy Price': buy_price,
                'Quantity': quantity
            }

    # Generate the list of town names
    town_names = list(trade_data.keys())

    return trade_data, town_names

def main_menu():
    """
    Prompts the user to select an option:
    1. Find the best trade
    2. Select origin and destination ports
    3. Refresh CSV data
    4. Exit

    Returns:
        int: The user's selected option (1, 2, 3, or 4).
    """
    while True:
        try:
            choice = int(input("Select an option:\n1. Find the best trade\n2. Select origin and destination ports\n3. Refresh CSV data\n4. Exit\n"))
            if choice in (1, 2, 3, 4):
                return choice
            else:
                print("Invalid choice. Please enter a valid option (1, 2, 3, or 4).")
        except ValueError:
            print("Invalid input. Please enter a valid option (1, 2, 3, or 4).")

def prompt_user_for_towns(town_names):
    """
    Prompts the user to select departure and destination towns.

    Args:
        town_names (list): A list of towns (strings).

    Returns:
        tuple: A tuple containing (from_town, to_town).
    """
    while True:
        # User input: Select departure town
        print("Available towns:")
        for i, town in enumerate(town_names, 1):
            print(f"{i}. {town}")

        try:
            from_choice = int(input("Enter the number corresponding to your port of origin: "))
            from_town = town_names[from_choice - 1]  # Adjust for 0-based indexing
        except (ValueError, IndexError):
            print("Invalid choice. Please select a valid departure town.")
            continue  # Ask the user to try again

        # User input: Select destination port
        print("\nAvailable destination ports:")
        for i, town in enumerate(town_names, 1):
            if town != from_town:
                print(f"{i}. {town}")

        try:
            to_choice = int(input("Enter the number corresponding to your destination port: "))
            to_town = town_names[to_choice - 1]  # Adjust for 0-based indexing
        except (ValueError, IndexError):
            print("Invalid choice. Please select a valid destination port.")
            continue  # Ask the user to try again

        print(f"\nDeparture town: {from_town}")
        print(f"Arrival town: {to_town}")

        return from_town, to_town

def calculate_profit_loss(from_town, to_town, trade_data, goods_weights):
    """
    Calculates the profit and loss based on the from_town, to_town, trade data information, and adjusts for the weight of each good.

    Args:
        from_town (str): The name of the departure town.
        to_town (str): The name of the destination town.
        trade_data (dict): The dictionary containing all of the trade data.
        goods_weights (dict): The dictionary containing the weight of each good.
    """
    # Calculate profit/loss and profit/loss per weight for each good
    profit_loss_data = []  # List to store (good, profit_loss, profit_loss_per_weight) tuples

    for good, data in trade_data.get(from_town, {}).items():
        buy_price = data.get('Buy Price', None)
        sell_price = trade_data.get(to_town, {}).get(good, {}).get('Sell Price', None)
        weight = goods_weights.get(good, None)

        if buy_price is not None and sell_price is not None and weight is not None:
            profit_loss = sell_price - buy_price
            profit_loss_per_weight = profit_loss / weight
            profit_loss_data.append((good, profit_loss, profit_loss_per_weight))

    # Sort goods by profit_loss_per_weight (highest to lowest)
    sorted_goods = sorted(profit_loss_data, key=lambda x: x[2], reverse=True)

    # Print sorted goods along with profit/loss per weight unit
    for good, profit_loss, profit_loss_per_weight in sorted_goods:
        print(f"Good: {good}")
        print(f"Profit/Loss: {profit_loss}")
        print(f"Profit/Loss per Weight: {profit_loss_per_weight:.2f}")
        print("-" * 30)

def find_best_trade(trade_data, town_names, goods_weights):
    """
    Finds the single best trade based on profit/loss to weight ratio from a selected departure town.

    Args:
        trade_data (dict): A dictionary containing trade data.
        town_names (list): A list of town names.
        goods_weights (dict): A dictionary containing the weights of goods.

    Returns:
        tuple: A tuple containing (to_town, best_good, profit_per_item, profit_per_weight).
    """
    while True:
        try:
            # User input: Select departure town
            print("Available towns:")
            for i, town in enumerate(town_names, 1):
                print(f"{i}. {town}")
            print(f"{len(town_names) + 1}. Exit")  # Add the exit option

            from_choice = int(input("Enter the number corresponding to your port of origin: "))
            if from_choice == len(town_names) + 1:  # Exit option
                print("Exiting. Returning to the main menu.")
                return None, None, None, None
            
            from_town = town_names[from_choice - 1]  # Adjust for 0-based indexing

            best_profit_per_weight = float('-inf')
            best_good = None
            to_town = None
            profit_per_item = 0

            for town in trade_data:
                if town != from_town:
                    for good, data in trade_data[from_town].items():
                        if good in trade_data[town] and good in goods_weights:
                            buy_price = data.get('Buy Price')
                            sell_price = trade_data[town][good].get('Sell Price')
                            weight = goods_weights[good]

                            # Ensure buy_price, sell_price, and weight are not None and weight is not zero
                            if buy_price is not None and sell_price is not None and weight is not None:
                                profit = sell_price - buy_price
                                profit_per_weight = profit / weight

                                if profit_per_weight > best_profit_per_weight:
                                    best_profit_per_weight = profit_per_weight
                                    best_good = good
                                    to_town = town
                                    profit_per_item = profit

            if best_good is None:
                print(f"No profitable trade found for {from_town}. Please choose another town.")
                continue

            return to_town, best_good, profit_per_item, best_profit_per_weight

        except (ValueError, IndexError):
            print("Invalid choice. Please select a valid departure town.")
            continue

def main():
    """
    Main program entry point
    """
    program_running = True  # Flag to control the outer loop

    while program_running:  # Use the flag as the condition
        try:
            # Prompt user for the trade file path
            csv_file_path = input("Enter the path and filename for the TradePrices CSV file: ")

            # Validate if the file exists and is a CSV file
            if not os.path.isfile(csv_file_path) or not csv_file_path.lower().endswith(".csv"):
                print("Invalid CSV file path. Please provide a valid path to a CSV file.")
                continue

            trade_data, town_names = read_csv_file(csv_file_path)
            town_names.sort()  # Sort the town names alphabetically
            # unique_goods_list = extract_unique_goods(trade_data) # Not needed as list of goods is currently hardcoded
            weights = goods_weights()

            while True:
                user_choice = main_menu()
                
                if user_choice == 1:
                    # Call the function to find the best trade
                    town, best_good, profit_per_item, profit_per_weight = find_best_trade(trade_data, town_names, weights)
                    if town is not None:
                        print(f"The best trade route (for profit to weight) is to {town} with {best_good}.")
                        print(f"The profit per item is: {profit_per_item}.")
                        print(f"The profit per weight is: {profit_per_weight}.")
                elif user_choice == 2:
                    # Call the functions to compare prices between two towns
                    from_town, to_town = prompt_user_for_towns(town_names)
                    calculate_profit_loss(from_town, to_town, trade_data, weights)
                elif user_choice == 3:
                    # Refresh trade data
                    trade_data, town_names = read_csv_file(csv_file_path)
                    town_names.sort()  # Sort the town names alphabetically
                    print("Trade data refreshed.")
                elif user_choice == 4:
                    print("Exiting. Goodbye!")
                    program_running = False  # Set the flag to false to exit the outer loop
                    break


        except KeyboardInterrupt:
            print("\nExiting due to user interruption. Goodbye!")
            program_running = False  # Ensure the program doesn't continue running after a keyboard interrupt
        except Exception as e:
            print(f"An error occurred: {e}")
            continue

## Not needed as list of goods is currently hardcoded in goods_weights()
##def extract_unique_goods(trade_data):
##    """
##    Create a list of unique goods names, ensuring names are accurate and there are no duplicates
##
##    Args:
##        trade_data (dict): A dictionary containing all the trade data, towns, good, sell, buy and quantity values
##
##    Returns:
##        unique_goods_list (list): A list containing the unique goods names
##    """
##    unique_goods = set()
##
##    # Iterate through the dictionary and extract the unique goods names
##    for town in trade_data:
##        for good in trade_data[town]:
##            unique_goods.add(good)
##    
##    unique_goods_list = list(unique_goods)
##    
##    return unique_goods_list

def goods_weights():
    """
    Create a list of goods and weights - the weights are currently hardcoded and so can be updated within this function

    Returns:
        goods_weights (dict): A dictionary containing a list of goods names and their associated weight
    """

    goods_weights = {
        "Cannonballs": 4,
        "Grapes": 2,
        "Chainshot": 4,
        "Hot Shot": 2,
        "Gunpowder": 6,
        "Food": 4,
        "Rum": 6,
        "Weapon": 3,
        "Medicine": 2,
        "Sailcloth": 4,
        "Planks": 5,
        "Linen": 4,
        "Silk": 4,
        "Clothes": 4,
        "Cotton": 3,
        "Wool": 3,
        "Hemp": 5,
        "Tea": 5,
        "Coffee": 5,
        "Cacao": 5,
        "Tabacco": 5,
        "Sugar": 5,
        "Wheat": 6,
        "Flax": 5,
        "Millet": 5,
        "Fish": 8,
        "Vegetables": 6,
        "Fruits": 7,
        "Cinnamon": 4,
        "Copra": 6,
        "Paprika": 4,
        "Ginger": 5,
        "Nutmeg": 5,
        "Peppercorn": 5,
        "Chilli": 5,
        "Basil": 5,
        "Almonds": 6,
        "Wine": 8,
        "Ale": 8,
        "Gin": 8,
        "Brandy": 8,
        "Molases": 5,
        "Paper": 6,
        "Leather": 5,
        "Salt": 5,
        "Oil": 7,
        "Vinegar": 7,
        "Pitch": 6,
        "Soap": 5,
        "Brick": 6,
        "Pottery": 6,
        "Dyes": 6,
        "Tools": 5,
        "Ivory": 9,
        "Timbers": 9,
        "Ebony": 10,
        "Mahogany": 9,
        "Sandalwood": 9,
        "Livestock": 10,
        "Slaves": 5,
        "Gold": 9,
        "Silver": 8,
        "Copper": 8,
        "Iron": 12,
    }
    
    return goods_weights


if __name__ == "__main__":
    main()
