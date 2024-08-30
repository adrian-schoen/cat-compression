import argparse
import os
import pickle
from huffman import HuffmanCompressor
from utils import read_file, write_file, attach_to_png, extract_catc_from_png

def compress_file(input_file, output_file):
    data = read_file(input_file)
    compressor = HuffmanCompressor()
    compressed_data, huffman_tree = compressor.compress(data)
    
    with open(output_file, 'wb') as file:
        pickle.dump((compressed_data, huffman_tree), file)
    
    print(f"File '{input_file}' compressed and saved as '{output_file}'.")

def decompress_file(input_file, output_file):
    with open(input_file, 'rb') as file:
        compressed_data, huffman_tree = pickle.load(file)
    
    compressor = HuffmanCompressor()
    decompressed_data = compressor.decompress(compressed_data, huffman_tree)
    
    with open(output_file, 'wb') as file:
        file.write(decompressed_data)
    
    print(f"File '{input_file}' decompressed and saved as '{output_file}'.")

def compress_and_attach(input_file, png_file, output_file):
    compressed_file = 'temp_compressed.catc'
    compress_file(input_file, compressed_file)
    attach_to_png(png_file, compressed_file, output_file)
    os.remove(compressed_file)

def extract_and_decompress(input_file, output_file):
    extracted_file = 'temp_extracted.catc'
    print(f"Extracting .catc file from '{input_file}' to '{extracted_file}'")
    extract_catc_from_png(input_file, extracted_file)
    if not os.path.exists(extracted_file):
        print(f"Error: Extracted file '{extracted_file}' does not exist.")
        return
    decompress_file(extracted_file, output_file)
    os.remove(extracted_file)

def main():
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

        for filename in os.listdir(args.input_folder):
            if filename.endswith('.txt'):
                input_file = os.path.join(args.input_folder, filename)
                output_file = os.path.join(args.output_folder, f"{os.path.splitext(filename)[0]}_with_catc.png")
                compress_and_attach(input_file, png_file, output_file)
    elif args.mode == 'catextract':
        png_file = os.path.join(args.cat_folder, 'cat.png')
        if not os.path.exists(png_file):
            print(f"Error: '{png_file}' does not exist.")
            return

        for filename in os.listdir(args.input_folder):
            if filename.endswith('_with_catc.png'):
                input_file = os.path.join(args.input_folder, filename)
                output_file = os.path.join(args.output_folder, f"{os.path.splitext(filename)[0].replace('_with_catc', '')}.txt")
                extract_and_decompress(input_file, output_file)

if __name__ == "__main__":
    main()