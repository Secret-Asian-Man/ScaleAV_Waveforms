from pytube import YouTube
from pydub import AudioSegment
from pytube import extract
import argparse
import os
import numpy as np
import matplotlib.pyplot as plt

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

video = YouTube(url)
rawTitle = title = video.title

# Process title
title = title.replace(" ", "")
title = title.replace(".", "-")

# Download YouTube video
yt = YouTube(url)  # replace with your YouTube video URL
stream = yt.streams.filter(only_audio=True).first()
stream.download(filename='tempAudio.mp4')

# Convert to mp3
audio = AudioSegment.from_file('tempAudio.mp4')
audio.export('tempAudio.mp3', format='mp3')

# Load audio file
audio = AudioSegment.from_mp3('tempAudio.mp3')
data = np.array(audio.get_array_of_samples())

# Generate waveform
plt.figure(figsize=(20, 10))
plt.plot(data)
plt.show()


# Create the "waveforms" directory if it doesn't exist
# waveformDir = 'waveforms'
# if not os.path.exists(waveformDir):
#   os.makedirs(waveformDir)