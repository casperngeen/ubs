import logging

from flask import request, jsonify

from routes import app

logger = logging.getLogger(__name__)

@app.route('/the-clumsy-programmer', methods=['POST'])
def evaluate_clumsy():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    
    results = []

    for test_case in data:
        dictionary = test_case["dictionary"]
        mistypes = test_case["mistypes"]

        trie = Trie()
        for word in dictionary:
            trie.build_trie(word)
        
        corrections = []
        for word in mistypes:
            corrections.append(trie.find_with_mismatch(word))

        results.append({"corrections": corrections})

    return jsonify(results)


if __name__ == '__main__':
    app.run(debug=True)    

class TrieNode:
    def __init__(self):
        self.children = {}          # Dictionary to hold child nodes
        self.is_end_of_word = False # Flag to mark the end of a word

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for char in word:
            # If the character is not already a child of the current node,
            # add a new TrieNode as a child of the current node
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]  # Move to the child node
        node.is_end_of_word = True  # Mark the end of the word

    def build_trie(self, words):
        for word in words:
            self.insert(word)


    def find_with_mismatch(self, word, max_mismatches=1):
        """
        Searches for a word in the trie allowing for a specified number of mismatches.

        Args:
            word (str): The word to search for.
            max_mismatches (int): The maximum number of allowed mismatches.

        Returns:
            bool: True if a word matching the criteria exists in the trie, False otherwise.
        """
        def dfs(node, index, mismatches):
            if mismatches > max_mismatches:
                return False  # Exceeded the allowed mismatches

            if index == len(word):
                # Check if we're at the end of a word in the trie
                return node.is_end_of_word

            char = word[index]
            found = False

            for child_char, child_node in node.children.items():
                if char == child_char:
                    # Character matches; proceed without incrementing mismatches
                    found = found or dfs(child_node, index + 1, mismatches)
                else:
                    # Character does not match; increment mismatches
                    found = found or dfs(child_node, index + 1, mismatches + 1)

            return found

        return dfs(self.root, 0, 0)

    def display(self, node=None, word=''):
        if node is None:
            node = self.root
        if node.is_end_of_word:
            print(word)
        for char, child_node in node.children.items():
            self.display(child_node, word + char)

                
