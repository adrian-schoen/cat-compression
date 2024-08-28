# CatCompression

CatCompression is a custom file compression tool that utilizes Huffman coding to compress files and embed the compressed data into a PNG image. The tool also supports extracting and decompressing the data from the PNG image. The project is designed to efficiently compress data and conveniently hide it within an image file.

## Features

- **File Compression:** Compresses input files using Huffman coding.
- **Data Embedding:** Embeds the compressed data into a PNG image file.
- **Data Extraction:** Extracts the compressed data from the PNG image file.
- **File Decompression:** Decompresses the extracted data back into its original form.

## Getting Started

### Prerequisites

Ensure you have Python installed. This project is compatible with Python 3.x.

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/adrian-schoen/cat-compression/
   cd CatCompression
   ```

2. Install the required Python packages:

   ```bash
   pip install -r requirements.txt
   ```

### Project Structure

- `main.py`: The main script for compressing, attaching, extracting, and decompressing files.
- `utils.py`: Contains utility functions for reading, writing, and handling files.
- `huffman.py`: Implements Huffman coding for data compression and decompression.
- `input/`: Directory for storing input files.
- `output/`: Directory for storing output files.
- `cat/`: Directory for storing the cat.png file used for embedding.

### Usage

#### Compress and Attach Data to a PNG

To compress a file and attach the compressed data to a PNG image:

```bash
python main.py catcompress <input_folder> <output_folder> <cat_folder>
```

- `<input_folder>`: Folder containing `input.txt` (the file to be compressed).
- `<output_folder>`: Folder where the resulting PNG image with embedded data will be saved.
- `<cat_folder>`: Folder containing `cat.png` (the image to attach the data to).

#### Extract and Decompress Data from a PNG

To extract and decompress data from a PNG image:

```bash
python main.py catextract <input_folder> <output_folder> <cat_folder>
```

- `<input_folder>`: Folder containing `output_with_catc.png` (the PNG file with embedded data).
- `<output_folder>`: Folder where the decompressed file will be saved.
- `<cat_folder>`: Folder containing `cat.png` (used for validation).

### Example

1. **Compress and Attach:**

   Assume you have the following structure:

   - `input/`: Contains `input.txt` (the file to be compressed).
   - `output/`: Empty directory where the result will be saved.
   - `cat/`: Contains `cat.png` (the image used for embedding).

   Run:

   ```bash
   python main.py catcompress input output cat
   ```

   The compressed data will be attached to `cat.png`, and the resulting image will be saved as `output_with_catc.png` in the `output/` directory.

2. **Extract and Decompress:**

   Use the `output_with_catc.png` from the previous step to extract and decompress:

   ```bash
   python main.py catextract input output cat
   ```

   The extracted and decompressed data will be saved as `decompressed_output.txt` in the `output/` directory.

### Notes

- The `.catc` file is a temporary file created during the compression and attaching process. It is automatically deleted after the operation.
- Ensure that `cat.png` remains consistent between compression and extraction to avoid errors.

## Contributing

Feel free to fork the repository and submit pull requests. If you encounter any issues, please report them via GitHub Issues.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

---

Enjoy using CatCompression! Hide your data in plain sight! 🐱

