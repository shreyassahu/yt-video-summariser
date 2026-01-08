from google import genai
from youtube_transcript_api import YouTubeTranscriptApi
from google import genai
import streamlit as st
import re

#Get the transcript from Youtube API

def get_transcript(video_id):
    ytt_api = YouTubeTranscriptApi()
    try:
        fetched_transcript = ytt_api.fetch(video_id)
        text = " ".join([t.text for t in fetched_transcript])
        return text
    except:
        return None

#Pass the content to Gemini API

def get_summary(text):
    client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=[text, "Summarise this transcript of a YT video."]
    )
    return response.text

#Extract Video ID from URL
def extract_video_id(url):
    pattern = r'(?:https?://)?(?:www\.)?(?:youtube\.com/(?:watch\?v=|embed/|v/)|youtu\.be/)([a-zA-Z0-9_-]{11})'
    match = re.search(pattern, url)
    return match.group(1) if match else None



st.title("YT Video Summariser")
yt_url = st.text_input("Enter YT Video URL")
video_id = extract_video_id(yt_url)

if video_id:
    transcript = get_transcript(video_id)
    if transcript:
        with st.spinner("Generating summary..."):
            summary = get_summary(transcript)
        st.markdown(summary)

















