import argparse
import os
import pickle
from huffman import HuffmanCompressor
from utils import read_file, write_file, attach_to_png, extract_catc_from_png

# Separator used to distinguish between different files in the concatenated data
FILE_SEPARATOR = b'FILE_SEPARATOR'

def compress_files(input_folder):
    """
    Compress all .txt files in the input folder using Huffman compression.
    
    Args:
        input_folder (str): Path to the folder containing .txt files to compress.
    
    Returns:
        list: A list of tuples containing filename, compressed data, and Huffman tree.
    """
    compressed_files = []
    compressor = HuffmanCompressor()
    
    for filename in os.listdir(input_folder):
        if filename.endswith('.txt'):
            input_file = os.path.join(input_folder, filename)
            data = read_file(input_file)
            compressed_data, huffman_tree = compressor.compress(data)
            compressed_files.append((filename, compressed_data, huffman_tree))
    
    return compressed_files

def concatenate_compressed_files(compressed_files):
    """
    Concatenate compressed files with a separator.
    
    Args:
        compressed_files (list): List of tuples containing filename, compressed data, and Huffman tree.
    
    Returns:
        bytes: Concatenated compressed data with separators.
    """
    concatenated_data = b''
    for filename, compressed_data, huffman_tree in compressed_files:
        file_data = pickle.dumps((filename, compressed_data, huffman_tree))
        concatenated_data += file_data + FILE_SEPARATOR
    return concatenated_data

def compress_and_attach(input_folder, png_file, output_file):
    """
    Compress all .txt files in the input folder and attach the compressed data to a PNG file.
    
    Args:
        input_folder (str): Path to the folder containing .txt files to compress.
        png_file (str): Path to the PNG file to attach the compressed data to.
        output_file (str): Path to save the output PNG file with attached compressed data.
    """
    compressed_files = compress_files(input_folder)
    concatenated_data = concatenate_compressed_files(compressed_files)
    
    with open('temp_compressed.catc', 'wb') as file:
        file.write(concatenated_data)
    
    attach_to_png(png_file, 'temp_compressed.catc', output_file)
    os.remove('temp_compressed.catc')

def extract_and_decompress(input_file, output_folder):
    """
    Extract and decompress data from a PNG file.
    
    Args:
        input_file (str): Path to the PNG file containing the compressed data.
        output_folder (str): Path to save the decompressed .txt files.
    """
    extracted_file = 'temp_extracted.catc'
    extract_catc_from_png(input_file, extracted_file)
    
    with open(extracted_file, 'rb') as file:
        concatenated_data = file.read()
    
    os.remove(extracted_file)
    
    files_data = concatenated_data.split(FILE_SEPARATOR)
    compressor = HuffmanCompressor()
    
    for file_data in files_data:
        if file_data:
            filename, compressed_data, huffman_tree = pickle.loads(file_data)
            decompressed_data = compressor.decompress(compressed_data, huffman_tree)
            output_file = os.path.join(output_folder, filename)
            with open(output_file, 'wb') as file:
                file.write(decompressed_data)
    
    print(f"Files extracted and decompressed to '{output_folder}'.")

def main():
    """
    Main function to handle command-line arguments and execute the appropriate mode.
    """
    parser = argparse.ArgumentParser(description="CatCompression - Custom File Compression Tool")
    parser.add_argument('mode', choices=['catcompress', 'catextract'], help="Mode: catcompress or catextract")
    parser.add_argument('input_folder', help="Input folder path")
    parser.add_argument('output_folder', help="Output folder path")
    parser.add_argument('cat_folder', help="Cat folder path containing cat.png")

    args = parser.parse_args()

    if args.mode == 'catcompress':
        png_file = os.path.join(args.cat_folder, 'cat.png')
        if not os.path.exists(png_file):
            print(f"Error: '{png_file}' does not exist.")
            return

        output_file = os.path.join(args.output_folder, 'compressed_with_catc.png')
        compress_and_attach(args.input_folder, png_file, output_file)
    elif args.mode == 'catextract':
        png_file = os.path.join(args.cat_folder, 'cat.png')
        if not os.path.exists(png_file):
            print(f"Error: '{png_file}' does not exist.")
            return

        input_file = os.path.join(args.input_folder, 'compressed_with_catc.png')
        extract_and_decompress(input_file, args.output_folder)

if __name__ == "__main__":
    main()