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
csv_path = os.path.join(base_dir, 'valid_words.csv')

# Load the word list
def load_words():
    words = []
    with open(csv_path, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            for row_number, row in enumerate(reader, start=1):
                if len(row) != 5:
                    logger.warning(f"Row {row_number} skipped: Expected 5 columns, got {len(row)}.")
                    continue  # Skip rows that don't have exactly 5 columns
                word = ''.join(letter.strip().lower() for letter in row)
                if len(word) == 5 and word.isalpha():
                    words.append(word)
                else:
                    logger.warning(f"Row {row_number} skipped: Invalid word '{word}'.")
    return words


def select_next_guess(possible_words):
    if not possible_words:
        # Fallback to a common word if no possibilities are left
        return "crane"
    # Advanced strategy: frequency analysis
    letter_frequency = defaultdict(int)
    for word in possible_words:
        for letter in set(word):
            letter_frequency[letter] += 1
    best_word = max(possible_words, key=lambda w: sum(letter_frequency[c] for c in set(w)))
    return best_word

def filter_by_dash(possible_words, char, index):
    return list(filter(lambda s: s[index] != char, possible_words))

def filter_by_X(possible_words, char):
    return list(filter(lambda s: char in s.lower(), possible_words))

def filter_by_O(possible_words, char, index):
    return list(filter(lambda s: s[index] == char, possible_words))


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
                possible_words = filter_by_X(possible_words, guessHistory[i][j])
            elif evaluationHistory[i][j] == '-':
                possible_words = filter_by_dash(possible_words, guessHistory[i][j], j)
            elif evaluationHistory[i][j] == 'O':
                possible_words = filter_by_O(possible_words, guessHistory[i][j], j)
    
    guess = select_next_guess(possible_words)
    return json.dumps({"guess": guess})