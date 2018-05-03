# coding: utf-8


class LZW(object):
    """ Implementation of the LZW algorithm.

    Attributes
    ----------
    bytes_dict : dict
        Association between repeated bytes sequences and integers.

    Examples
    --------
    An array of bytes like ['\x41', '\x42', '\x43', '\x0A', '\x00'] can be represented by an integer like 256.
    It means that one integer is able to represent multiple bytes at once.

    Notes
    -----
    On the internet we usually find this algorithm using integers that are coded on 12bits. But I think it's a waste of
    space and it can be optimized by sending along the encoded content, the size of the integers. So instead of sending
    12 bits integers, we will be able to send smaller (and bigger) integers. The size of the integers will be determined
    based on the biggest integer in the dictionary. This integer will be on 5 bits, it means other integers can be coded
    on 2^5 = 32 bits max. Which means the biggest supported dictionary is 2^32 = 4294967296 long. Which is more than
    enough.
    """
    def __init__(self):
        self.bytes_dict = None
        self.max_size_integer_size = 5  # The integers size is encoded on 5 bits by default
        self.integers_size_bits = 0  # Max value must be 2**max_size_integer_size (= 32 by default)

    def __build_bytes_dictionary(self, decompression=False):
        if decompression:
            self.bytes_dict = {byte: bytes([byte]) for byte in range(256)}
        else:
            self.bytes_dict = {bytes([byte]): byte for byte in range(256)}

    def __compress(self, bytes_list):

        self.__build_bytes_dictionary()

        biggest_integer = 0
        compressed = []
        pattern = bytes([])

        for byte in bytes_list:
            byte_as_array = bytes([byte])
            current = pattern + byte_as_array

            # if current in self.bytes_dict:  # Too heavy with big dictionaries
            if self.bytes_dict.get(current) is not None:
                pattern = current
            else:
                self.bytes_dict[current] = len(self.bytes_dict)
                compressed.append(self.bytes_dict[pattern])

                if biggest_integer < self.bytes_dict[pattern]:
                    biggest_integer = self.bytes_dict[pattern]

                pattern = byte_as_array

        if pattern:
            compressed.append(self.bytes_dict[pattern])

            if biggest_integer < self.bytes_dict[pattern]:
                biggest_integer = self.bytes_dict[pattern]

        if biggest_integer > 2**(2**self.max_size_integer_size):
            # Shouldn't happen
            raise ValueError("Can't encode such value... Maybe you should increase the size of max_size_integer_size.")

        self.integers_size_bits = biggest_integer.bit_length()
        print("The biggest integer is {} so integers will be coded on {} bits.".format(biggest_integer,
                                                                                       self.integers_size_bits))

        return compressed

    def compress_file(self, input_filename, output_filename):
        with open(input_filename, "rb") as input_file:
            bytes_list = input_file.read()

        print("Input size : {} bytes.".format(len(bytes_list)))
        compressed = self.__compress(bytes_list)

        big_int_compressed = 0

        # TODO : bitwise operation is too heavy on such numbers, find another way. (1 bit of padding can be the solution...)

        print("Assembling integers together...")
        for integer in compressed:
            big_int_compressed <<= self.integers_size_bits
            big_int_compressed += integer

        to_store_in_file = big_int_compressed << self.max_size_integer_size
        to_store_in_file += self.integers_size_bits
        print("Done.")

        to_store_in_file = to_store_in_file.to_bytes((to_store_in_file.bit_length() + 7) // 8, 'big')

        total_file_size = len(to_store_in_file)

        print("Output : {} bytes".format(total_file_size))

        if len(bytes_list) <= total_file_size:
            raise Exception("Aborted. No gain, you shouldn't compress that file. (+{} bytes)".format(
                total_file_size - len(bytes_list)))

        print("Compression gain : {0:.2f}%".format(100 - total_file_size * 100 / len(bytes_list)))

        with open(output_filename, "wb") as output_file:
            output_file.write(to_store_in_file)

    def __decompress(self, bytes_list):
        self.__build_bytes_dictionary(decompression=True)

        return None

    def decompress_file(self, input_filename, output_filanem):
        with open(input_filename, "rb") as input_file:
            bytes_list = input_file.read()

        big_int_compressed = int.from_bytes(bytes_list, 'big')
        self.integers_size_bits = big_int_compressed & 0b11111
        big_int_compressed >>= self.integers_size_bits

        print("Integers are {} bits long.".format(self.integers_size_bits))

        # TODO : gather integers one by one and create an integers list

        self.__decompress(bytes_list)
