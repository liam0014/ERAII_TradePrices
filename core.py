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

def calculate_profit_loss(from_town, to_town, trade_data):
    """
    Calculates the profit and loss based on the from_town, to_town, and trade data information.

    Args:
        from_town (str): The name of the departure town.
        to_town (str): The name of the destination town.
        trade_data (dict): The dictionary containing all of the trade data.
    """
    # Calculate profit/loss for each good
    profit_loss_data = []  # List to store (good, profit_loss) tuples

    for good, data in trade_data.get(from_town, {}).items():
        buy_price = data.get('Buy Price', None)
        sell_price = trade_data.get(to_town, {}).get(good, {}).get('Sell Price', None)

        if buy_price is not None and sell_price is not None:
            profit_loss = sell_price - buy_price
            profit_loss_data.append((good, profit_loss))

    # Sort goods by profit_loss (highest to lowest)
    sorted_goods = sorted(profit_loss_data, key=lambda x: x[1], reverse=True)

    # Print sorted goods
    for good, profit_loss in sorted_goods:
        print(f"Good: {good}")
        print(f"Profit/Loss: {profit_loss}")
        print("-" * 30)

def find_best_trade(trade_data, town_names):
    """
    Prompts the user for their departure town and finds the good with the highest profit.

    Args:
        trade_data (dict): A dictionary containing trade data.
        town_names (list): A list of town names.

    Returns:
        tuple: A tuple containing (to_town, best_good, profit_per_item).
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
                return None, None, None
            
            from_town = town_names[from_choice - 1]  # Adjust for 0-based indexing

            goods = trade_data.get(from_town, {})
            valid_from_goods = [good for good in goods if goods.get(good, {}).get('Buy Price') is not None]

            # Find the destination town with the highest profit for the selected good
            max_profit = float('-inf')
            best_good = None
            to_town = None

            for town in trade_data:
                if town != from_town:
                    for good in valid_from_goods:
                        sell_price = trade_data[town].get(good, {}).get('Sell Price', 0)
                        buy_price = goods.get(good, {}).get('Buy Price', 0)
                        if sell_price is not None:
                            profit = sell_price - buy_price
                            if profit > max_profit:
                                max_profit = sell_price
                                best_good = good
                                to_town = town

            if best_good is None:
                print(f"No profitable trade found for {from_town}. Please choose another town.")
                continue

            profit_per_item = max_profit
            return to_town, best_good, profit_per_item

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

            while True:
                user_choice = main_menu()
                
                if user_choice == 1:
                    # Call the function to find the best trade
                    town, best_good, profit_per_item = find_best_trade(trade_data, town_names)
                    if town is not None:
                        print(f"The best trade route is to {town} with {best_good}. The profit per item is: {profit_per_item}")
                elif user_choice == 2:
                    # Call the functions to compare prices between two towns
                    from_town, to_town = prompt_user_for_towns(town_names)
                    calculate_profit_loss(from_town, to_town, trade_data)
                elif user_choice == 3:
                    # Refresh trade data
                    trade_data, town_names = read_csv_file(csv_file_path)
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

if __name__ == "__main__":
    main()
