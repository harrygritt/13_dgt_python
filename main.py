# Import Modules
import requests
import os
import sys
import time
import random
import html


# Arrays
players = []
difficulty_options = ["Any Difficulty", "Easy", "Medium", "Hard"]


# API links

category_url = "https://opentdb.com/api_category.php"


# Variables
category_options = requests.get(category_url).json()
category_options = category_options.get("trivia_categories")
PRINTING_WIDTH = 50
DIVIDER_CHARACTER = "="
INVALID_MENU_ENTRY = "Please select a valid option by entering a valid number"

# Classes
class Player:
        correct = 0
        incorrect = 0
        
        def __init__(self, name):
            self.name = name


# Clearing screen function
def clear():
    # Clearing screen dependin on os
    if os.name == "posix":
        os.system('clear')
    else:
        os.system("cls")


# Format single level list function
def print_array(items: list):

    # Print the divider
    print(PRINTING_WIDTH * DIVIDER_CHARACTER)

    # Print the items in array as well as their index
    for index in range(len(items)):
        print(html.unescape(f"[{index + 1}] {items[index]}"))

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

    start_options = ["Start Game", "Players", "Category", "Difficulty", "Exit"]
    
    # Reset difficulty and category options
    difficulty = 0
    category = 0

    while True:
        
        start_index = menu("Main Menu", start_options)
        match start_index:
            case 1:
                question_asking(difficulty, category)

            case 2:
                player_menu()

            case 3:
                category = menu("Categories", [category.get('name') for category in category_options])

            case 4:
                difficulty = menu("Difficulties", difficulty_options)

            case 5:
                sys.exit()

            case _:
                print(INVALID_MENU_ENTRY)


def question_asking(difficulty, category):

    # Ask the  user for number of questions and store in api url
    api_amount = input_checking("How many questions would you like?: ", range(1, 50))

    # Formatting api url as a string
    api_url = f"https://opentdb.com/api.php?amount={api_amount}&type=multiple"

    # Check if a category has been chosen
    if category != 0:
        api_category = category + 8
        api_url += f"&category={api_category}"

    # Check if a difficulty has been chosen
    if difficulty != 0:
        api_difficulty = difficulty_options[difficulty - 1].lower()
        api_url += f"&difficulty={api_difficulty}" 

    # Get availible questions from api
    response = requests.get(api_url).json()
    results = response.get('results')

    # Ask questions
    for question in results:

        # Get incorrect and correct answers in array
        question_options = question.get('incorrect_answers')
        question_options.append(question.get('correct_answer'))

        # Randomise order of answers
        random.shuffle(question_options)
        answer = menu(html.unescape(question.get('question')), question_options)

        # Check if answer is correct or not
        if question_options[answer - 1] == question.get('correct_answer'):
            print("Corect. Top stuff geezer :)")

        else:
            print("Incorrect. That is sucky bum bum :(")
        input()


def player_menu():
    while True:

        menu_options = [player.name for player in players]
        menu_options.append("Add New Player")
        menu_options.append("Back")

        chosen_option = menu("Players", menu_options)
        
        # If user selects "Back" 
        if chosen_option == len(menu_options):
            break
            
        # If user has not selected "Add New Player"
        elif chosen_option != len(menu_options) - 1:
            user = players[chosen_option - 1]
            total = user.correct + user.incorrect
            print(f"Name: {user.name}, Correct: {user.correct}/{total}, Incorrect: {user.incorrect}/{total}")
            input("Press Enter to continue")
            continue
        
        # Check if there are too many users
        if len(players) >= 10:
            print("Maximum number of users reached")
            time.sleep(1)
            continue

        player_name = input("What is the new users name?: ")
        user_info = Player(player_name)
        players.append(user_info)



def menu(menu_title , array: list):

    clear()

    # Center the menu title
    print(DIVIDER_CHARACTER * PRINTING_WIDTH)
    title_len = int((PRINTING_WIDTH - len(menu_title))/2)
    print(" " * title_len, menu_title, " " * title_len)

    # Print category options
    print_array(array) 

    # Ask user to select category
    return input_checking("Please select an option:", array)



if __name__ == "__main__":
    start_menu()