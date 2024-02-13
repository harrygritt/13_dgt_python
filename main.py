# Import Modules
import requests
import os
import sys

# Arrays
start_options = ["Information","Players","Category","Difficulty","Exit"]
difficulty = ["Easy","Medium","Hard","Any Difficulty"]


# API links
api_url = "https://opentdb.com/api.php?amount=10&category=21&difficulty=easy"
category_url = "https://opentdb.com/api_category.php"

# Variables
category_options = requests.get(category_url).json()
category_options = category_options.get("trivia_categories")
PRINTING_WIDTH = 50
DIVIDER_CHARACTER = "="
INVALID_MENU_ENTRY = "Please select a valid option by entering a valid number"



# Clearing screen function
def clear():
    # Clearing screen
    os.system("cls")


# Format single level list function
def print_array(items: list):

    # Print the divider
    print(PRINTING_WIDTH * DIVIDER_CHARACTER)

    # Print the items in array as well as their index
    for index in range(len(items)):
        print(f"[{index + 1}] {items[index]}")

    print(PRINTING_WIDTH * DIVIDER_CHARACTER)


# Error checking function
def input_checking(prompt: str, array: list, start_index: int = 1, error_message = INVALID_MENU_ENTRY):

    # Loop while input is invalid
    while True:
        try:
            input_index = int(input(prompt))
        except ValueError:
            print(INVALID_MENU_ENTRY)
            continue
        # Check if option is in chosen list/menu, if not, display error message and loop
        if input_index not in range(start_index, len(array) + 1):
            print(error_message)
        else:
            return input_index


# Show start menu
def start_menu():

    # Clearing screen
    clear()

    print_array(start_options)
    
    start_index = input_checking("Please select option: " , start_options)
    match start_index:
        case 1:
            print("info")

        case 2:
            print("players")

        case 3:
            category_menu()

        case 4:
            difficulty_menu()

        case 5:
            sys.exit()

        case _:
            print(INVALID_MENU_ENTRY)


# Show category options 
def category_menu():

    clear()

    # Print category options
    print_array([category.get('name') for category in category_options])

    # Ask user to select category
    category_index = input_checking("Which category would you like to be tested on?:" , category_options)
    print(category_options[category_index - 1])


def difficulty_menu():

    clear()
    print("Difficulty")
    print_array(difficulty)
    difficulty_index = input_checking("Please select a difficulty:")
    


start_menu()