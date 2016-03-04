"""Prefix tree for searching string."""


class Node:
    """Node in Trie tree."""
    def __init__(self, children=None, value=None):
        # `children` is a set of Edge
        self.children = [] if children is None else children
        self.value = value  # a value for leaf node if not None

    def is_leaf(self):
        if self.children:
            return False
        else:
            return True

    def __repr__(self):
        return '<Node: value={}, children={}>'\
            .format(self.value, self.children)


class Edge:
    """Edge represents an edge in Trie."""
    def __init__(self, label=None, node=None):
        # `label` is a string needed append when tranverse to `node`
        self.label = label
        self.node = node

    def __repr__(self):
        return '<Edge: label={}>'.format(self.label)


class Trie(object):
    def __init__(self):
        self.root = Node()

    def find(self, word):
        """Find a word in Trie and return its value.
            Args:
                word: a string for searching
            Return:
                A value associated with word
                or None when not found.
        """
        if self.root.is_leaf():
            # No word in tree
            return None

        pos = 0  # position of word to be find
        curr_node = self.root
        next_node = curr_node

        while not curr_node.is_leaf():
            # decide which edge to go
            for edge in curr_node.children:
                if word[pos:].startswith(edge.label) and\
                        (word[pos:] == '' or
                         word[pos:] != '' and edge.label != ''):
                    next_node = edge.node
                    pos += len(edge.label)
                    break

            if curr_node == next_node:
                # No label matches remain word
                return None

            curr_node = next_node

        if pos == len(word):
            return curr_node.value
        else:
            return None

    def insert(self, word, value):
        """Insert a word with its value.
            Args:
                word: a string.
                value: the object associated with word.
        """
        assert self.root is not None, 'root node is None!!'
        if self.root.is_leaf():
            # Insert to right after root node
            node = Node(value=value)
            edge = Edge(label=word, node=node)
            self.root.children.append(edge)
        else:
            # Insert to another place
            pos = 0  # position of word to be inserted
            curr_node = self.root
            next_node = curr_node

            while not curr_node.is_leaf():
                for edge in curr_node.children:
                    if edge.label == '' and pos != len(word) or\
                            edge.label and edge.label[0] != word[pos]:
                        # Go for next edge
                        continue

                    # `edge` matching
                    for i in range(len(edge.label)):
                        if word[pos+i] != edge.label[i]:
                            # Break the edge with a connecting node
                            # and insert a new node to the connecting node
                            connect_edge = Edge(label=edge.label[i:],
                                                node=edge.node)
                            new_node = Node(value=value)
                            new_edge = Edge(label=word[pos+i:], node=new_node)
                            connect_node = Node(
                                children=[connect_edge, new_edge]
                            )
                            edge.label = edge.label[:i]
                            edge.node = connect_node
                            return  # Insertion succeed

                    # `edge` has matched
                    pos += len(edge.label)
                    next_node = edge.node
                    break
                if curr_node == next_node:
                    # No label matches remain word
                    # Insert to an internal node
                    new_node = Node(value=value)
                    new_edge = Edge(label=word[pos:], node=new_node)
                    curr_node.children.append(new_edge)
                    return
                curr_node = next_node

            if pos != len(word):
                # Insert to an existing prefix word
                new_node = Node(value=value)
                new_edge = Edge(label=word[pos:], node=new_node)
                connect_edge = Edge(label='', node=curr_node)
                connect_node = Node(children=[connect_edge, new_edge])
                edge.node = connect_node
        return

    def delete(self, word):
        if self.root.is_leaf():
            # No word in tree
            return

        pos = 0  # position of word to be find
        edge = None
        prev_edge = None
        prev_node = None
        curr_node = self.root
        next_node = curr_node

        while not curr_node.is_leaf():
            prev_edge = edge
            # decide which edge to go
            for edge in curr_node.children:
                if word[pos:].startswith(edge.label) and\
                        (word[pos:] == '' or
                         word[pos:] != '' and edge.label != ''):
                    next_node = edge.node
                    pos += len(edge.label)
                    break

            if curr_node == next_node:
                # No label matches remain word
                return

            prev_node = curr_node
            curr_node = next_node

        prev_node.children.remove(edge)
        if len(prev_node.children) == 1:
            prev_edge.label += prev_node.children[0].label
            prev_edge.node = prev_node.children[0].node

    def _get_leaves(self, node):
        """Return a generator of all leaves value from subtree of node"""
        if node.is_leaf():
            yield node.value

        for edge in node.children:
                yield from self._get_leaves(edge.node)

    def prefix_recommend(self, prefix):
        """Return a list of recommend word by prefix."""
        if self.root.is_leaf():
            # No word in tree
            return iter(())

        pos = 0
        curr_node = self.root
        next_node = curr_node

        while not curr_node.is_leaf():
            for edge in curr_node.children:
                if edge.label == '' and pos != len(prefix) or\
                        edge.label and edge.label[0] != prefix[pos]:
                    # Go for next edge
                    continue
                """
                if edge.label and edge.label[0] != prefix[pos]:
                    # Go for next edge
                    continue"""

                for i in range(len(edge.label)):
                    if i == len(prefix) - pos:
                        # Return all leaves in subtree of edge.node
                        return self._get_leaves(edge.node)
                        pass

                    if prefix[pos+i] != edge.label[i]:
                        # No word in tree have the prefix
                        return iter(())  # a empty iterable

                # edge matched
                pos += len(edge.label)
                next_node = edge.node

                if pos == len(prefix):
                    # Return the all leaves in subtree of edge.node
                    return self._get_leaves(edge.node)

                break

            if curr_node == next_node:
                # No label matched remain word
                return iter(())
            curr_node = next_node

if __name__ == "__main__":
    import random
    import string
    import time

    trie = Trie()
    trie.insert('abc', "abc's value")
    # test for insert to an edge
    trie.insert('abd', "abd's value")
    # test for duplicate insertion
    trie.insert('abd', "abd's value again")
    # test for insert to internal node
    trie.insert('abf', "abf's value")
    # test for insert to existing prefix word
    trie.insert('abce', "abce's value")

    # test for big number of word
    length = 4
    for i in range(15000):
        word = ''.join(
            random.choice(string.ascii_uppercase)
            for _ in range(length))
        trie.insert(word, word + "'s value'")

    start = time.time()
    trie.insert('DLKJASDKASKD', "DLKJASDKASKD's value")
    end = time.time()
    print('Insert time:', end - start)

    start = time.time()
    print(trie.find('DLKJASDKASKD'))
    end = time.time()
    print('Find time:', end - start)
    print("Find 'a':", trie.find('a'))

    # test for find()
    print(trie.find('abc'))
    print(trie.find('abd'))
    print(trie.find('abf'))
    print(trie.find('abce'))
    print(trie.find('abg'))

    # test for delete
    trie.delete('abc')
    print(trie.find('abc'))

    # test for recommend
    print('Prefix recommend')
    for value in trie.prefix_recommend('a'):
        print(value)

    # test for prefix-recommend 'downtown'
    print("prefix 'downtown'")
    for value in trie.prefix_recommend('downtown'):
        print(value)
