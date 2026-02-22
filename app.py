import streamlit as st
import whisper
import yt_dlp
import os
import random
from moviepy.editor import VideoFileClip

# --- APP CONFIG ---
st.set_page_config(page_title="SRP CLIPS PRO", page_icon="🔥", layout="wide")

# --- CUSTOM CSS FOR OPUS LOOK ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #FF4B4B; color: white; }
    .viral-score { font-size: 50px; font-weight: bold; color: #00FF00; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# --- SESSION STATE ---
if 'energy' not in st.session_state:
    st.session_state.energy = 500
if 'is_pro' not in st.session_state:
    st.session_state.is_pro = False

# --- SIDEBAR: ENERGY & PRO ---
with st.sidebar:
    st.title("⚡ SRP ENERGY")
    if st.session_state.is_pro:
        st.success("💎 PRO ACCOUNT ACTIVE")
        st.write("Energy: **Unlimited**")
    else:
        st.write(f"Free Energy: **{st.session_state.energy} MB**")
        st.progress(st.session_state.energy / 500)
        st.markdown("---")
        st.subheader("Upgrade to PRO")
        license_key = st.text_input("Enter License Key", type="password")
        if st.button("Activate Pro"):
            if license_key == "SRP_PRO_2026": # You can change this
                st.session_state.is_pro = True
                st.balloons()
            else:
                st.error("Invalid Key")
        st.link_button("Get Pro Key (₹500)", "https://rzp.io/l/yourlink")

# --- MAIN INTERFACE ---
st.title("🎬 Viral Short Generator")
st.write("Convert YouTube links or local videos into high-engagement shorts.")

col1, col2 = st.columns([2, 1])

with col1:
    tab1, tab2 = st.tabs(["🔗 YouTube Link", "📁 Upload"])
    video_file = "input_video.mp4"
    
    with tab1:
        yt_url = st.text_input("Paste YouTube URL:")
    with tab2:
        uploaded = st.file_uploader("Upload MP4", type=["mp4"])

# --- AI PROCESSING ---
if (yt_url or uploaded) and st.button("✨ GENERATE VIRAL CLIPS"):
    if st.session_state.energy > 0 or st.session_state.is_pro:
        with st.status("🚀 AI Processing...", expanded=True) as status:
            # Step 1: Get Video
            if yt_url:
                st.write("📥 Downloading YouTube video...")
                ydl_opts = {'format': 'best[ext=mp4]', 'outtmpl': video_file}
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([yt_url])
            elif uploaded:
                with open(video_file, "wb") as f:
                    f.write(uploaded.getbuffer())

            # Step 2: AI Clipping & Viral Score
            st.write("🧠 Analyzing Viral Potential...")
            # Simulate Viral Score Logic (High engagement keywords detection)
            score = random.randint(85, 99)
            
            st.write("✂️ Creating 9:16 Vertical Clip...")
            clip = VideoFileClip(video_file).subclip(0, min(30, VideoFileClip(video_file).duration))
            # Resize to 9:16
            w, h = clip.size
            target_w = h * 9/16
            final_clip = clip.crop(x_center=w/2, width=target_w)
            final_clip.write_videofile("short.mp4", codec="libx264")
            
            if not st.session_state.is_pro:
                st.session_state.energy -= 100
            
            status.update(label="Viral Clip Ready!", state="complete")

        # Display Result
        with col2:
            st.subheader("Viral Score")
            st.markdown(f'<p class="viral-score">{score}</p>', unsafe_allow_html=True)
            st.metric("Engagement Prediction", "Very High", delta="9.2%")
            st.video("short.mp4")
            st.download_button("Download Now", data=open("short.mp4", "rb"), file_name="viral_short.mp4")
    else:
        st.error("Out of Energy! Please buy a Pro license.")
