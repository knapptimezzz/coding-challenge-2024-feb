# Chained Hashed Example

## How to Run / Execute

* All libraries are default python libraries (no `pip install` required)
* This was developed and tested using Python `3.10`

### Encoder.py

Should be run first as without encoded files, there's nothing to decode.

#### Get help menu

```shell
python3 encoder.py -h
```

Options are:

```shell
usage: Encoder [-h] [--method METHOD] [--chunk-size CHUNK_SIZE] [--logs] filepath

Encode chunks of videos into binary files with hashes

positional arguments:
  filepath              file to chunk and hash. Please provide no spaces in the file name

options:
  -h, --help            show this help message and exit
  --method METHOD       forward-backwards or backwards-seeking
  --chunk-size CHUNK_SIZE
                        the size of chunks you want in bytes, default is 1048576
  --logs                Set logs to higher verbosity
```

For further information about methods see [Thoughts / Process](#thoughts-/-process) below

#### Encode a video file

```shell
python3 encoder.py FLIRT_TRAINS.mp4
```

### Decoder.py

#### Get help menu

```shell
python3 decoder.py -h
```

Options are:

```shell
usage: Decoder [-h] [--method METHOD] [--chunk-size CHUNK_SIZE] [--logs] filepath

Decode chunks of videos into binary files with hashes

positional arguments:
  filepath              folder path of the chunks + hashes. Please provide no spaces in the file name

options:
  -h, --help            show this help message and exit
  --chunk-size CHUNK_SIZE
                        the size of chunks you want in bytes, default is 1048576
  --logs                Set logs to higher verbosity
```

#### Encode a video file

```shell
python3 decoder.py FLIRT_TRAINS
```

Please note that the encoder will make a folder name of the same name as the file minus the extension. Please update the field if you have changed the name of the directory.

## Thoughts / Process

I had many thoughts when working on this. My first line of thinking is to actually print off the document (which you can't always do) and grab a pen and paper and start to plot out what it is that I want this code to do. I know I need to main components, `encoder.py` and `decoder.py`. So I'll start with the encoder first.

A different approach would have been to start with decoder and used it to "test" that my encoder works, but I chose differently. I started with some logic Pros / Cons. There really was two ways that I saw to do this encoding:

1. Break the file down into parts and reverse the process to get the hashes. I'll call this method "Forward / Backwards".
2. Start from the rear of the file and keep "seeking" backwards through the file seeking and hashing as I go along. I'll call this method "Backwards Seeking".

There are several pros and cons to this that I'll discuss here

### Forward / Backwards 

By doing it in two steps parse the file and then reverse backwards to hash, the file and the code is easier to read by all programmers. It might take more lines of code and added time complexity but it comes at ease of reading. 

The added time complexity could also be negated (in my opinion) as thinking at a larger system level this event always happens just once during the initial upload of a video. Having uploaded videos to YouTube, it takes a VERY long time to upload and encode and transcode the video for several formats, etc. It's a computationally intensive process that just requires time to do. However, the intent and idea is that once this process is completed, it's allows for reuse. Same goes for the chunking and hashing.

### Backwards Seeking

Now one could argue that the **whole purpose** of Kontain is that it's about how to reduce time and complexity of spinning up functions so TIME is the (most) important factor. That code complexity might be irrelevant to all other factors. If this were the case then I would also encourage some further requirements around the documentation to highlight which aspects are most important.

### Other Thoughts

* I also decided to implement both as the output to be consumed by the decoder is the same. So I decided to implement the two encoder methods the same way. `Backwards-Seeking` is more performant in terms of time space but both are relatively fast with the file sizes being small.


* I made the file sizes 1MB instead of 1KB. Seemed more reasonable when talking about video files to have a somewhat larger size, but this is just the default. Could be switched to a smaller size / configurable for that.


* I could have also set up a Flask or Django webserver to handle the process of the video requests for the `decoder.py` file but I am treating the reading of binary chunks from a folder as getting parts served to the `decoder.py` file.


* I implemented some basic logging to get messages out of the code if you wanted to compare some hashes on the command line.

## Additional Updates

After further discussion with Serge, I have decided to investigate and implement a few points of discussion we had.

### O_DIRECT

In an effort to be more efficient and reduce the amount of copying that happens under the hood through normal kernel operations, we discussed `O_DIRECT` which is a way for a file to be opened and to NOT have it cached before entering into the program memory. We discussed the components of that and how there are options in the kernel to help with this. Given that python has a lot of C under the hood, I tried to add `O_DIRECT` as a flag, which is in option in the `os.open()` [method for python](https://docs.python.org/3.10/library/os.html#os.open). I am developing on a Mac and so these methods are not available to me. However, I did some investigation and these options are not available for Mac testing. I could spin up an AWS instance and implement these changes. Additional research also puts this as an `os.open` instead of the `open()` which is a built in pything funciton. There are several differences that would require some additional changes to the code.

### Smaller Files with Writing

Additionally what we discussed is ways to keep the memory down when writing the files. It would be better to write the files out as they come in than to keep hold of all the data and write it out when ending the program like before. Therefore, much of the file output logic has been moved into the functions themselves. I still kept both functions as a way to demonstrate where my logic and thinking where at.

### Single Binary - In progress

Lastly, we discussed making a single, large file. Rather than treating the application like the chunking method, abstract that thinking away to a webserver and pretend these python scripts are on the other sides of that.