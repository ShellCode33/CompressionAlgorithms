# coding: utf-8


class Node(object):

    def __init__(self, value=None):
        self.value = value
        self.left = None
        self.right = None

    def __str__(self):

        if self.is_leaf():
            return "[{}]".format(self.value)

        return "<{}> ( {} {} )".format(self.value, self.left, self.right)

    # compare nodes between them : node1 < node2
    def __lt__(self, other):
        return self.value < other.value

    def is_leaf(self):
        return self.left is None and self.right is None
