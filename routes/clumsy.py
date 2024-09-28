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
        trie.display()
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


    def find_with_mismatch(self, word):

        results = []

        def dfs(node, index, mismatches, path):
            if mismatches > 1:
                return  None # Exceeded the allowed mismatches

            if index == len(word):
                if node.is_end_of_word and mismatches == 1:
                    return path
                return

            char = word[index]

            if char in node.children:
                # Character matches; proceed without incrementing mismatches
                return dfs(node.children[char], index + 1, mismatches, path + char)
                
            else:
                # Character does not match and no matching child node
                for child_char, child_node in node.children.items():
                    # Only consider mismatch when there is no matching character
                    possible = dfs(child_node, index + 1, mismatches + 1, path + child_char)
                    if possible != None:
                        return possible

        dfs(self.root, 0, 0, '')
        return results[0] if results else None


    def display(self, node=None, word=''):
        if node is None:
            node = self.root
        if node.is_end_of_word:
            print(word)
        for char, child_node in node.children.items():
            self.display(child_node, word + char)

                
