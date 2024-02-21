import hashlib
import logging
import os
import glob


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
        file_content = open(f"b{i}h{i+1}.bin", "rb").read(chunk_size + 32)
        curr_hash = hashlib.sha256(file_content).digest()
        logging.debug("Curr hash: {}\nHash  Key: {}".format(curr_hash, hash_key))

        if hash_key != curr_hash:
            return InvalidHashDetected()
        else:
            hash_key = file_content[-32:]


if __name__ == "__main__":
    decode(file_path="FLIRT_TRAINS", chunk_size=1048576)
