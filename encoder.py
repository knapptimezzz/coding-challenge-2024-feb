import hashlib
import logging
import os
import sys
import argparse as ap


def encode_forward_backwards(file_path, chunk_size=1048576):
    """
    Take a file, the chunk size and create the hashes for the parts
    :param file_path: The path to the file
    :param chunk_size: The size of the chunks you want in bytes, default is 1MB
    :return: H0 and an array of binary chunks with hashes B0||H1, B1||H2, etc.
    """

    # Setup known values for later computation
    hashed_binaries = []

    # Open file for reading
    with open(file_path, 'rb') as video_file:

        while True:
            # Read until the final b'' indicator
            try:
                chunk = video_file.read(chunk_size)
                if chunk != b'':
                    hashed_binaries.append(chunk)
                else:
                    break
            # Do some basic error handling for now to know that something bad happened
            except Exception as e:
                logging.error('Encoding error: {}'.format(e))

    # Encode / hash the chunks
    for i in range(len(hashed_binaries) - 2, -1, -1):
        hashed_binaries[i] = hashed_binaries[i] + hashlib.sha256(hashed_binaries[i + 1]).digest()
        # Some error checking that the sha256 didn't add extra bytes, etc.
        if len(hashed_binaries[i]) != chunk_size + 32:
            logging.error('Chunk size is off!')

    logging.debug("Encoding complete. Encoded chunks: {}".format(hashed_binaries))

    return hashlib.sha256(hashed_binaries[0]).digest(), hashed_binaries


if __name__ == "__main__":

    # Enable some arguments to be passed
    parser = ap.ArgumentParser(
        prog='Encoder',
        description='Encode chunks of videos into binary files with hashes')
    parser.add_argument('filepath', type=str,
                        help='file to chunk and hash. Please provide no spaces in the file name')
    parser.add_argument('--method', default="forward-backwards",
                        help='forward-backwards or backwards-seeking')
    parser.add_argument('--chunk-size', default=1048576,
                        help='the size of chunks you want in bytes, default is 1048576')
    parser.add_argument('--logs', action='store_true',
                        help='Set logs to higher verbosity')
    args = parser.parse_args()

    if args.logs:
        logging.basicConfig(level=logging.ERROR)
    else:
        logging.basicConfig(level=logging.NOTSET)

    h0, hashed_results = None, None
    directory_name = args.filepath[0:args.filepath.rfind('.')]

    if args.method == "forward-backwards":
        h0, hashed_results = encode_forward_backwards(file_path=args.filepath, chunk_size=args.chunk_size)
    elif args.method == "backwards-seeking":
        pass
    try:
        os.mkdir(directory_name)
    except FileExistsError as fee:
        # Do nothing if the directory already exists
        pass
    # Change to the directory
    os.chdir(directory_name)

    # Write out the binary files
    open("h0.bin", "wb").write(h0)
    for i in range(0, len(hashed_results)):
        open(f"b{i}h{i+1}.bin", "wb").write(hashed_results[i])

    print("Successfully chunked and hashed file.")
