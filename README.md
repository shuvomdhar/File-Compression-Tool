# Huffman File Compression Tool

A Python implementation of file compression using Huffman encoding algorithm. This tool can compress any type of file while preserving the original file extension and provides both compression and decompression capabilities.

## Features

- **Universal File Support**: Compresses any file type (text, images, documents, executables, etc.)
- **Huffman Encoding**: Implements the optimal lossless compression algorithm
- **Preserves File Extensions**: Maintains original file extensions for seamless file handling
- **Compression Statistics**: Detailed metrics including compression ratio and space saved
- **Round-trip Support**: Full compression and decompression functionality
- **Interactive CLI**: User-friendly command-line interface
- **Programmatic API**: Easy integration into other Python projects
- **Error Handling**: Comprehensive error handling with informative messages

## Installation

1. Clone the repository:
```bash
git clone https://github.com/shuvomdhar/File-Compression-Tool.git
cd File-Compressor-Tool
```

2. Ensure you have Python 3.6+ installed:
```bash
python --version
```

3. No additional dependencies required - uses only Python standard library!

## Usage

### Interactive Mode

Run the tool interactively:

```bash
python huffman_compressor.py
```

You'll see a menu with options:
```
Huffman File Compression Tool
========================================

Options:
1. Compress file
2. Decompress file
3. Exit

Enter your choice (1-3):
```

### Programmatic Usage

```python
from huffman_compressor import HuffmanCompressor

# Create compressor instance
compressor = HuffmanCompressor()

# Compress a file
result = compressor.compress_file("document.pdf")
print(f"Original size: {result['original_size']:,} bytes")
print(f"Compressed size: {result['compressed_size']:,} bytes")
print(f"Compression ratio: {result['compression_ratio']:.2f}%")

# Decompress a file
result = compressor.decompress_file("document_compressed.pdf")
print(f"Decompression successful: {result['decompressed_file']}")
```

### Custom Output Paths

```python
# Specify custom output paths
compressor.compress_file("input.txt", "custom_compressed.txt")
compressor.decompress_file("custom_compressed.txt", "restored.txt")
```

## How It Works

### Huffman Encoding Algorithm

1. **Frequency Analysis**: Analyzes byte frequency in the input file
2. **Tree Construction**: Builds a binary tree where frequent bytes have shorter paths
3. **Code Generation**: Creates variable-length binary codes for each byte
4. **Encoding**: Replaces original bytes with their Huffman codes
5. **Storage**: Saves compressed data along with the tree structure

### File Structure

The compressed file contains:
- Huffman tree structure
- Encoded data as compressed bytes
- Padding information
- Original file size metadata

## Examples

### Text File Compression
```bash
Original file: example.txt (1,024 bytes)
Compressed file: example_compressed.txt (512 bytes)
Compression ratio: 50.00%
Space saved: 512 bytes
```

### Image File Compression
```bash
Original file: photo.jpg (2,048,576 bytes)
Compressed file: photo_compressed.jpg (1,536,432 bytes)
Compression ratio: 25.00%
Space saved: 512,144 bytes
```

## File Naming Convention

- **Compression**: `filename.ext` → `filename_compressed.ext`
- **Decompression**: `filename_compressed.ext` → `filename_decompressed.ext`

## API Reference

### HuffmanCompressor Class

#### `compress_file(input_path, output_path=None)`
Compresses a file using Huffman encoding.

**Parameters:**
- `input_path` (str): Path to the input file
- `output_path` (str, optional): Path for compressed output file

**Returns:**
- Dictionary with compression statistics

**Raises:**
- `FileNotFoundError`: If input file doesn't exist
- `ValueError`: If input file is empty

#### `decompress_file(compressed_path, output_path=None)`
Decompresses a Huffman-compressed file.

**Parameters:**
- `compressed_path` (str): Path to the compressed file
- `output_path` (str, optional): Path for decompressed output file

**Returns:**
- Dictionary with decompression information

**Raises:**
- `FileNotFoundError`: If compressed file doesn't exist
- `pickle.UnpicklingError`: If file is corrupted or not a valid compressed file

## Performance

### Compression Effectiveness

The compression ratio depends on the file content:
- **Text files**: 40-60% compression ratio
- **Code files**: 30-50% compression ratio
- **Already compressed files** (ZIP, JPEG): Minimal compression
- **Binary files**: Varies based on entropy

### Memory Usage

- Memory usage scales with file size
- Huffman tree size depends on the number of unique bytes (max 256)
- Suitable for files up to several GB on modern systems

## Limitations

- **No streaming**: Entire file must be loaded into memory
- **Pickle dependency**: Uses Python's pickle for tree storage
- **Single-threaded**: No parallel processing support
- **No encryption**: Compressed files are not encrypted

## Error Handling

The tool handles various error conditions:
- File not found
- Empty files
- Corrupted compressed files
- Permission errors
- Disk space issues

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and add tests
4. Commit your changes: `git commit -am 'Add feature'`
5. Push to the branch: `git push origin feature-name`
6. Submit a pull request

## Testing

Run the built-in tests:
```python
# Test with a sample file
compressor = HuffmanCompressor()
result = compressor.compress_file("test.txt")
result = compressor.decompress_file("test_compressed.txt")
```

## License

This project is licensed under the MIT License.

## Acknowledgments

- David A. Huffman for the Huffman coding algorithm
- Python Software Foundation for the excellent standard library
- Contributors and users of this project

## Support

If you encounter any issues or have questions:
1. Check the error message for specific details
2. Ensure you have Python 3.6+ installed
3. Verify file paths are correct and accessible
4. Open an issue on GitHub for bug reports or feature requests

## Version History

- **v1.0.0**: Initial release with basic compression and decompression
- Features planned for future releases:
  - Streaming compression for large files
  - Multi-threading support
  - GUI interface
  - Compression format improvements