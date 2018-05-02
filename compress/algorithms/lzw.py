# coding: utf-8


class LZW(object):

    def __init__(self):
        self.found_bytes = []

    def __find_bytes(self, bytes_list):

        for byte in bytes_list:
            if byte not in self.found_bytes:
                self.found_bytes.append(byte)

    def __compress(self, bytes_list):

        patterns = []
        pattern = [bytes_list[0]]

        for i in range(1, len(bytes_list)):
            current_byte = [bytes_list[i]]

            if pattern + current_byte in patterns:
                pattern += current_byte
            else:
                print(pattern)
                patterns.append(pattern + current_byte)
                pattern = current_byte

        print(pattern)

    def compress_file(self, input_filename, output_filename):
        with open(input_filename, "rb") as input_file:
            bytes_list = input_file.read()

        bytes_list = b"Hello there ! How you doing ? Personnally I'm doing great ! And what a wonderful weather  by the way !"
        self.__find_bytes(bytes_list)
        self.__compress(bytes_list)

    def decompress_file(self, intput_filename, output_filanem):
        pass
