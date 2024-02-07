# Import Modules
import requests

# Arrays
array_difficulty = ["Easy","Medium","Hard","Any Difficulty"]

api_url = "https://opentdb.com/api.php?amount=10&category=21&difficulty=easy"
category_url = "https://opentdb.com/api_category.php"


category_options = requests.get(category_url).json()
category_options = category_options.get("trivia_categories")


for category in category_options:
    print(f"[{category.get('id') - 8}] {category.get('name')}")

