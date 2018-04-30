import base64
from tree import Tree
from heapq import *

class Huffman():

    def __init__(self):
        self.characters_frequency = {}
        self.tree = None

    def __find_bytes_frequences(self, bytes_list):

        # Count bytes
        for byte in bytes_list:
            try:
                self.characters_frequency[byte] += 1
            except KeyError:
                self.characters_frequency[byte] = 1

        # Convert to frequencies
        for item in self.characters_frequency:
            self.characters_frequency[item] /= len(bytes_list)

    def __build_tree(self, bytes_list):
        heap = heapify(bytes_list)


    def compress(self, bytes_list):
        self.__find_bytes_frequences(bytes_list)
        self.__build_tree(bytes_list)

    def decompress(self, base64_string):
        decoded_bytes = base64.b64decode(base64_string)
        print(decoded_bytes)
