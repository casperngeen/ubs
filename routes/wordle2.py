import json
import logging
import random
import string
import csv
import os

from collections import defaultdict
from flask import request

from routes import app

logger = logging.getLogger(__name__)


base_dir = os.path.abspath(os.path.dirname(__file__))
txt_path = os.path.join(base_dir, 'valid_words.txt')

# Load the word list
def load_words():
    words = []
    with open(txt_path, 'r', encoding='utf-8') as txtfile:
        for row_number, line in enumerate(txtfile, start=1):
            word = line.strip().lower()  # Strip whitespace and convert to lowercase
            if len(word) == 5 and word.isalpha():
                words.append(word)
            else:
                logger.warning(f"Row {row_number} skipped: Invalid word '{word}'.")
    return words


def select_next_guess(possible_words):
    if not possible_words:
        return "crane"
    
    letter_frequency = defaultdict(int)
    for word in possible_words:
        for letter in set(word):
            letter_frequency[letter] += 1
    
    scored_words = [
        (word, sum(letter_frequency[letter] for letter in set(word)))
        for word in possible_words
    ]
    
    best_word = max(scored_words, key=lambda x: x[1])[0]
    best_word = random.choice(possible_words) # test
    return best_word


# def select_next_guess(possible_words):
#     if not possible_words:
#         return "crane"
    
#     letter_frequency = defaultdict(int)
#     for word in possible_words:
#         for letter in set(word):
#             letter_frequency[letter] += 1
    
#     scored_words = [
#         (word, sum(letter_frequency[letter] for letter in set(word)))
#         for word in possible_words
#     ]
    
#     best_word = max(scored_words, key=lambda x: x[1])[0]
#     return best_word

def filter_by_X(possible_words, char, index):
    return [word for word in possible_words if word[index] != char]

def filter_by_dash(possible_words, char):
    return [word for word in possible_words if char not in word.lower()]

def filter_by_O(possible_words, char, index):
    return [word for word in possible_words if word[index] == char]

@app.route('/wordle-game', methods=['POST'])
def evaluate_wordle2():
    data = request.get_json()
    logger.info("Data sent for evaluation: {}".format(data))
    guessHistory: list[str] = data.get('guessHistory', [])
    evaluationHistory: list[str] = data.get('evaluationHistory', [])

    # First guess (Edge case)
    if len(guessHistory) == 0:
        return json.dumps({"guess": "slate"})
    
    possible_words = load_words()

    for i in range(len(guessHistory)):
        for j in range(5):
            if evaluationHistory[i][j] == 'X':
                possible_words = filter_by_X(possible_words, guessHistory[i][j], j)
            elif evaluationHistory[i][j] == '-':
                possible_words = filter_by_dash(possible_words, guessHistory[i][j])
            elif evaluationHistory[i][j] == 'O':
                possible_words = filter_by_O(possible_words, guessHistory[i][j], j)

    guess = select_next_guess(possible_words)
    return json.dumps({"guess": guess})