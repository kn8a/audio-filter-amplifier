import os
import sys
from pydub import AudioSegment

# Set the path to the local ffmpeg executable
FFMPEG_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "ffmpeg", "bin"))
FFMPEG_PATH = os.path.join(FFMPEG_DIR, "ffmpeg.exe")
FFPROBE_PATH = os.path.join(FFMPEG_DIR, "ffprobe.exe")

def check_ffmpeg():
    return os.path.exists(FFMPEG_PATH) and os.path.exists(FFPROBE_PATH)

def install_ffmpeg():
    print("ffmpeg executables not found in the expected location.")
    print("Please ensure the ffmpeg folder is in the same directory as this script.")
    print("The folder structure should be:")
    print("- Your script directory")
    print("  - ffmpeg")
    print("    - bin")
    print("      - ffmpeg.exe")
    print("      - ffprobe.exe")
    sys.exit(1)

# Check for ffmpeg
if not check_ffmpeg():
    install_ffmpeg()

# Add ffmpeg to the system PATH
os.environ["PATH"] += os.pathsep + FFMPEG_DIR

# Directories for input and output
input_dir = "input"
output_dir = "output"

# Load the audio file
input_filename = os.path.join(input_dir, "Voice03.m4a")  # Change to your input file name
output_wav_filename = os.path.join(output_dir, "loud_parts_amplified.wav")

# Load the audio file using pydub
audio = AudioSegment.from_file(input_filename, format="m4a")

# Define a decibel threshold for audio segments to keep
threshold_db = -30  # Threshold in decibels (above this will be saved)

# Initialize an empty audio segment for the output
output_audio = AudioSegment.empty()

# Loop through the audio in chunks to check the dB level
chunk_size = 1000  # Size of each chunk in milliseconds
for start in range(0, len(audio), chunk_size):
    end = start + chunk_size
    segment = audio[start:end]
    
    # Check if the segment's average dB is above the threshold
    if segment.dBFS > threshold_db:
        # Amplify the segment by 10 dB
        amplified_segment = segment + 10  # Increase volume by 10 dB
        output_audio += amplified_segment

# Check if any segments were added
if len(output_audio) == 0:
    print("No audio above threshold detected; no audio was added.")
else:
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Export the amplified segments to the output directory
    output_audio.export(output_wav_filename, format="wav")
    print(f"WAV file saved to {output_wav_filename}")