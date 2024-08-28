import heapq
from collections import Counter

class HuffmanNode:
    def __init__(self, char, freq):
        """
        Initialize a HuffmanNode with a character and its frequency.
        """
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        """
        Less-than comparison based on frequency for priority queue.
        """
        return self.freq < other.freq

class HuffmanCompressor:
    def build_tree(self, frequency):
        """
        Build the Huffman tree based on character frequencies.
        
        Args:
            frequency (dict): A dictionary with characters as keys and their frequencies as values.
        
        Returns:
            HuffmanNode: The root node of the Huffman tree.
        """
        # Create a priority queue (min-heap) with initial nodes
        heap = [HuffmanNode(char, freq) for char, freq in frequency.items()]
        heapq.heapify(heap)
        
        # Merge nodes until only one tree remains
        while len(heap) > 1:
            left = heapq.heappop(heap)
            right = heapq.heappop(heap)
            merged = HuffmanNode(None, left.freq + right.freq)
            merged.left = left
            merged.right = right
            heapq.heappush(heap, merged)
        
        return heap[0]

    def build_codes(self, root):
        """
        Generate Huffman codes for each character based on the Huffman tree.
        
        Args:
            root (HuffmanNode): The root node of the Huffman tree.
        
        Returns:
            dict: A dictionary with characters as keys and their Huffman codes as values.
        """
        codes = {}
        
        # Recursive function to generate Huffman codes
        def _generate_codes(node, current_code):
            if node is None:
                return
            if node.char is not None:
                codes[node.char] = current_code
                return
            _generate_codes(node.left, current_code + "0")
            _generate_codes(node.right, current_code + "1")
        
        _generate_codes(root, "")
        return codes

    def compress(self, data):
        """
        Compress the input data using Huffman coding.
        
        Args:
            data (str): The input string to be compressed.
        
        Returns:
            tuple: A tuple containing the compressed data as a bytearray and the Huffman tree.
        """
        # Calculate frequency of each character
        frequency = Counter(data)
        # Build Huffman tree
        huffman_tree = self.build_tree(frequency)
        # Generate Huffman codes
        huffman_codes = self.build_codes(huffman_tree)
        
        # Encode data using Huffman codes
        encoded_data = "".join(huffman_codes[char] for char in data)
        
        # Convert the encoded string to bytes using bit-packing
        byte_array = bytearray()
        current_byte = 0
        bits_filled = 0
        
        for bit in encoded_data:
            current_byte = (current_byte << 1) | int(bit)
            bits_filled += 1
            if bits_filled == 8:
                byte_array.append(current_byte)
                current_byte = 0
                bits_filled = 0
        
        # Append the last byte if there are remaining bits
        if bits_filled > 0:
            current_byte = current_byte << (8 - bits_filled)
            byte_array.append(current_byte)
        
        return byte_array, huffman_tree

    def decompress(self, byte_array, huffman_tree):
        """
        Decompress the input bytearray using the Huffman tree.
        
        Args:
            byte_array (bytearray): The compressed data as a bytearray.
            huffman_tree (HuffmanNode): The root node of the Huffman tree.
        
        Returns:
            bytearray: The decompressed data.
        """
        current_node = huffman_tree
        decoded_data = bytearray()
        
        # Decode the encoded string using the Huffman tree
        for byte in byte_array:
            bits = f"{byte:08b}"
            for bit in bits:
                current_node = current_node.left if bit == "0" else current_node.right

                if current_node.char is not None:
                    decoded_data.append(current_node.char)
                    current_node = huffman_tree
        
        return decoded_data