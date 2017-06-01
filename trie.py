
class TrieNode(object):
    
    def __init__(self, c):
        self.map = {}
        self.character = c
        self.isLast = False

class Trie(object):

    def __init__(self):
        self.root = TrieNode('')

    def insert(self, word):
        curr = self.root
        for c in word:
            if c not in curr.map:
                curr.map[c] = TrieNode(c)
            curr = curr.map[c]
        curr.isLast = True

    def search(self, word):
        curr = self.root
        for c in word:
            if c not in curr.map:
                return False
            curr = curr.map[c]
        return curr.isLast

    def startsWith(self, prefix):
        curr = self.root
        for c in prefix:
            if c not in curr.map:
                return False
            curr = curr.map[c]
        return True

if __name__ == '__main__':
    t = Trie()
    t.insert('somestring')
    print t.search('some')
    print t.startsWith('some')
