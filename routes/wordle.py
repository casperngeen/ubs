# import json
# import logging
# import random
# import string

# from collections import defaultdict
# from flask import request

# from routes import app

# logger = logging.getLogger(__name__)


# # @app.route('/wordle-game', methods=['POST'])
# def evaluate_wordle():
#     data = request.get_json()
#     logging.info("data sent for evaluation {}".format(data))
#     guessHistory: list['str'] = data.get('guessHistory')
#     evaluationHistory: list['str'] = data.get('evaluationHistory')
#     final = ""
#     # default guess
#     if not guessHistory and not evaluationHistory:
#         starting = ["slate", "crane", "crate", "trace", "salet", "raise", "roast", "stare"]
#         final = starting[random.randrange(0, len(starting))]

#     else:    
#     # if there are previous guesses
#         found = ['-' for _ in range(5)] 
#         wrong_position = [set() for _ in range(5)] 
#         skip = set()
#         letter_counts = defaultdict(int)
#         my_guess = ['-' for _ in range(5)]

#         for i in range(len(guessHistory)):
#             # First pass, handle 'O' (correct position)
#             for j in range(5):
#                 letter = guessHistory[i][j]
#                 evaluation = evaluationHistory[i][j]

#                 # Correct letter in the correct position
#                 if evaluation == 'O':
#                     found[j] = letter
#                     letter_counts[letter] += 1

#             # Second pass, handle 'X' (wrong position) and '-'
#             for j in range(5):
#                 letter = guessHistory[i][j]
#                 evaluation = evaluationHistory[i][j]

#                 # Correct letter in the wrong position
#                 if evaluation == 'X':
#                     correct_and_misplaced_count = sum(1 for k in range(5) if guessHistory[i][k] == letter and evaluationHistory[i][k] in ['O', 'X'])
#                     # Add to wrong_position but ensure it’s not already in found
#                     if letter_counts[letter] < correct_and_misplaced_count:
#                         wrong_position[j].add(letter)
#                         letter_counts[letter] += 1
                
#                 # Letter not in the word at all
#                 elif evaluation == '-':
#                     # Only add to skip if the letter is not in found and not in wrong positions
#                     if letter not in found and all(letter not in sublist for sublist in wrong_position):
#                         skip.add(letter)

#         guesses = []
#         # fill up the solved positions
#         for letter in letter_counts:
#             for i in range(letter_counts[letter]):
#                 guesses.append(letter)

#         for i in range(5):
#             if found[i] != '-':
#                 my_guess[i] = found[i]
#                 guesses.remove(found[i])

#         indices_to_fill = []
#         for i in range(5):
#             if my_guess[i] == '-':
#                 indices_to_fill.append(i)

#         # fill up the rest of the unsolved positions
#         guess = list(guesses)
#         while len(guess) < len(indices_to_fill):
#             guess.append('-')
#         while in_wrong_place(guess, indices_to_fill, wrong_position):
#             random.shuffle(guess)
#         for i in range(len(guess)):
#             if guess[i] != '-':
#                 my_guess[indices_to_fill[i]] = guess[i]
#             else:
#                 my_guess[indices_to_fill[i]] = get_guess(skip, wrong_position[indices_to_fill[i]])
#         final = ''.join(my_guess)
                
#     logging.info("My guess :{}".format(final))
#     return json.dumps({"guess": final})

# def in_wrong_place(guess, indices_to_fill, wrong_position):
#     for i in range(len(guess)):
#         if guess[i] != '-' and guess[i] in wrong_position[indices_to_fill[i]]:
#                 return True
#     return False

# def get_guess(skip: set, wrong_position: set):
#     lowercase_letters = set(string.ascii_lowercase)
#     for letter in skip:
#         lowercase_letters.remove(letter)
#     for letter in wrong_position:
#         lowercase_letters.remove(letter)
#     return random.sample(lowercase_letters, 1)[0]