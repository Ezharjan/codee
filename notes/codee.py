# pip install setuptools
# pip install numpy
# pip install Pillow
import struct
import hashlib
import argparse
import numpy as np
from PIL import Image


def serialization(data: bytes) -> bytes:
    """
    Input data, output its encapsulated byte type, which encapsulates the following content:
    - The length of the data (4 bytes)
    - Data itself (n bytes)
    """
    return len(data).to_bytes(length=4, byteorder="big") + data


def deserialization(serialized_data: bytes):
    return serialized_data[4 : 4 + int.from_bytes(serialized_data[:4], byteorder="big")]


def bytes2bin_(bytes1: bytes) -> str:
    return "".join([format(i, "08b") for i in bytes1])


def encode(bytes_data: bytes, img_filename: str, img_filename_new: str):
    data_to_write = serialization(bytes_data)
    img = np.array(Image.open(img_filename))
    height, width = img.shape[:2]
    data_to_write_bin = "".join([format(i, "08b") for i in data_to_write])
    assert len(data_to_write_bin) < height * width * 3, "Input file too big to encode!"

    for i, binary in enumerate(data_to_write_bin):
        x, y, c = (i // 3) // width, (i // 3) % width, i % 3
        tmp = img[x, y, c]
        if binary == "0":
            img[x, y, c] = tmp & 0b11111110
        if binary == "1":
            img[x, y, c] = tmp | 0b00000001
    Image.fromarray(img).save(img_filename_new)
    return img


def decode(img_filename: str) -> bytes:
    img = np.array(Image.open(img_filename))
    height, width = img.shape[:2]

    # get the 1st 4 bytes (only 32 binary storage lengths)
    lst = []
    for i in range(32):
        x, y, c = (i // 3) // width, (i // 3) % width, i % 3
        lst.append(img[x, y, c] & 0b00000001)

    # Get the real encoded data length (binary digits)
    len_data = int("".join(str(i) for i in lst), base=2) * 8
    lst = []
    for i in range(len_data + 32):
        x, y, c = (i // 3) // width, (i // 3) % width, i % 3
        lst.append(img[x, y, c] & 0b00000001)

    s_bin = "".join(str(i) for i in lst)

    s_out = b"".join(
        [
            struct.pack(">B", int(s_bin[i * 8 : i * 8 + 8], base=2))
            for i in range(len(s_bin) // 8)
        ]
    )
    return deserialization(s_out)


def file_encode(filename: str, img_filename: str, img_filename_new: str):
    with open(file=filename, mode="rb") as f:
        encode(
            bytes_data=f.read(),
            img_filename=img_filename,
            img_filename_new=img_filename_new,
        )


def file_decode(filename: str, img_filename: str):
    with open(file=filename, mode="wb") as f:
        f.write(decode(img_filename=img_filename))


def main():
    parser = argparse.ArgumentParser(description='Encode and decode files into images')
    parser.add_argument('-e', '--encode', nargs=3, metavar=('input_file', 'holder_img', 'output_img'), help='Encode a file into an image')
    parser.add_argument('-d', '--decode', nargs=2, metavar=('encoded_img', 'output_file'), help='Decode a file from an image')
    parser.add_argument('-c', '--check', nargs=2, metavar=('original_file', 'decoded_file'), help='Check if the original and decoded files match')
    parser.add_argument('-v', '--version', action='store_true', help='Show version')
    args = parser.parse_args()

    if not any(vars(args).values()):
        print("Sorry, please use -h for help!")
        return
    
    if args.version:
        print("""
Please check the version information from the PyPI website at https://pypi.org
        """)
        return

    if args.encode:
        input_file, holder_img, output_img = args.encode
        file_encode(filename=input_file, img_filename=holder_img, img_filename_new=output_img)
        print(f"Encoding complete! \nFile '{input_file}' encoded into '{output_img}'.")

    if args.decode:
        encoded_img, output_file = args.decode
        text_encode = file_decode(output_file, img_filename=encoded_img)
        print(f"Decoding complete! \nFile '{encoded_img}' decoded into '{output_file}'.")

    if args.check:
        original_file, decoded_file = args.check
        try:
            with open(original_file, 'rb') as f1, open(decoded_file, 'rb') as f2:
                assert hashlib.md5(f1.read()).hexdigest() == hashlib.md5(f2.read()).hexdigest()
                print(f"The original file '{original_file}' and the decoded file '{decoded_file}' match.")
        except AssertionError:
            print(f"The original file '{original_file}' and the decoded file '{decoded_file}' do not match!!!")
        except FileNotFoundError:
            print(f"One or both of the files '{original_file}' and '{decoded_file}' were not found!")
        except Exception as e:
            print(f"An error occurred while checking the files: {e}!")

if __name__ == "__main__":
    main()