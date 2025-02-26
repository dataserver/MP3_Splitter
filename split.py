"""
MP3 Splitter CLI Tool

This script splits a large MP3 file into individual tracks based on timestamps provided in a tracklist text file.
The user can specify which tracks to ignore. The script saves the resulting split tracks to a specified output directory.

Usage:
    python split.py -i <input_mp3_file> -t <tracklist_file> -o <output_directory>

Arguments:
    -i, --input      Path to the large MP3 input file (e.g., "large_file.mp3").
    -t, --tracklist  Path to the tracklist text file containing timestamps and track names (e.g., "tracklist.txt").
    -o, --output     Path to the directory where the split tracks will be saved (e.g., "output_dir").

Tracklist Format:
    The tracklist file should contain one line per track with the timestamp and track name:
    <timestamp> <track_name>
    For example:
        00:00 Track Name A
        02:36 Track Name B
        05:05 Track Name C
        08:02 Track Name D

    Each timestamp is in the format MM:SS, indicating the start time of each track.

Example:
    python split.py -i large_file.mp3 -t tracklist.txt -o output

Requirements:
    - pydub (https://pydub.com/)
    - ffmpeg (required by pydub for MP3 file handling)
"""

import argparse
import os
import re
from pathlib import Path

from pydub import AudioSegment

# Set the FFmpeg binary path (optional)
# os.environ["FFMPEG_BINARY"] = (
#     r"D:\python\mp3_spliter\bin\ffmpeg.exe"  # Adjust for Windows
# )


# Function to convert time string (MM:SS) to milliseconds
def time_to_ms(time_str: str) -> int:
    minutes, seconds = map(int, time_str.split(":"))
    return (minutes * 60 + seconds) * 1000  # Convert to milliseconds


# Function to read the timestamps and track names from the text file
def read_timestamps(file_path: Path) -> list[tuple[str, str]]:
    timestamps = []
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            for line in file:
                parts = line.strip().split(maxsplit=1)
                if len(parts) == 2:
                    timestamp, track_name = parts
                    timestamps.append((timestamp, track_name))
    except UnicodeDecodeError:
        print("UnicodeDecodeError encountered. Trying ISO-8859-1 encoding...")
        with open(file_path, "r", encoding="ISO-8859-1") as file:
            for line in file:
                parts = line.strip().split(maxsplit=1)
                if len(parts) == 2:
                    timestamp, track_name = parts
                    timestamps.append((timestamp, track_name))
    return timestamps


# Function to sanitize track names to be valid filenames
def sanitize_filename(track_name: str) -> str:
    sanitized = re.sub(r'[<>:"/\\|?*]', "_", track_name)
    return sanitized


# Function to prompt user to select which tracks to ignore
def prompt_ignore_tracks(timestamps: list[tuple[str, str]]) -> list[int]:
    print("Here is a list of all track names:")
    for i, (_, track_name) in enumerate(timestamps, 1):
        print(f"{i}: {track_name}")

    ignore_input = input(
        "Enter the numbers of tracks to ignore (comma separated, e.g., 2,5,8 or ranges like 3-6), or press Enter to skip: "
    )

    ignore_indices = []
    if ignore_input.strip():
        parts = ignore_input.split(",")
        for part in parts:
            part = part.strip()
            if "-" in part:
                # Handle ranges like 3-6
                try:
                    start, end = map(int, part.split("-"))
                    if start <= end:
                        ignore_indices.extend(
                            range(start - 1, end)
                        )  # Make it zero-indexed
                except ValueError:
                    print(f"Invalid range format: {part}")
            elif part.isdigit():
                ignore_indices.append(int(part) - 1)  # Make it zero-indexed


# Function to split the mp3 file based on timestamps from the text file
def split_mp3(
    mp3_path: Path,
    timestamps: list[tuple[str, str]],
    output_folder: Path,
    ignore_indices: list[int],
):
    audio = AudioSegment.from_mp3(mp3_path)

    output_folder.mkdir(parents=True, exist_ok=True)

    total_duration_ms = len(audio)

    track_number_padding = 2 if len(timestamps) <= 99 else 3

    previous_timestamp_ms = 0
    for i, (timestamp, track_name) in enumerate(timestamps):
        if i in ignore_indices:
            print(f"Skipping {track_name}.")
            continue

        timestamp_ms = time_to_ms(timestamp)

        if i + 1 == len(timestamps):
            end_timestamp_ms = total_duration_ms
        else:
            end_timestamp_ms = time_to_ms(timestamps[i + 1][0])

        segment = audio[previous_timestamp_ms:end_timestamp_ms]

        track_number = str(i + 1).zfill(track_number_padding)
        sanitized_track_name = sanitize_filename(track_name)
        output_file = output_folder / f"{track_number} - {sanitized_track_name}.mp3"

        segment.export(output_file, format="mp3")

        previous_timestamp_ms = timestamp_ms
        print(f"Saved {track_number} - {sanitized_track_name}.mp3")

    print("Splitting complete.")


# Main function with argument parsing using argparse
if __name__ == "__main__":
    # Set up the argument parser
    parser = argparse.ArgumentParser(
        description="Split a large MP3 file into tracks based on a tracklist."
    )
    parser.add_argument(
        "-i", "--input", required=True, help="Path to the large MP3 input file."
    )
    parser.add_argument(
        "-t", "--tracklist", required=True, help="Path to the tracklist text file."
    )
    parser.add_argument(
        "-o", "--output", required=True, help="Directory to save the split tracks."
    )

    # Parse the arguments
    args = parser.parse_args()

    # Convert input paths to Path objects
    mp3_path = Path(args.input)
    timestamps_file = Path(args.tracklist)
    output_folder = Path(args.output)

    # Read the timestamps and track names from the text file
    timestamps = read_timestamps(timestamps_file)

    # Prompt the user to select which tracks to ignore
    ignore_indices = prompt_ignore_tracks(timestamps)

    # Split the MP3 based on the timestamps and the ignore list
    split_mp3(mp3_path, timestamps, output_folder, ignore_indices)
