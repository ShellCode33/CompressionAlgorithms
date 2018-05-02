#!/usr/bin/python3
# coding: utf-8

from compress.algorithms.huffman import Huffman
from compress.algorithms.lzw import LZW

if __name__ == "__main__":

    # TODO : write command line tool

    lzw = LZW()
    lzw.compress_file("/home/shellcode/Downloads/STAR_API_dump.json", "/tmp/huffman_encoded")

    # huffman = Huffman()
    # huffman.compress_file("/tmp/huffman", "/tmp/huffman_encoded")
