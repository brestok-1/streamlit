import os

import anthropic
import streamlit as st
import yt_dlp
from autogen import AssistantAgent, UserProxyAgent
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

anthropic_api_key = os.getenv('API_KEY')

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))


def download_video(url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': "audio"
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


def transcribe_audio():
    audio_file = open('audio.mp3', 'rb')
    transcription = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file
    )
    return transcription.text


def summarize_text(text, custom_prompt, custom_act):
    client = anthropic.Client(api_key=anthropic_api_key)
    prompt = (
        f"Please summarize the following text. {custom_prompt} {custom_act}\n\n"
        f"{text}\n\n"
    )
    response = client.completions.create(
        prompt=f"\n\nHuman: {prompt}\n\nAssistant:",
        model="claude-v1",
        temperature=1.0,
        max_tokens_to_sample=150,
        stop_sequences=["\n\nHuman:"],
        top_k=40,
        top_p=0.9
    )
    return response.completion.strip()


class YouTubeSummarizerAgent(AssistantAgent):
    def __init__(self, name="YouTubeSummarizer"):
        super().__init__(name=name)

    def summarize(self, url, custom_prompt, custom_act):
        st.write("Downloading video...")
        download_video(url)
        st.write("Transcribing video...")
        transcription = transcribe_audio()
        st.text_area("Transcription", transcription, height=300, key="transcription")
        st.write("Summarizing transcription...")
        summary = summarize_text(transcription, custom_prompt, custom_act)
        st.text_area("Summary", summary, height=150, key="summary")


class YouTubeUserAgent(UserProxyAgent):
    def __init__(self, name="UserAgent"):
        super().__init__(name=name)

    def request_summary(self, url, custom_prompt, custom_act):
        agent = YouTubeSummarizerAgent()
        agent.summarize(url, custom_prompt, custom_act)
