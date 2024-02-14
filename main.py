# Import Modules
import requests
import os
import sys
import time


# Arrays
start_options = ["Information","Players","Category","Difficulty","Exit"]
difficulty_options = ["Easy","Medium","Hard","Any Difficulty"]


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

    # Reset difficulty and category options
    difficulty = 0
    category = 0

    while True:
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
                category = menu("Categories" , [category.get('name') for category in category_options])

            case 4:
                difficulty = menu("Difficulties" , difficulty_options)

            case 5:
                sys.exit()

            case _:
                print(INVALID_MENU_ENTRY)


def menu(menu_title , array: list):

    clear()

    # Print menu title
    print(menu_title)

    # Print category options
    print_array(array)

    # Ask user to select category
    index = input_checking("Please select an option:" , array)
    print(f"You have selected: {array[index - 1]}")

    # Let user see their selection
    time.sleep(2)

    # Return choice
    return index


start_menu()