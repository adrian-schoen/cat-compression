import pickle
from typing import Tuple, Union

def read_file(file_path: str, compressed: bool = False) -> Union[bytes, Tuple[bytes, dict]]:
    """
    Read a file from the given path. If compressed is True, it will read and return compressed data and Huffman tree.

    Args:
        file_path (str): Path to the file to read.
        compressed (bool): Flag indicating if the file is compressed.

    Returns:
        Union[bytes, Tuple[bytes, dict]]: The file data or a tuple containing compressed data and Huffman tree.
    """
    if compressed:
        with open(file_path, 'rb') as file:
            compressed_data, huffman_tree = pickle.load(file)
        return compressed_data, huffman_tree
    else:
        with open(file_path, 'rb') as file:
            data = file.read()
        return data

def write_file(file_path: str, compressed_data: bytes, huffman_tree: dict) -> None:
    """
    Write compressed data and Huffman tree to a file.

    Args:
        file_path (str): Path to the file to write.
        compressed_data (bytes): The compressed data to write.
        huffman_tree (dict): The Huffman tree to write.
    """
    with open(file_path, 'wb') as file:
        pickle.dump((compressed_data, huffman_tree), file)

def attach_to_png(png_file_path: str, concatenated_data: bytes, output_file_path: str) -> None:
    """
    Attach concatenated data to a PNG file and save it as a new file.

    Args:
        png_file_path (str): Path to the original PNG file.
        concatenated_data (bytes): The concatenated data to attach.
        output_file_path (str): Path to save the new PNG file with attached data.
    """
    with open(png_file_path, 'rb') as png_file:
        png_data = png_file.read()

    combined_data = png_data + b'CATC_MARKER' + concatenated_data

    with open(output_file_path, 'wb') as output_file:
        output_file.write(combined_data)

def extract_catc_from_png(png_file_path: str) -> bytes:
    """
    Extract concatenated data from a PNG file.

    Args:
        png_file_path (str): Path to the PNG file containing the concatenated data.

    Returns:
        bytes: The extracted concatenated data.
    """
    try:
        with open(png_file_path, 'rb') as file:
            file_content = file.read()

            marker_index = file_content.rfind(b'CATC_MARKER')
            if marker_index == -1:
                raise ValueError("Marker not found in the PNG file.")

            catc_data = file_content[marker_index + len(b'CATC_MARKER'):]
            return catc_data

    except OSError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")