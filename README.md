# CatCompression

## Work in Progress

**Disclaimer:** This project is currently a work in progress. Features and functionality may change as development continues. Please check back for updates!

---

CatCompression is a specialized file compression tool that employs Huffman coding to efficiently compress files and seamlessly embed the compressed data within a PNG image of a cat. This innovative tool not only facilitates the compression process but also allows for easy extraction and decompression of the data from the PNG image. Designed for both efficiency and convenience, CatCompression offers a unique way to store data discreetly within a charming cat image file.

## Features

- **File Compression:** Compresses one or more input files using Huffman coding.
- **Data Embedding:** Embeds the compressed data into a single PNG image file.
- **Data Extraction:** Extracts the compressed data from one or more PNG image files.
- **File Decompression:** Decompresses the extracted data back into its original form.
- **Batch Processing:** Supports handling multiple input text files for compression into a single PNG and multiple PNG files for separate extraction and decompression.

## Getting Started

### Prerequisites

Ensure you have Python installed. This project is compatible with Python 3.x.

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/adrian-schoen/cat-compression/
   cd CatCompression
   ```

2. Install the required packages:

   ```bash
   pip install tqdm
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

To compress one or more text files and attach the compressed data to a PNG image:

```bash
python main.py catcompress <input_folder> <output_folder> <cat_folder>
```

- `<input_folder>`: Folder containing one or more `.txt` files to be compressed.
- `<output_folder>`: Folder where the resulting PNG image with embedded data will be saved.
- `<cat_folder>`: Folder containing `cat.png` (the image to attach the data to).

All `.txt` files in the `<input_folder>` will be compressed and concatenated before being embedded into a single PNG file.

#### Extract and Decompress Data from PNG(s)

To extract and decompress data from one or more PNG images:

```bash
python main.py catextract <input_folder> <output_folder> <cat_folder>
```

- `<input_folder>`: Folder containing one or more `.png` files with embedded data.
- `<output_folder>`: Folder where the decompressed files will be saved.
- `<cat_folder>`: Folder containing `cat.png` (used for validation).

Each PNG file in the `<input_folder>` will be processed separately, with the decompressed files being saved in a subfolder named after the PNG file (without its extension).

### Example

1. **Compress and Attach:**

   Assume you have the following structure:

   - `input/`: Contains `input1.txt`, `input2.txt` (the files to be compressed).
   - `output/`: Empty directory where the result will be saved.
   - `cat/`: Contains `cat.png` (the image used for embedding).

   Run:

   ```bash
   python main.py catcompress input output cat
   ```

   The compressed data from both `input1.txt` and `input2.txt` will be attached to `cat.png`, and the resulting image will be saved as `compressed_with_catc.png` in the `output/` directory.

2. **Extract and Decompress:**

   Use the `compressed_with_catc.png` from the previous step, or multiple PNGs in the `input/` folder, to extract and decompress:

   ```bash
   python main.py catextract input output cat
   ```

   The extracted and decompressed data from each PNG will be saved in separate subfolders within the `output/` directory, named after each PNG file (e.g., `output/compressed_with_catc/`).

### Notes

- The `.catc` file is a temporary file created during the compression and attaching process. It is automatically deleted after the operation.
- Ensure that `cat.png` remains consistent between compression and extraction to avoid errors.

## Contributing

Feel free to fork the repository and submit pull requests. If you encounter any issues, please report them via GitHub Issues.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

---

Enjoy using CatCompression! Hide your data in plain sight! 🐱