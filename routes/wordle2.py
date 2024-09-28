import json
import logging
import random
import string
import csv

from collections import defaultdict
from flask import request

from routes import app

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
# Configure handler if not already done
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

# Load the word list
VALID_WORDS = []
with open('valid_words.csv', 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row_number, row in enumerate(reader, start=1):
            if len(row) != 5:
                logger.warning(f"Row {row_number} skipped: Expected 5 columns, got {len(row)}.")
                continue  # Skip rows that don't have exactly 5 columns
            # Concatenate letters to form the word
            word = ''.join(letter.strip().lower() for letter in row)
            if len(word) == 5 and word.isalpha():
                VALID_WORDS.append(word)
            else:
                logger.warning(f"Row {row_number} skipped: Invalid word '{word}'.")

def filter_words(valid_words, found, wrong_position, skip):
    possible_words = []
    for word in valid_words:
        valid = True
        for i in range(5):
            if found[i] != '-' and word[i] != found[i]:
                valid = False
                break
            if word[i] in wrong_position[i]:
                valid = False
                break
        if any(letter in word for letter in skip):
            valid = False
        if valid:
            possible_words.append(word)
    return possible_words

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

@app.route('/wordle-game', methods=['POST'])
def evaluate_wordle2():
    data = request.get_json()
    logger.info("Data sent for evaluation: {}".format(data))
    guessHistory: list[str] = data.get('guessHistory', [])
    evaluationHistory: list[str] = data.get('evaluationHistory', [])
    final = ""

    if not guessHistory and not evaluationHistory:
        # Starting guess
        final = "crane"
    else:
        found = ['-' for _ in range(5)]
        wrong_position = [set() for _ in range(5)]
        skip = set()
        letter_counts = defaultdict(int)

        for i in range(len(guessHistory)):
            for j in range(5):
                evaluation = evaluationHistory[i][j]
                if evaluation == '?':
                    continue  # Skip masked positions
                letter = guessHistory[i][j]
                if evaluation == 'O':
                    found[j] = letter
                    letter_counts[letter] += 1
            for j in range(5):
                evaluation = evaluationHistory[i][j]
                if evaluation == '?':
                    continue  # Skip masked positions
                letter = guessHistory[i][j]
                if evaluation == 'X':
                    wrong_position[j].add(letter)
                    letter_counts[letter] += 1
                elif evaluation == '-':
                    if letter not in found and all(letter not in wp for wp in wrong_position):
                        skip.add(letter)

        possible_words = filter_words(VALID_WORDS, found, wrong_position, skip)
        final = select_next_guess(possible_words)

    logger.info("Next guess: {}".format(final))
    return json.dumps({"guess": final})