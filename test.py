#!/usr/bin/python3
# coding: utf-8

from huffman import Huffman

if __name__ == "__main__":
    huffman = Huffman()
    huffman.compress_file("/home/shellcode/Downloads/test.c", "/tmp/huffman_encoded")
