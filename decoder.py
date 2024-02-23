import hashlib
import logging
import os
import glob
import argparse as ap


class InvalidHashDetected(Exception):
    """Raises and exception when an invalid hash is detected with a part of the file."""
    pass


def decode(file_path, chunk_size=1048576):

    # Variables for local use
    os.chdir(file_path)
    file_count = len(glob.glob('*'))

    # Fetch the first hash and load it
    hash_key = open("h0.bin", "rb").read(32)

    # Process each part
    for i in range(0, file_count - 1):
        # Determine the name of the chunks to parse
        file_content = open(f"b{i}h{i+1}.bin", "rb").read(chunk_size + 32)
        curr_hash = hashlib.sha256(file_content).digest()

        # Check that the hashes match
        if hash_key != curr_hash:
            logging.error("\nCurr hash: {}\nHash  Key: {}".format(curr_hash, hash_key))
            raise InvalidHashDetected()
        else:
            logging.debug("\nCurr hash: {}\nHash  Key: {}".format(curr_hash, hash_key))
            hash_key = file_content[-32:]


if __name__ == "__main__":
    parser = ap.ArgumentParser(
        prog='Decoder',
        description='Decode chunks of videos into binary files with hashes')
    parser.add_argument('filepath', type=str,
                        help='folder path of the chunks + hashes. Please provide no spaces in the file name')
    parser.add_argument('--chunk-size', default=1048576,
                        help='the size of chunks you want in bytes, default is 1048576')
    parser.add_argument('--logs', action='store_true',
                        help='Set logs to higher verbosity')
    args = parser.parse_args()

    if args.logs:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.ERROR)

    try:
        decode(file_path="FLIRT_TRAINS", chunk_size=args.chunk_size)
        print("Decoded chunks successfully")
    except InvalidHashDetected:
        logging.error("Invalid hash detected")
