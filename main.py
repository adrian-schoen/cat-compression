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
    extract_catc_from_png(input_file, extracted_file)
    decompress_file(extracted_file, output_file)
    os.remove(extracted_file)

def main():
    parser = argparse.ArgumentParser(description="CatCompression - Custom File Compression Tool")
    parser.add_argument('mode', choices=['catcompress', 'catextract'], help="Mode: catcompress or catextract")
    parser.add_argument('input_file', help="Input file path")
    parser.add_argument('output_file', help="Output file path")
    parser.add_argument('--png_file', help="PNG file path for catcompress mode")

    args = parser.parse_args()

    if args.mode == 'catcompress':
        if args.png_file is None:
            print("Error: --png_file is required for catcompress mode.")
            return
        compress_and_attach(args.input_file, args.png_file, args.output_file)
    elif args.mode == 'catextract':
        extract_and_decompress(args.input_file, args.output_file)

if __name__ == "__main__":
    main()

# python main.py catcompress input.txt output_with_catc.png --png_file cat.png

# python main.py catextract output_with_catc.png decompressed_output.txt