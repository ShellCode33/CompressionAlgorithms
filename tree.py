

class Tree(object):

    def __init__(self, init_node=None):
        self.init_node = init_node
        self.left = None
        self.right = None

    def is_leaf(self):
        return self.left is None and self.right is None
