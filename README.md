# Audio Loudness Filter and Amplifier

This Python program processes audio files by detecting segments with significant energy in a specific frequency range and decibel level, amplifies those segments, and exports them as a new .wav file. The program supports .m4a, .mp3, and .wav input files.

## Features

- Detects audio segments based on a decibel threshold and specified frequency range.
- Amplifies the detected segments by a user-defined decibel amount.
- Exports the processed audio as a .wav file.
- Displays progress bars for reading and processing files.

## Prerequisites

- Python 3.x
- pydub for handling audio files.
- scipy for Fast Fourier Transform (FFT) calculations.
- numpy for numerical operations.
- tqdm for progress bars.
- ffmpeg for handling .m4a and .mp3 files.


## Installation

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd <repository-name>
2. Install the requirements:

 ```bash
pip install pydub numpy librosa
```

2.1 Download and set up ffmpeg:
Download ffmpeg from [here](https://ffmpeg.org/download.html).
Place the ffmpeg folder in the same directory as this script.
Ensure the folder structure is as follows:
```markdown
- Your script directory
  - ffmpeg
    - bin
      - ffmpeg.exe
      - ffprobe.exe
```

## Usage

3. Place your input audio file in the input directory. (You can rename it as Voice02.m4a or change the script to reflect your filename.)

4. Adjust the threshold_db variable in the script to set your desired dB threshold.

5. Run the script:

 ```bash
python audioCleaner_hz.py
```

or if you only need to filter by db, run:

 ```bash
python audioCleaner.py
```

6. The output audio file with amplified segments will be saved in the output directory as loud_parts_amplified.wav.

## Configuration
Threshold Level: You can adjust the loudness threshold by changing the threshold_db variable in the script. The default is set to -20 dB.

Amplification Level: The segments are amplified by 10 dB. This value can be modified in the line amplified_segment = segment + 10.

## License
This project is licensed under the MIT License - see the LICENSE file for details.
