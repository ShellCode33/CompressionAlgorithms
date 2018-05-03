#!/usr/bin/python3
# coding: utf-8

from optparse import OptionParser
from compress.algorithms.huffman import Huffman
from compress.algorithms.lzw import LZW
import os

if __name__ == "__main__":

    parser = OptionParser(usage="Usage: %prog [options] file")
    parser.set_defaults(verbose=False, compress=True, algo="lzw")
    parser.add_option("-v", "--verbose", action="store_true", dest="verbose",
                      help="Set verbose mode to understand what's underneath.")

    parser.add_option("-a", "--algo", action="store", dest="algo",
                      help="Set the algorithm you want to use (Huffman or LZW) default is LZW.")

    parser.add_option("-o", "--output", action="store", dest="output",
                      help="Set the output file name, default is the same as input + tor extension.")

    parser.add_option("-d", "--decompress", action="store_false", dest="compress",
                      help="Decompress the file.")

    (options, args) = parser.parse_args()

    if len(args) != 1:
        parser.error("Please specify a file to compress.")

    if os.path.isdir(args[0]):
        parser.error("This program doesn't support directory compressing yet.")

    if options.output is None:
        options.output = args[0] + ".tor"

    algo = None

    if options.algo.lower() == "huffman":
        algo = Huffman()
    elif options.algo.lower() == "lzw":
        algo = LZW()
    else:
        parser.error("Algorithm does not exist or is not supported yet.")

    if options.compress:
        algo.compress_file(args[0], options.output)
    else:
        algo.decompress_file(args[0], options.output)
