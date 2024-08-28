import pickle
import os

def read_file(file_path, compressed=False):
    if compressed:
        with open(file_path, 'rb') as file:
            compressed_data, huffman_tree = pickle.load(file)
        return compressed_data, huffman_tree
    else:
        with open(file_path, 'rb') as file:
            data = file.read()
        return data

def write_file(file_path, compressed_data, huffman_tree):
    with open(file_path, 'wb') as file:
        pickle.dump((compressed_data, huffman_tree), file)

def attach_to_png(png_file_path, catc_file_path, output_file_path):
    # Read the .png file content
    with open(png_file_path, 'rb') as png_file:
        png_data = png_file.read()

    # Read the .catc file content
    with open(catc_file_path, 'rb') as catc_file:
        catc_data = catc_file.read()

    # Combine .png data with .catc data
    combined_data = png_data + b'CATC_MARKER' + catc_data

    # Write the combined data to the output .png file
    with open(output_file_path, 'wb') as output_file:
        output_file.write(combined_data)

    print(f"Attached '{catc_file_path}' to '{png_file_path}' and saved as '{output_file_path}'.")

def extract_catc_from_png(png_file_path, catc_output_path):
    try:
        with open(png_file_path, 'rb') as file:
            # Read the entire file content
            file_content = file.read()

            # Find the marker indicating the start of the .catc data
            marker_index = file_content.rfind(b'CATC_MARKER')
            if marker_index == -1:
                raise ValueError("Marker not found in the PNG file.")

            # Extract the .catc data
            catc_data = file_content[marker_index + len(b'CATC_MARKER'):]

            # Write the extracted .catc data to a file
            with open(catc_output_path, 'wb') as catc_file:
                catc_file.write(catc_data)

        print(f"Extracted .catc data from '{png_file_path}' and saved as '{catc_output_path}'.")

    except OSError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")