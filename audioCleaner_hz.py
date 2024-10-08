import os
import sys
import numpy as np
from pydub import AudioSegment
from scipy.fft import rfft, rfftfreq
from tqdm import tqdm  # Progress bar
import io
import warnings

# Set the path to the local ffmpeg executable
FFMPEG_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "ffmpeg", "bin"))
FFMPEG_PATH = os.path.join(FFMPEG_DIR, "ffmpeg.exe")
FFPROBE_PATH = os.path.join(FFMPEG_DIR, "ffprobe.exe")

# Add ffmpeg to the system PATH
os.environ["PATH"] += os.pathsep + FFMPEG_DIR

# Directories for input and output
input_dir = "input"
output_dir = "output"

# List files in the input directory
def list_input_files(directory):
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    if not files:
        print(f"No files found in {directory}")
        sys.exit(1)
    return files

# Allow the user to choose a file from the list
def choose_input_file():
    files = list_input_files(input_dir)
    print("Select a file to process:")
    for idx, file in enumerate(files, start=1):
        print(f"{idx}. {file}")
    
    # Input validation loop
    while True:
        try:
            choice = int(input("Enter the number of the file to process: ")) - 1
            if 0 <= choice < len(files):
                return files[choice]
            else:
                print("Invalid choice. Please enter a valid number.")
        except ValueError:
            print("Invalid input. Please enter a number.")

# Choose file from input directory
input_filename = os.path.join(input_dir, choose_input_file())

# Load the audio file using pydub and manually update the progress bar
audio = None
with open(input_filename, "rb") as f:
    audio_bytes = f.read()
    
# Create audio segment from bytes after reading
audio = AudioSegment.from_file(io.BytesIO(audio_bytes), format="m4a")

# Define a decibel threshold for audio segments to keep
threshold_db = -30  # Threshold in decibels (above this will be saved)

# Frequency range to check for
lowcut = 800.0  # Low cutoff frequency
highcut = 6000.0  # High cutoff frequency
fs = audio.frame_rate  # Sample rate from the audio segment

# Initialize an empty audio segment for the output
output_audio = AudioSegment.empty()

# Function to check if a segment contains significant energy in a frequency range
def contains_frequencies(segment, lowcut, highcut, threshold_db):
    # Convert segment to numpy array for FFT
    samples = np.array(segment.get_array_of_samples())
    
    # Compute the FFT
    N = len(samples)
    yf = rfft(samples)
    xf = rfftfreq(N, 1 / fs)

    # Compute the magnitude of the FFT
    magnitude = np.abs(yf)

    # Find indices for the frequency range
    low_index = np.searchsorted(xf, lowcut)
    high_index = np.searchsorted(xf, highcut)

    # Calculate the total energy in the specified frequency range
    total_energy_in_range = np.sum(magnitude[low_index:high_index])
    
    # Calculate total energy in the segment
    total_energy = np.sum(magnitude)

    # Check if the energy in the specified frequency range is above a certain percentage of the total energy
    if total_energy > 0 and (total_energy_in_range / total_energy) > 0.1:  # 10% threshold
        return True
    return False

# Loop through the audio in chunks to check the dB level and frequency content
chunk_size = 1000  # Size of each chunk in milliseconds
total_chunks = len(audio) // chunk_size

# Check if any segments were added
if len(output_audio) == 0:
    print("No audio above threshold detected; no audio was added.")
else:
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Export the amplified segments to the output directory
    output_wav_filename = os.path.join(output_dir, f"amplified_{os.path.basename(input_filename)}.wav")
    output_audio.export(output_wav_filename, format="wav")
    print(f"WAV file saved to {output_wav_filename}")