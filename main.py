# Import Modules
import requests
import os
import sys
import time
import random
import math
import html
import json


# Arrays
players = []
difficulty_options = ["Any Difficulty", "Easy", "Medium", "Hard"]


# API links
category_url = "https://opentdb.com/api_category.php"


# Variables
category_options = requests.get(category_url).json()
category_options = category_options.get("trivia_categories")
PRINTING_WIDTH = 140
DIVIDER_CHARACTER_HOZ = "═"
DIVIDER_CHARACTER_VERTICAL = "║"
INVALID_MENU_ENTRY = "Please select a valid option by entering a valid number"
FILE = "player_history.json"


# Class
class Player:
        correct = 0
        incorrect = 0
        total = 0

        def __init__(self, name):
            self.name = name
        
        def calculate_total(self):
            self.total = self.correct + self.incorrect


# Clearing screen function
def clear():
    # Clearing screen dependin on os
    if os.name == "posix":
        os.system('clear')
    else:
        os.system("cls")


# Format single level list function
def print_array(items: list):


    divider = DIVIDER_CHARACTER_HOZ * PRINTING_WIDTH

    print("╠" + divider + "╣")

    # Print the items in array as well as their index
    for index in range(len(items)):
            text = html.unescape(f"[{index + 1}] {items[index]}")
            spacing = PRINTING_WIDTH - len(text)
            print(DIVIDER_CHARACTER_VERTICAL + text + " " * spacing + DIVIDER_CHARACTER_VERTICAL)

    print("╚" + divider + "╝")


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
                if len(players) == 0:
                    print("At least 1 player must be created to start a game")
                    time.sleep(1)
                    continue

                questions = download_questions(difficulty, category)
                for player in players:
                    question_asking(questions, player)

                player_menu()


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


def question_asking(questions, player):

    # Ask questions
    for question in questions:

        # Randomise order of answers
        question_options = question.get('answers')
        answer = menu(html.unescape(question.get('question')), question_options)

        # Check if answer is correct or not
        if question_options[answer - 1] == question.get('correct_answer'):
            print("Correct. Top stuff geezer :)")
            # Add 1 to number of correct answers per user
            player.correct += 1

        else:
            print("Incorrect. That is sucky bum bum :(")
            # Add 1 to number of incorrect answers per user
            player.incorrect += 1

        # Pause screen so user can see if they were right or wrong
        input()


def download_questions(difficulty, category):

    # Ask the  user for number of questions and store in api url
    api_amount = input_checking("How many questions would you like? (max is 50): ", range(1, 50))

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
    for question in results:
        question["answers"] = [html.unescape(answers) for answers in question.get('incorrect_answers')]
        question["answers"].append(html.unescape(question.get("correct_answer")))
        random.shuffle(question["answers"])

    return results


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
            response = menu(user.name, ["Show Score", "Delete This User", "Back"])
            match response:
                # Display player's score
                case 1:
                    user.calculate_total()
                    print(f"Name: {user.name}, Correct: {user.correct}/{user.total}, Incorrect: {user.incorrect}/{user.total}")
                    input("Press Enter to continue")
                
                case 2:
                    # Remove old player from list of players
                    del players[chosen_option - 1]

            continue
        
        # Check if there are too many users
        if len(players) >= 10:
            print("Maximum number of users reached")
            time.sleep(1)
            continue
        
        # Ask for new user's name
        player_name = input("What is the new users name?: ")
        user_info = Player(player_name)
        players.append(user_info)


    users_big_dict = {
        "users" : []
    }
    

    for player in players:
        player.calculate_total()
        users_big_dict["users"].append(player.__dict__)

    
    with open(FILE, "w") as outfile:
        json.dump(users_big_dict, outfile, indent = 4)
    


def menu(menu_title , array: list):
    clear()

    # Center the menu title
    print("╔" + DIVIDER_CHARACTER_HOZ * PRINTING_WIDTH + "╗")

    title_lines = []
    current_line = 0
    title_length = len(menu_title)
    for i in range(title_length):
        # Check if there is an item
        if current_line >= len(title_lines):
            title_lines.append("")

        # Add the current character to the line
        title_lines[current_line] += menu_title[i]

        if (i - (current_line * PRINTING_WIDTH) > PRINTING_WIDTH - 2):
            current_line += 1

    for line in title_lines:
        titlespace = math.floor((PRINTING_WIDTH - len(line)) / 2)
        print(f"{DIVIDER_CHARACTER_VERTICAL}{' ' * titlespace}{line}{' ' * titlespace} {DIVIDER_CHARACTER_VERTICAL}")

    # Print category options
    print_array(array)

    # Ask user to select category
    return input_checking("Please select an option:", array)


# Import the scores from previous games
def import_scores():

    # Opening JSON file
    with open(FILE, "r") as openfile:
    
        # Reading from json file
        json_object = json.load(openfile)

        # Get user's information from previous games
        users = json_object["users"]
        for user in users:
            new_player = Player(user.get("name"))
            new_player.correct = user.get("correct")
            new_player.incorrect = user.get("incorrect")
            # Check if the user has got any wrong
            if new_player.incorrect == None:
                new_player.incorrect = 0
            # Check if the user has got any right
            if new_player.correct == None or new_player.correct == 0:
                new_player.correct = 0
                # Shame the user for being unskilled
                if " has room for improvement" not in new_player.name:
                    new_player.name += " has room for improvement"
            
            # Put previous players in list of current players
            players.append(new_player)
            

if __name__ == "__main__":  
    import_scores()
    start_menu()