# Import Modules
import threading
import winsound
import requests
import os
import sys
import time
import random
import math
import html
import json
from ctypes import WinDLL

# Arrays
players = []
difficulty_options = ["Any Difficulty", "Easy", "Medium", "Hard"]

correct_sounds = [
    ["Amazing.wav", 1],
    ["Brilliant.wav", 1],
    ["Monsterful.wav", 1],
    ["Spot On.wav", 1],
    ["Top Stuff Geezer.wav", 0.3],
    ["Ding Ding Ding.wav", 1],
]

incorrect_sounds = [
    ["Better Luck Next Time Buddy.wav", 1],
    ["Err Err.wav", 1],
    ["Sucky Bum Bum.wav", 0.3],
    ["Uh Uh UH.wav", 1],
    ["You Suck.wav", 1],
]

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

# Fetch the categoriess from the apis
category_options = requests.get(category_url).json()
category_options = category_options.get("trivia_categories")


# Class for the players
class Player:
    # Storing player's score
    correct = 0
    incorrect = 0
    total = 0

    # Initialising the class by setting the name
    def __init__(self, name):
        self.name = name

    # Calculate the player's score
    def calculate_total(self):
        self.total = self.correct + self.incorrect


def pick_sound(sounds):
    while True:

        # Get a random number between 0 and 1 for the cutoff
        cutoff = random.random()

        # Get a random sound
        sound = random.choice(sounds)

        # Check if the sound is picked
        if sound[1] > cutoff:
            return sound[0]


# Clearing screen function
def clear():
    # Clearing screen depending on os
    if os.name == "posix":
        os.system('clear')

    else:
        os.system("cls")


# Format single level list function
def print_array(items: list):
    # Define the horizontal border of the options 
    divider = DIVIDER_CHARACTER_HOZ * PRINTING_WIDTH

    # Display the top horizontal border of the options 
    print("╠" + divider + "╣")

    # Print the items in array as well as their index
    for index in range(len(items)):
        # Escape the html codess
        text = html.unescape(f"[{index + 1}] {items[index]}")

        # Format and display the sides of the menu
        spacing = PRINTING_WIDTH - len(text)
        print(DIVIDER_CHARACTER_VERTICAL + text + " " * spacing + DIVIDER_CHARACTER_VERTICAL)

    # Display the bottom horizontal border of the options 
    print("╚" + divider + "╝")


# Error checking function
def input_checking(prompt: str, array: list, start_index: int = 1, error_message=INVALID_MENU_ENTRY):
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


def play_sound(file):
    initalise_audio_driver()
    winsound.PlaySound("sounds/" + file, winsound.SND_FILENAME | winsound.SND_ASYNC)


# Show start menu
def start_menu():
    play_sound("Intro.wav")

    # Defining options for the start menu
    start_options = ["Start Game", "Players", "Category", "Difficulty", "Exit"]

    # Current difficulty and category options
    difficulty = 0
    category = 0

    # Loop while input is invalid
    while True:

        # Store what option user selects
        start_index = menu("Main Menu", start_options)
        match start_index:
            case 1:
                # Check if there are enough players for the game to start
                if len(players) == 0:
                    print("At least 1 player must be created to start a game")
                    time.sleep(1)
                    continue
                
                # Ask user how many questions they want with limit at 50
                api_amount = input_checking("How many questions would you like? (max is 50): " , range(1, 50))

                # Start downloading of questions based on difficulty and category
                questions = download_questions(difficulty, category, api_amount)

                # Play the intro
                play_sound("Quiz Start.wav")
                print("Starting game..", end="")
                for x in range(4):
                    if x != 3:
                        print(f"\rStarting in {3 - x}", end="")
                    else:
                        print(f"\rQUIZ !              ", end="")
                    time.sleep(0.5)

                # Ask the same questions for each player once at time
                for player in players:
                    question_asking(questions, player)

                # Display players
                player_menu()

            case 2:
                # Display players
                player_menu()

            case 3:
                # Display category menu
                category = menu("Categories", [category.get('name') for category in category_options])

            case 4:
                # Display difficulty menu
                difficulty = menu("Difficulties", difficulty_options)

            case 5:
                # Close program
                sys.exit()

            case _:
                # Display error message
                print(INVALID_MENU_ENTRY)


# Downloading questions from the api
def download_questions(difficulty, category, amount):

    # Add the amount to the url
    api_url = f"https://opentdb.com/api.php?amount={amount}&type=multiple"

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

    # If rate limit reached, pause and re-run
    if  response.get('response_code') == 5:
        print("Download failed, trying again...")
        time.sleep(1)
        return download_questions(difficulty, category, amount)
        

    results = response.get('results')
    for question in results:
        question["correct_answer"] = html.unescape(question.get("correct_answer"))
        question["answers"] = [html.unescape(answers) for answers in question.get('incorrect_answers')]
        question["answers"].append(html.unescape(question.get("correct_answer")))
        # Randomising order of answers displayed
        random.shuffle(question["answers"])

    return results

# Ask user questions
def question_asking(questions, player):
    # Display who should be answering which questions
    begin = menu("The following questions are for: " + player.name, ["Begin", "Skip Player"])
    if begin == 2:
        return

    # Ask questions
    for question in questions:

        # Randomise order of answers
        question_options = question.get('answers')
        answer = menu(html.unescape(question.get('question')), question_options)
        print("Correct Answer:", question.get('correct_answer'))

        # Check if answer is correct or not
        if question_options[answer - 1] == question.get('correct_answer'):
            play_sound(pick_sound(correct_sounds))
            print("Correct. Top stuff geezer :)")

            # Add 1 to number of correct answers per user
            player.correct += 1

        else:
            play_sound(pick_sound(incorrect_sounds))
            print("Incorrect. That is sucky bum bum :(")

            # Add 1 to number of incorrect answers per user
            player.incorrect += 1

        # Pause screen so user can see if they were right or wrong
        input()


# Storing and displaying player information
def player_menu():
    while True:

        # Store player's information in array
        menu_options = [player.name for player in players]
        menu_options.append("Add New Player")
        menu_options.append("Back")

        # Display the menu and store their choice
        chosen_option = menu("Players", menu_options)

        # If user selects the last item (Back) 
        if chosen_option == len(menu_options):
            break

        # If user has not selected "Add New Player", this means they must have chosen a player
        elif chosen_option != len(menu_options) - 1:
            user = players[chosen_option - 1]
            response = menu(user.name, ["Show Score", "Delete This User", "Back"])
            match response:

                # Display player's score
                case 1:
                    user.calculate_total()
                    print(f"Name: {user.name}," +
                          f"Correct: {user.correct}/{user.total}," +
                          f"Incorrect: {user.incorrect}/{user.total}")
                    input("Press Enter to continue")

                case 2:
                    # Remove old player from list of players
                    del players[chosen_option - 1]

            continue

        # If falls through to here then no other option then add new player is slected   

        # Check if there are too many users
        if len(players) >= 10:
            print("Maximum number of users reached")
            time.sleep(1)
            continue

        # Ask for new user's name
        player_name = input("What is the new users name?: ")
        user_info = Player(player_name)
        players.append(user_info)

    # Store users and their info
    users_big_dict = {
        "users": []
    }

    # Store player's scores in the dict as a object
    for player in players:
        player.calculate_total()
        users_big_dict["users"].append(player.__dict__)

    # Overwirte the data in the store file with the updated info
    with open(FILE, "w") as outfile:
        json.dump(users_big_dict, outfile, indent=4)


def menu(menu_title, array: list):
    # Clear the screen
    clear()

    # Center the menu title
    print("╔" + DIVIDER_CHARACTER_HOZ * PRINTING_WIDTH + "╗")

    # To store the lines in the event of the title overflowing
    title_lines = []
    current_line = 0
    title_length = len(menu_title)

    # Break each line that is over the title length
    for item in range(title_length):
        if current_line >= len(title_lines):
            title_lines.append("")

        # Add the current character to the line
        title_lines[current_line] += menu_title[item]

        if (item - (current_line * PRINTING_WIDTH) > PRINTING_WIDTH - 2):
            current_line += 1

    # Formatting menu
    for line in title_lines:
        titlespace = math.floor((PRINTING_WIDTH - len(line)) / 2)
        formatted = f"{DIVIDER_CHARACTER_VERTICAL}{' ' * titlespace}{line}{' ' * titlespace} {DIVIDER_CHARACTER_VERTICAL}"
        # If the line is over the width, cut it off
        if len(formatted) > PRINTING_WIDTH + 2:
            formatted = formatted[:PRINTING_WIDTH + 1] + DIVIDER_CHARACTER_VERTICAL

        # Ensure the vertical border is drawn

        print(formatted)

    # Print category options
    print_array(array)

    # Ask user to select category
    return input_checking("Please select an option: ", array)


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
            # Check if the player has got any wrong
            if new_player.incorrect == None:
                new_player.incorrect = 0
            # Check if the player has got any right
            if new_player.correct == None or new_player.correct == 0:
                new_player.correct = 0
                # Shame the player for being unskilled
                if " has room for improvement" not in new_player.name:
                    new_player.name += " has room for improvement"

            # Remove the mark of shame from the player
            elif new_player.correct != None or new_player.correct != 0:
                if " has room for improvement" in new_player.name:
                    new_player.name = new_player.name.replace(" has room for improvement", "")

            # Put previous players in list of current players
            players.append(new_player)


def initalise_audio_driver():
    return

    # Get a user handle
    user32 = WinDLL("user32")

    # Send volume control events
    for iteration in range(50):
        user32.keybd_event(0xAF, 0, 0, 0)
        user32.keybd_event(0xAF, 0, 2, 0)

# Prevents modulation
if __name__ == "__main__":

    # First audio init
    initalise_audio_driver()

    # Import the scores from previous games
    import_scores()

    # Initiate quiz 
    start_menu()
