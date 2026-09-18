import streamlit as st
import requests
from bs4 import BeautifulSoup
from openai import OpenAI

# Streamlit Page Config
st.set_page_config(page_title="AI Automation Tool", page_icon="⚡")
st.title("⚡ Smart AI Web Summarizer")

# API Key Setup
api_key = st.sidebar.text_input("Enter OpenAI API Key", type="password")

# Input Form
url_input = st.text_input("Enter Web URL to Analyze:")

def extract_text_from_url(url):
    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(response.text, 'html.parser')
        paragraphs = soup.find_all('p')
        text = ' '.join([p.get_text() for p in paragraphs])
        return text[:4000] # Limiting context length
    except Exception as e:
        return f"Error: {str(e)}"

def process_with_ai(text, client):
    prompt = f"Analyze the following text and provide a concise summary, key takeaways, and action items:\n\n{text}"
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

if st.button("Run Automation"):
    if not api_key:
        st.error("Please provide an API Key!")
    elif not url_input:
        st.warning("Please enter a URL!")
    else:
        with st.spinner("Scraping content and running AI analysis..."):
            client = OpenAI(api_key=api_key)
            scraped_text = extract_text_from_url(url_input)
            
            if "Error:" in scraped_text:
                st.error(scraped_text)
            else:
                st.subheader("Extracted Content Preview")
                st.write(scraped_text[:300] + "...")
                
                result = process_with_ai(scraped_text, client)
                st.subheader("AI Analysis Result")
                st.success(result)