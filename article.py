import os

import anthropic
import requests
import streamlit as st
from bs4 import BeautifulSoup
from dotenv import load_dotenv

anthropic_api_key = os.getenv("API_KEY")

load_dotenv()


def scrape_article(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    paragraphs = soup.find_all('p')
    article_text = '\n'.join([para.get_text() for para in paragraphs])
    return article_text


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


class ArticleSummarizerAgent:
    def summarize(self, url, custom_prompt, custom_act):
        st.write("Scraping article...")
        article_text = scrape_article(url)
        st.success('Article scraped successfully!')

        st.text_area("Article Text", article_text, height=300, key="article_text")

        st.write("Summarizing article...")
        summary = summarize_text(article_text, custom_prompt, custom_act)
        st.text_area("Summary", summary, height=150, key="summary")


class ArticleUserAgent:
    def request_summary(self, url, custom_prompt, custom_act):
        agent = ArticleSummarizerAgent()
        agent.summarize(url, custom_prompt, custom_act)
