# coding: utf-8

import base64
from node import Node
from heapq import *


class Huffman(object):
    """ This class is an implementation of the Huffman compression algorithm.

    Attributes
    ----------
    root_node : Node
        Root node of the tree.

    bytes_occurrences : dict
        Association between a byte and its number occurrences.

    huffman_code : dict
        Association between a byte and its new code.

    Notes
    -----
    The method we have chosen to use here is semi-adaptive because it will build a tree based on actual frequencies
    instead of using static symbols weights.
    (but it will not dynamically change the tree like the real adaptive algorithm
    https://en.wikipedia.org/wiki/Adaptive_Huffman_coding ).
    The problem with this method is that we have to transmit the tree with the encoded content in order to decompress.
    The tree can't be bigger than 256 leaves, which means this method will be good to compress big chunks of data but
    it will be inefficient to compress small ones.
    """

    def __init__(self):
        self.root_node = None
        self.bytes_occurrences = {}
        self.huffman_code = {}

        self.compress_file("/tmp/huffman", "/tmp/huffman_encoded")

    def __find_bytes_occurrences(self, bytes_list):

        # Count bytes
        for byte in bytes_list:
            try:
                self.bytes_occurrences[byte] += 1
            except KeyError:
                self.bytes_occurrences[byte] = 1

    def __build_tree(self):

        heap = []

        for byte in self.bytes_occurrences:
            # In Python, tuples are compared one item after another. If the first values are different,
            # they'll be used to compare tuples, not the other items of the tuples. Which means the order is important.
            heappush(heap, (self.bytes_occurrences[byte], Node(byte)))

        while heap:  # While there are items to pop
            item1 = heappop(heap)  # will always exist

            try:
                item2 = heappop(heap)

                # Create new node from 2 others
                new_node = Node(item1[0] + item2[0])
                new_node.left = item1[1]
                new_node.right = item2[1]

                # Push back the new node on the heap
                heappush(heap, (new_node.value, new_node))

            # If item2 doesn't exist, it means the heap is empty and item1 is the final node
            except IndexError:
                self.root_node = item1[1]

    def __create_huffman_code(self, node, code=""):

        if node.is_leaf():
            self.huffman_code[node.value] = code

        else:
            self.__create_huffman_code(node.left, code + "0")
            self.__create_huffman_code(node.right, code + "1")

    def __compress(self, bytes_list):

        self.__find_bytes_occurrences(bytes_list)
        print("Occurrences: " + str(self.bytes_occurrences))
        self.__build_tree()
        print("Tree: " + str(self.root_node))
        self.__create_huffman_code(self.root_node)
        print("Code: " + str(self.huffman_code))

        encoded_string = "1"  # Padding needed to convert to bytes, otherwise we will lose information (the first zeros)

        for byte in bytes_list:
            encoded_string += self.huffman_code[byte]

        print("Encoded: " + encoded_string)

        # Convert to bytes list
        return int(encoded_string, 2).to_bytes((len(encoded_string)+7) // 8, byteorder='big')

    def compress_file(self, input_filename, output_filename):
        print("Reading {}...".format(input_filename))

        with open(input_filename, "rb") as input_file:
            bytes_list = input_file.read()

        print("Input size : ", len(bytes_list))
        compressed = self.__compress(bytes_list)
        print("Compressed size : ", len(compressed))

        # TODO : Write the tree to the file

        with open(output_filename, "wb") as output_file:
            output_file.write(compressed)

    def decompress_file(self, input_filename, output_filename):
        # int.from_bytes(compressed, byteorder='big')
        pass