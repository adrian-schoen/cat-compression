import pickle

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
