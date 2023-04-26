import sys
import os
import yt_dlp
import requests
import json
import openai
from pydub import AudioSegment
from dotenv import load_dotenv

load_dotenv()


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def get_video_audio(youtube_url, output_file):
    ydl_opts = {
        "format": "bestaudio/best",
        "quiet": True,
        "no_warnings": True,
        "outtmpl": output_file
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtube_url])

def split_audio_to_segments(input_file, duration=10*60*1000):
    audio = AudioSegment.from_file(input_file)
    segments = []
    start_time = 0
    while start_time < len(audio):
        end_time = start_time + duration
        segment = audio[start_time:end_time]
        segments.append(segment)
        start_time += duration
    return segments

def transcribe_audio_segment(segment, file_format="mp3"):
    with open("temp_segment.mp3", "wb") as f:
        segment.export(f, format=file_format)

    with open("temp_segment.mp3", "rb") as f:
        transcript = openai.Audio.transcribe("whisper-1", f)

    os.remove("temp_segment.mp3")
    return transcript["text"]

def main():
    if len(sys.argv) != 2:
        print("Usage: python youtube_transcribe.py [youtube_url]")
        return

    youtube_url = sys.argv[1]
    output_file = "audio_output.mp3"
    get_video_audio(youtube_url, output_file)

    openai.api_key = OPENAI_API_KEY

    segments = split_audio_to_segments(output_file)
    os.remove(output_file)

    transcript = ""
    for segment in segments:
        segment_transcript = transcribe_audio_segment(segment)
        transcript += segment_transcript + "\\n"

    print(transcript)

if __name__ == "__main__":
    main()
