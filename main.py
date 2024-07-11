import os

import anthropic
import streamlit as st
import whisper
import youtube_dl
import yt_dlp
from autogen import AssistantAgent, UserProxyAgent
from moviepy.audio.io.AudioFileClip import AudioFileClip

anthropic_api_key = os.getenv('API_KEY')

os.environ["AUTOGEN_USE_DOCKER"] = "no"


def download_video(url):
    ydl_opts = {
        'format': 'bestaudio[ext=webm]/best',
        'outtmpl': "audio.webm",
        'noplaylist': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    audio_clip = AudioFileClip("audio.webm")
    audio_clip.write_audiofile("audio.mp3")
    audio_clip.close()


def transcribe_audio():
    model = whisper.load_model("base")
    result = model.transcribe('audio.mp3')
    return result['text']


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


class UserAgent(UserProxyAgent):
    def __init__(self, name="UserAgent"):
        super().__init__(name=name)

    def request_summary(self, url, custom_prompt, custom_act):
        agent = YouTubeSummarizerAgent()
        agent.summarize(url, custom_prompt, custom_act)


def main():
    st.title("YouTube Video Transcription and Summarizer")

    url = st.text_input("Enter YouTube Video URL")
    custom_prompt = st.text_input("Enter custom prompt for summarization",
                                  value="Act as a researcher and provide a concise summary.")
    custom_act = st.text_input("Enter additional instructions for summarization",
                               value="Provide the summary in 5 sentences.")

    user_agent = UserAgent()

    if st.button("Run"):
        user_agent.request_summary(url, custom_prompt, custom_act)


if __name__ == "__main__":
    main()
