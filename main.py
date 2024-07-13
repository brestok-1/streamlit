import streamlit as st

from article import ArticleUserAgent
from podcasts import PodcastUserAgent
from youtube import YouTubeUserAgent


def init_session_state():
    if 'button1_clicked' not in st.session_state:
        st.session_state.button1_clicked = False
    if 'button2_clicked' not in st.session_state:
        st.session_state.button2_clicked = False
    if 'button3_clicked' not in st.session_state:
        st.session_state.button3_clicked = False
    if 'url' not in st.session_state:
        st.session_state.url = ""
    if 'custom_prompt' not in st.session_state:
        st.session_state.custom_prompt = "Act as a researcher and provide a concise summary."
    if 'custom_act' not in st.session_state:
        st.session_state.custom_act = "Provide the summary in 5 sentences."


def main():
    st.title("Summarizer")

    # Initialize session state
    init_session_state()

    col1, col2, col3 = st.columns(3)

    if col1.button('Youtube video summarizer', key='button1'):
        st.session_state.button1_clicked = True
        st.session_state.button2_clicked = False
        st.session_state.button3_clicked = False
    if col2.button('Article summarizer', key='button2'):
        st.session_state.button1_clicked = False
        st.session_state.button2_clicked = True
        st.session_state.button3_clicked = False
    if col3.button('Podcast Summarizer', key='button3'):
        st.session_state.button1_clicked = False
        st.session_state.button2_clicked = False
        st.session_state.button3_clicked = True

    if st.session_state.button1_clicked:
        st.session_state.url = st.text_input("Enter YouTube Video URL", value=st.session_state.url)
        st.session_state.custom_prompt = st.text_input("Enter custom prompt for summarization",
                                                       value=st.session_state.custom_prompt)
        st.session_state.custom_act = st.text_input("Enter additional instructions for summarization",
                                                    value=st.session_state.custom_act)
        user_agent = YouTubeUserAgent()
        if st.button("Run"):
            user_agent.request_summary(st.session_state.url, st.session_state.custom_prompt,
                                       st.session_state.custom_act)

    if st.session_state.button2_clicked:
        st.session_state.url = st.text_input("Enter Article URL", value=st.session_state.url)
        st.session_state.custom_prompt = st.text_input("Enter custom prompt for summarization",
                                                       value=st.session_state.custom_prompt)
        st.session_state.custom_act = st.text_input("Enter additional instructions for summarization",
                                                    value=st.session_state.custom_act)
        user_agent = ArticleUserAgent()
        if st.button("Run"):
            user_agent.request_summary(st.session_state.url, st.session_state.custom_prompt,
                                       st.session_state.custom_act)

    if st.session_state.button3_clicked:
        st.session_state.url = st.text_input('Enter Podcast URL', value=st.session_state.url)
        st.session_state.custom_prompt = st.text_input("Enter custom prompt for summarization",
                                                       value=st.session_state.custom_prompt)
        st.session_state.custom_act = st.text_input("Enter additional instructions for summarization",
                                                    value=st.session_state.custom_act)
        user_agent = PodcastUserAgent()
        if st.button("Run"):
            user_agent.request_summary(st.session_state.url, st.session_state.custom_prompt,
                                       st.session_state.custom_act)


if __name__ == "__main__":
    main()
