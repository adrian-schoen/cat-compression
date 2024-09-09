import argparse
import os
import pickle
from typing import List, Tuple
from huffman import HuffmanCompressor
from utils import read_file, attach_to_png, extract_catc_from_png
from tqdm import tqdm

# Constants
FILE_SEPARATOR = b'FILE_SEPARATOR'
TXT_EXTENSION = '.txt'
PNG_EXTENSION = '.png'

def get_ascii_cat() -> str:
    return r"""
   _____         _      _____                                        _             
  / ____|       | |    / ____|                                      (_)            
 | |            | |_  | |     ___  _ __ ___  _ __  _ __ ___  ___ ___ _  ___  _ __  
 | |      /\_/\ | __| | |    / _ \| '_ ` _ \| '_ \| '__/ _ \/ __/ __| |/ _ \| '_ \ 
 | |____ ( o.o )| |_  | |___| (_) | | | | | | |_) | | |  __/\__ \__ \ | (_) | | | |
  \_____| > ^ <  \__|  \_____\___/|_| |_| |_| .__/|_|  \___||___/___/_|\___/|_| |_| 
                                            | |                                    
                                            |_|                                    
"""

def compress_files(input_folder: str) -> List[Tuple[str, bytes, dict]]:
    """
    Compress all .txt files in the input folder using Huffman compression.
    
    Args:
        input_folder (str): Path to the folder containing .txt files to compress.
    
    Returns:
        list: A list of tuples containing filename, compressed data, and Huffman tree.
    """
    compressed_files = []
    compressor = HuffmanCompressor()
    txt_files = [f for f in os.listdir(input_folder) if f.endswith(TXT_EXTENSION)]
    
    for filename in tqdm(txt_files, desc="Compressing files", unit="file"):
        input_file = os.path.join(input_folder, filename)
        try:
            data = read_file(input_file)
            compressed_data, huffman_tree = compressor.compress(data)
            compressed_files.append((filename, compressed_data, huffman_tree))
        except Exception as e:
            print(f"Failed to compress {filename}: {e}")
    
    return compressed_files

def concatenate_compressed_files(compressed_files: List[Tuple[str, bytes, dict]]) -> bytes:
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

def compress_and_attach(input_folder: str, png_file: str, output_file: str) -> None:
    """
    Compress all .txt files in the input folder and attach the compressed data to a PNG file.
    
    Args:
        input_folder (str): Path to the folder containing .txt files to compress.
        png_file (str): Path to the PNG file to attach the compressed data to.
        output_file (str): Path to save the output PNG file with attached compressed data.
    """
    print(get_ascii_cat())

    compressed_files = compress_files(input_folder)
    concatenated_data = concatenate_compressed_files(compressed_files)
    
    try:
        attach_to_png(png_file, concatenated_data, output_file)
        print(f"Attached compressed data to '{png_file}' and saved as '{output_file}'.")
    except Exception as e:
        print(f"Failed to attach compressed data to PNG: {e}")

def extract_and_decompress(input_file: str, output_folder: str) -> None:
    """
    Extract and decompress data from a PNG file.
    
    Args:
        input_file (str): Path to the PNG file containing the compressed data.
        output_folder (str): Path to save the decompressed .txt files.
    """
    print(get_ascii_cat())
    
    try:
        concatenated_data = extract_catc_from_png(input_file)
    except Exception as e:
        print(f"Failed to extract data from PNG: {e}")
        return
    
    files_data = concatenated_data.split(FILE_SEPARATOR)
    compressor = HuffmanCompressor()
    
    for file_data in tqdm(files_data, desc="Extracting files", unit="file"):
        if file_data:
            try:
                filename, compressed_data, huffman_tree = pickle.loads(file_data)
                decompressed_data = compressor.decompress(compressed_data, huffman_tree)
                output_file = os.path.join(output_folder, filename)
                with open(output_file, 'wb') as file:
                    file.write(decompressed_data)
            except Exception as e:
                print(f"Failed to decompress file data: {e}")
    
    print(f"Extracted data from '{input_file}' to '{output_folder}'.")

def main() -> None:
    """
    Main function to handle command-line arguments and execute the appropriate mode.
    """
    parser = argparse.ArgumentParser(description="CatCompression - Custom File Compression Tool")
    parser.add_argument('mode', choices=['compress', 'extract'], help="Mode: compress or extract")
    parser.add_argument('input_folder', help="Input folder path")
    parser.add_argument('output_folder', help="Output folder path")
    parser.add_argument('cat_folder', help="Cat folder path containing cat.png")
    
    args = parser.parse_args()
    
    if args.mode == 'compress':
        png_file = os.path.join(args.cat_folder, 'cat.png')
        if not os.path.exists(png_file):
            print(f"Error: '{png_file}' does not exist.")
            return
    
        output_file = os.path.join(args.output_folder, 'compressed_with_catc.png')
        compress_and_attach(args.input_folder, png_file, output_file)
    elif args.mode == 'extract':
        png_files = [f for f in os.listdir(args.input_folder) if f.endswith(PNG_EXTENSION)]
        if not png_files:
            print(f"Error: No .png files found in '{args.input_folder}'.")
            return
    
        for filename in png_files:
            input_file = os.path.join(args.input_folder, filename)
            output_subfolder = os.path.join(args.output_folder, os.path.splitext(filename)[0])
            os.makedirs(output_subfolder, exist_ok=True)
            extract_and_decompress(input_file, output_subfolder)

if __name__ == "__main__":
    main()