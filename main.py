import argparse
from huffman import HuffmanCompressor
from utils import read_file, write_file
import pickle

def compress_file(input_file, output_file):
    """
    Compress the contents of the input file and save the compressed data to the output file.

    Args:
        input_file (str): Path to the input file to be compressed.
        output_file (str): Path to the output file where compressed data will be saved.
    """
    data = read_file(input_file)
    compressor = HuffmanCompressor()
    compressed_data, huffman_tree = compressor.compress(data)
    
    with open(output_file, 'wb') as file:
        pickle.dump((compressed_data, huffman_tree), file)
    
    print(f"File '{input_file}' compressed and saved as '{output_file}'.")

def decompress_file(input_file, output_file):
    """
    Decompress the contents of the input file and save the decompressed data to the output file.

    Args:
        input_file (str): Path to the input file containing compressed data.
        output_file (str): Path to the output file where decompressed data will be saved.
    """
    with open(input_file, 'rb') as file:
        compressed_data, huffman_tree = pickle.load(file)
    
    compressor = HuffmanCompressor()
    decompressed_data = compressor.decompress(compressed_data, huffman_tree)
    
    with open(output_file, 'wb') as file:
        file.write(decompressed_data)
    
    print(f"File '{input_file}' decompressed and saved as '{output_file}'.")

def main():
    """
    Main function to handle command-line arguments and perform compression or decompression.
    """
    parser = argparse.ArgumentParser(description="CatCompression - Custom File Compression Tool")
    parser.add_argument('mode', choices=['compress', 'decompress'], help="Mode: compress or decompress")
    parser.add_argument('input_file', help="Input file path")
    parser.add_argument('output_file', help="Output file path")

    args = parser.parse_args()

    if args.mode == 'compress':
        compress_file(args.input_file, args.output_file)
    elif args.mode == 'decompress':
        decompress_file(args.input_file, args.output_file)

if __name__ == "__main__":
    main()