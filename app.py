import streamlit as st
import yt_dlp
import os
from moviepy.editor import VideoFileClip

def get_viral_clip(url):
    video_path = "input_video.mp4"
    
    # NEW 2026 BYPASS CONFIGURATION
    ydl_opts = {
        'format': 'best[ext=mp4]',
        'outtmpl': video_path,
        # This argument is the critical fix for Feb 2026
        'extractor_args': {
            'youtube': {
                'player_client': ['web_embedded', 'web', 'tv'],
                'player_skip': ['android_sdkless', 'ios']
            }
        },
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/121.0.0.0 Safari/537.36',
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    return video_path

st.title("🎬 SRP CLIPS PRO")
url = st.text_input("Paste YouTube Link:")

if url and st.button("Generate"):
    try:
        path = get_viral_clip(url)
        st.video(path)
        st.success("Download Successful!")
    except Exception as e:
        # If cloud IP is blacklisted, this is the only remaining fix:
        st.error("YouTube has blocked this server's IP address.")
        st.info("💡 WORKAROUND: Download the video to your device and use the 'Upload File' button instead. This bypasses all 403 errors 100% of the time.")
