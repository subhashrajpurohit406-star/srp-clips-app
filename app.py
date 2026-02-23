import streamlit as st
import yt_dlp
from moviepy.editor import VideoFileClip
import os

st.set_page_config(page_title="SRP CLIPS AI", layout="wide")
st.title("🎬 SRP AI Viral Short Generator")

def download_video(url):
    ydl_opts = {
        'format': 'best[ext=mp4]',
        'outtmpl': 'input.mp4',
        'quiet': True
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    return "input.mp4"

option = st.radio("Choose Input:", ["YouTube Link", "Upload Video"])
video_file = None

if option == "YouTube Link":
    url = st.text_input("Paste YouTube URL")
    if url and st.button("Download"):
        video_file = download_video(url)

else:
    uploaded = st.file_uploader("Upload MP4", type=["mp4"])
    if uploaded:
        with open("input.mp4", "wb") as f:
            f.write(uploaded.read())
        video_file = "input.mp4"

if video_file and st.button("Generate 30s Vertical Short"):
    clip = VideoFileClip(video_file).subclip(0, 30)
    w, h = clip.size
    vertical = clip.crop(x_center=w/2, width=h*9/16)
    vertical.write_videofile("short.mp4", codec="libx264")

    st.success("Done!")
    st.video("short.mp4")

    with open("short.mp4", "rb") as f:
        st.download_button("Download Short", f, "srp_short.mp4")
