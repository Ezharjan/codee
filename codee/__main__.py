import argparse
import codee.utils as utils
import hashlib

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
        utils.file_encode(filename=input_file, img_filename=holder_img, img_filename_new=output_img)
        print(f"Encoding complete! \nFile '{input_file}' encoded into '{output_img}'.")

    if args.decode:
        encoded_img, output_file = args.decode
        text_encode = utils.file_decode(output_file, img_filename=encoded_img)
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