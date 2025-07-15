import heapq
import pickle
import time
import os
from collections import defaultdict, Counter
from pathlib import Path

class HuffmanNode:
    """Node class for Huffman tree"""
    def __init__(self, char=None, freq=0, left=None, right=None):
        self.char = char
        self.freq = freq
        self.left = left
        self.right = right
    
    def __lt__(self, other):
        return self.freq < other.freq

class HuffmanCompressor:
    """Huffman encoding compression tool"""
    
    def __init__(self):
        self.root = None
        self.codes = {}
        self.reverse_codes = {}
    
    def _build_frequency_table(self, data):
        """Build frequency table from data bytes"""
        return Counter(data)
    
    def _build_huffman_tree(self, freq_table):
        """Build Huffman tree from frequency table"""
        heap = []
        
        # Create leaf nodes for each character
        for char, freq in freq_table.items():
            node = HuffmanNode(char, freq)
            heapq.heappush(heap, node)
        
        # Handle single character case
        if len(heap) == 1:
            root = HuffmanNode(freq=heap[0].freq)
            root.left = heapq.heappop(heap)
            return root
        
        # Build tree bottom-up
        while len(heap) > 1:
            left = heapq.heappop(heap)
            right = heapq.heappop(heap)
            
            parent = HuffmanNode(freq=left.freq + right.freq)
            parent.left = left
            parent.right = right
            
            heapq.heappush(heap, parent)
        
        return heap[0]
    
    def _generate_codes(self, root):
        """Generate Huffman codes from tree"""
        if not root:
            return {}
        
        codes = {}
        
        def traverse(node, code=""):
            if node.char is not None:  # Leaf node
                codes[node.char] = code if code else "0"  # Handle single char case
                return
            
            if node.left:
                traverse(node.left, code + "0")
            if node.right:
                traverse(node.right, code + "1")
        
        traverse(root)
        return codes
    
    def _encode_data(self, data, codes):
        """Encode data using Huffman codes"""
        encoded = ""
        for byte in data:
            encoded += codes[byte]
        return encoded
    
    def _decode_data(self, encoded_data, root):
        """Decode data using Huffman tree"""
        if not root:
            return bytes()
        
        decoded = []
        current = root
        
        for bit in encoded_data:
            if bit == "0":
                current = current.left
            else:
                current = current.right
            
            if current.char is not None:  # Leaf node
                decoded.append(current.char)
                current = root
        
        return bytes(decoded)
    
    def compress_file(self, input_path, output_path=None):
        """Compress a file using Huffman encoding"""
        input_path = Path(input_path)
        
        if not input_path.exists():
            raise FileNotFoundError(f"Input file {input_path} not found")
        
        # Generate output path if not provided
        if output_path is None:
            output_path = input_path.parent / f"{input_path.stem}_compressed{input_path.suffix}"
        else:
            output_path = Path(output_path)
        
        # Read input file
        with open(input_path, 'rb') as f:
            data = f.read()
        
        if not data:
            raise ValueError("Input file is empty")
        
        # Build frequency table
        freq_table = self._build_frequency_table(data)
        
        # Build Huffman tree
        self.root = self._build_huffman_tree(freq_table)
        
        # Generate codes
        self.codes = self._generate_codes(self.root)
        self.reverse_codes = {v: k for k, v in self.codes.items()}
        
        # Encode data
        encoded_data = self._encode_data(data, self.codes)
        
        # Convert bit string to bytes
        # Add padding to make it multiple of 8
        padding = 8 - len(encoded_data) % 8
        if padding != 8:
            encoded_data += "0" * padding
        
        # Convert to bytes
        encoded_bytes = bytearray()
        for i in range(0, len(encoded_data), 8):
            byte = encoded_data[i:i+8]
            encoded_bytes.append(int(byte, 2))
        
        # Create compression data
        compression_data = {
            'tree': self.root,
            'encoded_data': bytes(encoded_bytes),
            'padding': padding,
            'original_size': len(data),
            'compressed_size': len(encoded_bytes)
        }
        
        # Save compressed file
        with open(output_path, 'wb') as f:
            pickle.dump(compression_data, f)
        
        # Calculate compression ratio
        original_size = len(data)
        compressed_size = output_path.stat().st_size
        compression_ratio = (1 - compressed_size / original_size) * 100
        
        return {
            'original_file': str(input_path),
            'compressed_file': str(output_path),
            'original_size': original_size,
            'compressed_size': compressed_size,
            'compression_ratio': compression_ratio,
            'space_saved': original_size - compressed_size
        }
    
    def decompress_file(self, compressed_path, output_path=None):
        """Decompress a Huffman compressed file"""
        compressed_path = Path(compressed_path)
        
        if not compressed_path.exists():
            raise FileNotFoundError(f"Compressed file {compressed_path} not found")
        
        # Generate output path if not provided
        if output_path is None:
            stem = compressed_path.stem
            if stem.endswith('_compressed'):
                stem = stem[:-11]  # Remove '_compressed'
            output_path = compressed_path.parent / f"{stem}_decompressed{compressed_path.suffix}"
        else:
            output_path = Path(output_path)
        
        # Load compressed data
        with open(compressed_path, 'rb') as f:
            compression_data = pickle.load(f)
        
        # Extract components
        tree = compression_data['tree']
        encoded_bytes = compression_data['encoded_data']
        padding = compression_data['padding']
        
        # Convert bytes back to bit string
        bit_string = ""
        for byte in encoded_bytes:
            bit_string += format(byte, '08b')
        
        # Remove padding
        if padding != 8:
            bit_string = bit_string[:-padding]
        
        # Decode data
        decoded_data = self._decode_data(bit_string, tree)
        
        # Save decompressed file
        with open(output_path, 'wb') as f:
            f.write(decoded_data)
        
        return {
            'compressed_file': str(compressed_path),
            'decompressed_file': str(output_path),
            'original_size': compression_data['original_size'],
            'decompressed_size': len(decoded_data)
        }

# create a async function to show the user to keep patience and please wait
def show_wait_message():
    """Show a message to the user to keep patience"""
    print("Please wait, this may take a while...")

def main():
    """Main function to demonstrate the compressor"""
    compressor = HuffmanCompressor()
    
    print("Huffman File Compression Tool")
    print("=" * 40)
    
    while True:
        print("\nOptions:")
        print("1. Compress file")
        print("2. Decompress file")
        print("3. Exit")
        
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == '1':
            try:
                file_path = input("Enter file path to compress: ").strip()
                print(f"Compressing....")
                time.sleep(5)
                show_wait_message()
                result = compressor.compress_file(file_path)
                
                print(f"\nCompression successful!")
                print(f"Original file: {result['original_file']}")
                print(f"Compressed file: {result['compressed_file']}")
                print(f"Original size: {result['original_size']:,} bytes")
                print(f"Compressed size: {result['compressed_size']:,} bytes")
                print(f"Space saved: {result['space_saved']:,} bytes")
                print(f"Compression ratio: {result['compression_ratio']:.2f}%")
                
            except Exception as e:
                print(f"Error during compression: {e}")
        
        elif choice == '2':
            try:
                file_path = input("Enter compressed file path: ").strip()
                print(f"Decompressing....")
                time.sleep(5)
                show_wait_message()
                result = compressor.decompress_file(file_path)
                
                print(f"\nDecompression successful!")
                print(f"Compressed file: {result['compressed_file']}")
                print(f"Decompressed file: {result['decompressed_file']}")
                print(f"Original size: {result['original_size']:,} bytes")
                print(f"Decompressed size: {result['decompressed_size']:,} bytes")
                
            except Exception as e:
                print(f"Error during decompression: {e}")
        
        elif choice == '3':
            print("Goodbye!")
            break
        
        else:
            print("Invalid choice. Please try again.")

# Example usage
if __name__ == "__main__":
    # You can also use the compressor directly
    # compressor = HuffmanCompressor()
    # result = compressor.compress_file("example.txt")
    # print(f"Compression ratio: {result['compression_ratio']:.2f}%")
    
    main()