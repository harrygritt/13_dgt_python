# Import Modules
import requests
import os

# Arrays
array_difficulty = ["Easy","Medium","Hard","Any Difficulty"]

# API links
api_url = "https://opentdb.com/api.php?amount=10&category=21&difficulty=easy"
category_url = "https://opentdb.com/api_category.php"

# Variables
category_options = requests.get(category_url).json()
category_options = category_options.get("trivia_categories")
PRINTING_WIDTH = 50
DIVIDER_CHARACTER = "="
INVALID_MENU_ENTRY = "Please select a valid option (select number)"


def category_menu():
    # Print category options
    print_array([category.get('name') for category in category_options])
    # Ask user to select category
    


# Printing divider function
def divider():
    # Printing divider
    print(PRINTING_WIDTH * DIVIDER_CHARACTER)


# Clearing screen function
def clear():
    # Clearing screen
    os.system("cls")


# Format single level list function
def print_array(items: list):
    # Print the divider
    print(PRINTING_WIDTH * DIVIDER_CHARACTER)

    # For every index for the item in the list
    for index in range(len(items)):
        # Print index and item
        print(f"[{index + 1}] {items[index]}")

    print(PRINTING_WIDTH * DIVIDER_CHARACTER)


# Error checking function
def input_checking(prompt: str, array: list, start_index: int = 1, error_message=INVALID_MENU_ENTRY):
    # Loop while input is invalid
    while True:
        try:
            input_index = int(input(prompt))
        except ValueError:
            print(INVALID_MENU_ENTRY, "by entering a valid number")
            continue

        # Check if option is in chosen list/menu, if not, display error message and loop
        if input_index not in range(start_index, len(array) + 1):
            print(error_message)
        else:
            return input_index



category_menu()