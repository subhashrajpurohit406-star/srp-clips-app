import streamlit as st
import yt_dlp
import whisper
import os
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip

st.set_page_config(page_title="SRP CLIPS PRO", layout="wide")

# --- SIDEBAR: PRO LICENSE ---
with st.sidebar:
    st.title("💎 PRO ACCOUNT")
    license = st.text_input("License Key", type="password")
    if st.button("Activate"):
        if license == "SRP_PRO_2026": st.success("PRO Active!")

# --- MAIN APP ---
st.title("🎬 Viral Short Generator")

# STEP 1: INPUT (YouTube or Upload)
tab1, tab2 = st.tabs(["🔗 YouTube Link", "📁 Upload Directly (Recommended)"])
video_file = None

with tab1:
    url = st.text_input("Paste YouTube Link:")
    if url and st.button("Fetch YouTube"):
        # BYPASS CONFIG 2026
        ydl_opts = {
            'format': 'best[ext=mp4]',
            'outtmpl': 'input.mp4',
            'extractor_args': {'youtube': {'player_client': ['web_embedded', 'tv']}},
        }
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl: ydl.download([url])
            video_file = "input.mp4"
        except Exception as e:
            st.error(f"YouTube Blocked the Cloud Server (403). Please use the 'Upload' tab instead.")

with tab2:
    uploaded = st.file_uploader("Upload MP4 Video", type=["mp4"])
    if uploaded:
        with open("input.mp4", "wb") as f: f.write(uploaded.getbuffer())
        video_file = "input.mp4"

# STEP 2: AI EDITING (Opus Style)
if video_file and st.button("🪄 Generate Viral Short"):
    with st.status("🛠️ AI is processing..."):
        # Transcription
        model = whisper.load_model("base")
        result = model.transcribe(video_file)
        
        # Vertical Reframe (9:16)
        clip = VideoFileClip(video_file).subclip(0, 30)
        final_clip = clip.crop(x_center=clip.w/2, width=clip.h*9/16)
        
        # Yellow Captions
        txt_clip = TextClip(result['text'][:50], fontsize=70, color='yellow', 
                           font='Arial-Bold', stroke_color='black', stroke_width=2, 
                           method='caption', size=(final_clip.w*0.8, None))
        txt_clip = txt_clip.set_pos(('center', 0.7*final_clip.h)).set_duration(30)
        
        # Final Export
        CompositeVideoClip([final_clip, txt_clip]).write_videofile("short.mp4", codec="libx264")
    
    st.video("short.mp4")
    st.download_button("Download Short", data=open("short.mp4", "rb"), file_name="viral.mp4")
