import hashlib
import logging
import os
import argparse as ap
import math


def encode_backwards_seeking(file_path, chunk_size=1048576):
    """
    Take a file, the chunk size and create the hashes for the parts
    :param file_path: The path to the file
    :param chunk_size: The size of the chunks you want in bytes, default is 1MB
    :return: Nothing
    """

    # Setup known values for later computation
    chunks = math.floor(os.path.getsize(file_path) / chunk_size)
    previous_chunk = None
    directory_name = file_path[0:file_path.rfind('.')]

    try:
        os.mkdir(directory_name)
    except FileExistsError as fee:
        # Do nothing if the directory already exists
        pass

    # Open file for reading
    with open(file_path, 'rb') as video_file:
        while chunks >= 0:
            try:
                video_file.seek(chunks * chunk_size)
                chunk = video_file.read(chunk_size)
                # This is the last piece of the file
                if previous_chunk is None:
                    previous_chunk = chunk
                elif previous_chunk is not None:
                    hashed_chunk = chunk + hashlib.sha256(previous_chunk).digest()
                    previous_chunk = hashed_chunk
                else:
                    break
                open(f"{directory_name}/b{chunks}h{chunks + 1}.bin", "wb").write(previous_chunk)
                chunks -= 1
            # Do some basic error handling for now to know that something bad happened
            except Exception as e:
                logging.error('Encoding error: {}'.format(e))
        open(f"{directory_name}/h0.bin", "wb").write(hashlib.sha256(previous_chunk).digest())

    logging.debug("Hashing complete")
    return


if __name__ == "__main__":

    # Enable some arguments to be passed
    parser = ap.ArgumentParser(
        prog='Encoder',
        description='Encode chunks of videos into binary files with hashes')
    parser.add_argument('filepath', type=str,
                        help='file to chunk and hash. Please provide no spaces in the file name')
    parser.add_argument('--chunk-size', default=1048576,
                        help='the size of chunks you want in bytes, default is 1048576')
    parser.add_argument('--logs', action='store_true',
                        help='Set logs to higher verbosity')
    args = parser.parse_args()

    if args.logs:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.ERROR)

    encode_backwards_seeking(file_path=args.filepath, chunk_size=args.chunk_size)

    print("Successfully chunked and hashed file.")
