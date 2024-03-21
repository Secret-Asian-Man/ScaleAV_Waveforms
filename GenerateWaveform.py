from pytube import YouTube
from pydub import AudioSegment
from pytube import extract
import argparse
import os
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

matplotlib.use('TkAgg')

# Create an argument parser
parser = argparse.ArgumentParser(description='Get YouTube video transcript')

# Add the arguments to the parser
parser.add_argument('-u', '--url', required=True, help='Input YouTube video URL')

# Parse the command line arguments
args = parser.parse_args()

url = args.url
video_id = None

if "youtube.com" in url:
  video_id = extract.video_id(url)
else:
  video_id = url
  url = f"https://www.youtube.com/watch?v={url}"

print(f"Downloading {url}...")
yt = YouTube(url)
title = yt.title

# Process title
title = title.replace(" ", "")
title = title.replace(".", "-")

# Download YouTube video
stream = yt.streams.filter(only_audio=True).first()
stream.download(filename='tempAudio.mp4')

# Convert to mp3
print("Converting to mp3...")
audio = AudioSegment.from_file('tempAudio.mp4')
audio.export('tempAudio.mp3', format='mp3')

# Load audio file
audio = AudioSegment.from_mp3('tempAudio.mp3')
data = np.array(audio.get_array_of_samples())

# Generate waveform
print("Generating waveform...")
time = np.arange(0, len(data)) / audio.frame_rate

# Resize the figure based on the video duration
plt.figure(figsize=(50, 2))

# Plot the waveform
plt.plot(time, data)
plt.xlabel('Time (seconds)')
plt.ylabel('Amplitude')

waveform_dir = "waveforms"
if not os.path.exists(waveform_dir):
  os.makedirs(waveform_dir)

# Save waveform
plt.savefig(f'{waveform_dir}/{title}_waveform.png')
print(f"Waveform saved to {waveform_dir}/{title}_waveform.png")

# Clean up
os.remove('tempAudio.mp4')
os.remove('tempAudio.mp3')

plt.show()