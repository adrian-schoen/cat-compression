import heapq
from collections import Counter
from typing import Dict, Tuple, Optional

class HuffmanNode:
    def __init__(self, char: Optional[str], freq: int) -> None:
        """
        Initialize a HuffmanNode with a character and its frequency.
        
        Args:
            char (Optional[str]): The character represented by the node.
            freq (int): The frequency of the character.
        """
        self.char = char
        self.freq = freq
        self.left: Optional[HuffmanNode] = None
        self.right: Optional[HuffmanNode] = None

    def __lt__(self, other: 'HuffmanNode') -> bool:
        """
        Less-than comparison based on frequency for priority queue.
        
        Args:
            other (HuffmanNode): The other node to compare against.
        
        Returns:
            bool: True if this node's frequency is less than the other node's frequency.
        """
        return self.freq < other.freq

class HuffmanCompressor:
    def build_tree(self, frequency: Dict[str, int]) -> HuffmanNode:
        """
        Build the Huffman tree based on character frequencies.
        
        Args:
            frequency (Dict[str, int]): A dictionary with characters as keys and their frequencies as values.
        
        Returns:
            HuffmanNode: The root node of the Huffman tree.
        """
        heap = [HuffmanNode(char, freq) for char, freq in frequency.items()]
        heapq.heapify(heap)
        
        while len(heap) > 1:
            left = heapq.heappop(heap)
            right = heapq.heappop(heap)
            merged = HuffmanNode(None, left.freq + right.freq)
            merged.left = left
            merged.right = right
            heapq.heappush(heap, merged)
        
        return heap[0]

    def build_codes(self, root: HuffmanNode) -> Dict[str, str]:
        """
        Generate Huffman codes for each character based on the Huffman tree.
        
        Args:
            root (HuffmanNode): The root node of the Huffman tree.
        
        Returns:
            Dict[str, str]: A dictionary with characters as keys and their Huffman codes as values.
        """
        codes = {}
        
        def _generate_codes(node: HuffmanNode, current_code: str) -> None:
            if node is None:
                return
            if node.char is not None:
                codes[node.char] = current_code
                return
            _generate_codes(node.left, current_code + "0")
            _generate_codes(node.right, current_code + "1")
        
        _generate_codes(root, "")
        return codes

    def compress(self, data: str) -> Tuple[bytearray, HuffmanNode]:
        """
        Compress the input data using Huffman coding.
        
        Args:
            data (str): The input string to be compressed.
        
        Returns:
            Tuple[bytearray, HuffmanNode]: A tuple containing the compressed data as a bytearray and the Huffman tree.
        """
        frequency = Counter(data)
        huffman_tree = self.build_tree(frequency)
        huffman_codes = self.build_codes(huffman_tree)
        
        encoded_data = "".join(huffman_codes[char] for char in data)
        
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
        
        if bits_filled > 0:
            current_byte = current_byte << (8 - bits_filled)
            byte_array.append(current_byte)
        
        return byte_array, huffman_tree

    def decompress(self, byte_array: bytearray, huffman_tree: HuffmanNode) -> bytearray:
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
        
        for byte in byte_array:
            bits = f"{byte:08b}"
            for bit in bits:
                current_node = current_node.left if bit == "0" else current_node.right

                if current_node.char is not None:
                    decoded_data.append(current_node.char)
                    current_node = huffman_tree
        
        return decoded_data