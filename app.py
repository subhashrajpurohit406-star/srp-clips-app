import streamlit as st
import whisper
from moviepy.editor import VideoFileClip
import os

st.title("SRP CLIPS FOR BLOGGER")

# Upload Area
uploaded_file = st.file_uploader("Upload a video to create a clip", type=["mp4", "mov"])

if uploaded_file is not None:
    with open("temp_video.mp4", "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    st.info("AI is analyzing and cutting your clip... please wait.")
    
    # 1. AI Transcription (The Ear)
    model = whisper.load_model("base")
    result = model.transcribe("temp_video.mp4")
    
    # 2. Simple Logic: Cut the first 30 seconds
    video = VideoFileClip("temp_video.mp4")
    clip = video.subclip(0, min(30, video.duration))
    
    # 3. Crop to Vertical (The Eye)
    w, h = clip.size
    target_w = h * (9/16)
    final_clip = clip.crop(x1=(w-target_w)/2, y1=0, x2=(w+target_w)/2, y2=h)
    
    # 4. Save and Show
    final_clip.write_videofile("srp_output.mp4", codec="libx264")
    st.video("srp_output.mp4")
    st.success("Your SRP Clip is ready!")
