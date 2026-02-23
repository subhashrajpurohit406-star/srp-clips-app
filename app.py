import streamlit as st
from moviepy.editor import VideoFileClip
import os

st.set_page_config(page_title="SRP CLIPS AI", layout="wide")
st.title("🎬 SRP AI Viral Short Generator")

st.info("⚠️ Upload video directly. YouTube links are blocked on cloud servers.")

uploaded = st.file_uploader("Upload MP4 Video", type=["mp4"])

if uploaded:
    with open("input.mp4", "wb") as f:
        f.write(uploaded.read())

    if st.button("Generate 30s Vertical Short"):
        try:
            clip = VideoFileClip("input.mp4").subclip(0, 30)
            w, h = clip.size
            vertical = clip.crop(x_center=w/2, width=h*9/16)

            vertical.write_videofile("short.mp4", codec="libx264", audio_codec="aac")

            st.success("Short Created!")
            st.video("short.mp4")

            with open("short.mp4", "rb") as f:
                st.download_button("Download Short", f, "srp_short.mp4")

        except Exception as e:
            st.error(str(e))
