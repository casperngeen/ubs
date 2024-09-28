import logging

from flask import request, jsonify

from routes import app

logger = logging.getLogger(__name__)

@app.route('/the-clumsy-programmer', methods=['POST'])
def evaluate_clumsy():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    
    results = [{"corrections": []},{"corrections": []},{"corrections": []},{"corrections": []},{"corrections": []},{"corrections": []}]

    for i in range(6):
        dictionary = data[i]["dictionary"]
        mistypes = data[i]["mistypes"]

        trie = Trie()

        for word in dictionary:
            trie.insert(word)

        corrections = []
        for word in mistypes:
            corrections.append(trie.search_with_mismatch(word))

        results[i] = {"corrections": corrections}

    return jsonify(results)


if __name__ == '__main__':
    app.run(debug=True)    

class TrieNode:
    def __init__(self):
        self.child = [None] * 26         
        self.is_end_of_word = False # Flag to mark the end of a word

class TrieNode:
    def __init__(self):
        # Each node holds a dictionary of its children nodes
        self.children = {}
        # Flag to indicate if the node represents the end of a word
        self.is_end_of_word = False

class Trie:
    def __init__(self):
        """
        Initialize the Trie with a root node.
        The root node doesn't hold any character.
        """
        self.root = TrieNode()

    def insert(self, word):
        """
        Inserts a word into the trie.
        
        :param word: The word to be inserted.
        """
        current = self.root
        for char in word:
            # If the character is not already a child of the current node, add it
            if char not in current.children:
                current.children[char] = TrieNode()
            # Move to the child node
            current = current.children[char]
        # After inserting all characters, mark the end of the word
        current.is_end_of_word = True

    def search(self, word):
        """
        Returns True if the word is in the trie, False otherwise.
        
        :param word: The word to search for.
        :return: Boolean indicating if the word exists in the trie.
        """
        current = self.root
        for char in word:
            if char not in current.children:
                return False
            current = current.children[char]
        return current.is_end_of_word
    
    def search_with_mismatch(self, word, max_mismatch=1):
        """
        Searches for words in the trie that match the given word with up to max_mismatch mismatches.

        :param word: The word to search for.
        :param max_mismatch: The maximum number of allowed mismatched characters.
        :return: A list of matching words.
        """
        results = []

        def _search(node, index, mismatches, path):
            if mismatches > max_mismatch:
                return  # Exceeded the allowed number of mismatches

            if index == len(word):
                if node.is_end_of_word and mismatches <= max_mismatch:
                    results.append("".join(path))
                return

            current_char = word[index]

            for char, child_node in node.children.items():
                path.append(char)
                if char == current_char:
                    _search(child_node, index + 1, mismatches, path)
                else:
                    _search(child_node, index + 1, mismatches + 1, path)
                path.pop()  # Backtrack

        _search(self.root, 0, 0, [])
        return results