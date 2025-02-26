# MP3 Splitter CLI Tool

This script allows you to split a large MP3 file into individual tracks based on timestamps provided in a tracklist text file. It provides an interactive CLI for users to specify which tracks to ignore during the splitting process and saves the resulting MP3 files to a specified output directory.

## Features

- Split a large MP3 file into individual tracks using timestamps from a tracklist.
- Optionally ignore specific tracks based on user input, including ranges of tracks (e.g., `3-6` to skip tracks 3 to 6).
- Automatically saves the split tracks to a chosen directory.
- Sanitizes track names to create valid filenames.


## Usage Case

A common use case for this tool is when you convert a YouTube video to MP3 format and want to split it into individual tracks based on timestamps. Many YouTube videos include a tracklist or timestamp information in their descriptions. This tracklist allows viewers to quickly navigate between different sections of the video.

For example, some music albums or podcasts on YouTube may have the following timestamped description:

```
00:00 Intro 
01:30 Track 1 - Song Title 
05:15 Track 2 - Song Title 
09:45 Track 3 - Song Title 
12:00 Outro
```

After downloading the video as an MP3 file, you can use this script to automatically split the MP3 file into separate tracks based on the provided timestamps. The timestamps in the description, when converted into a tracklist text file (following the format described in the **Tracklist Format** section), can be used to split the MP3 file into individual tracks.

### Example Workflow:

1. **Convert the YouTube video to MP3**: Use any YouTube-to-MP3 converter to get the audio file.
2. **Create a Tracklist**: Copy the timestamp and track names from the video description and save it in a text file (e.g., `tracklist.txt`).
3. **Run the MP3 Splitter**: Use the `split.py` script to split the MP3 file using the tracklist.

```bash
python split.py -i audio.mp3 -t tracklist.txt -o output_directory
```



## Requirements

- `pydub`: A Python package for audio manipulation.
- [`ffmpeg`](https://www.ffmpeg.org/): A multimedia framework required by pydub for handling MP3 files.

### Install Dependencies

Make sure you have `ffmpeg` installed on your system and accessible in your environment's PATH. For Python dependencies, install `pydub` using `pip`:

```bash
pip install pydub
```

## Usage

To run the script, use the following command in your terminal:

```bash
python split.py -i <input_mp3_file> -t <tracklist_file> -o <output_directory>
```

## Arguments:

- `-i`, `--input`: Path to the input MP3 file (e.g., large_file.mp3).
- `-t`, `--tracklist`: Path to the tracklist text file containing timestamps and track names (e.g., tracklist.txt).
- `-o`, `--output`: Directory where the split MP3 files will be saved (e.g., output_dir).

## Tracklist Format

The tracklist file should contain one line per track, formatted as:

```
<timestamp> <track_name>
```
    The timestamp is in the `MM:SS` format.
    The track name is a string (e.g., `Track Name A`).

Example tracklist format:
```
00:00 Track Name A
02:36 Track Name B
05:05 Track Name C
08:02 Track Name D
13:03 Track Name X
```
Example

```bash
python split.py -i large_file.mp3 -t tracklist.txt -o output
```

This command will split the `large_file.mp3` file into tracks based on the timestamps in `tracklist.txt`, and save the resulting MP3 files into the `output` directory.

## Interactive Mode

During the splitting process, you will be prompted to select which tracks you would like to ignore. You can enter the numbers of the tracks to skip or press Enter to include all tracks.

For example:
```yaml
Here is a list of all track names:
1: Track Name A
2: Track Name B
3: Track Name C
4: Track Name D
5: Track Name E
6: Track Name F
7: Track Name G
8: Track Name H
9: Track Name I

Enter the numbers of tracks to ignore (comma separated, e.g., 2,5,8 or ranges like 3-6), or press Enter to skip:
```
## Input Format for Ignoring Tracks:

- Individual tracks: Enter the track numbers separated by commas (e.g., 2,5,8).
- Ranges: Specify a range of tracks to ignore (e.g., 3-6 to skip tracks from 3 to 6).

Example input:
```
3,5,7-9
```

This will skip tracks 3, 5, and the range from 7 to 9.

## Output Files

The script will save each split track as a new MP3 file in the output directory. The filename for each track will be in the following format:
```
<track_number> - <sanitized_track_name>.mp3
```

Example:
```
01 - Track Name A.mp3
02 - Track Name B.mp3
03 - Track Name C.mp3
```
Track names are sanitized to ensure they are valid filenames by replacing any invalid characters (e.g., `<>:"/\\|?*`) with underscores.

## License

This project is licensed under the `Unlicense`. You can freely use, modify, and distribute it. For more details, please refer to [The Unlicense](./LICENSE).


