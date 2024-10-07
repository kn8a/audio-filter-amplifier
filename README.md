# Audio Loudness Filter and Amplifier

This Python program processes audio files to extract and amplify segments that exceed a specified loudness threshold. It uses `pydub` for audio manipulation and requires `ffmpeg` for audio format handling.

## Features

- Extracts audio segments that exceed a defined dB threshold.
- Amplifies the extracted segments by a specified dB level.
- Supports multiple audio formats (via ffmpeg).
- Simple and straightforward usage.

## Prerequisites

Before running the script, ensure you have the following installed:

- Python 3.x
- [ffmpeg](https://ffmpeg.org/download.html) (Ensure the `ffmpeg` folder is in the same directory as the script with the correct structure)


## Installation

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd <repository-name>
Install the required Python packages:

 ```bash
pip install pydub numpy librosa
Usage
```
Place your input audio file in the input directory. (You can rename it as Voice02.m4a or change the script to reflect your filename.)

Adjust the threshold_db variable in the script to set your desired dB threshold.

Run the script:

 ```bash
python audio_loudness_filter.py
```
The output audio file with amplified segments will be saved in the output directory as loud_parts_amplified.wav.

Configuration
Threshold Level: You can adjust the loudness threshold by changing the threshold_db variable in the script. The default is set to -20 dB.

Amplification Level: The segments are amplified by 10 dB. This value can be modified in the line amplified_segment = segment + 10.

License
This project is licensed under the MIT License - see the LICENSE file for details.
