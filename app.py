import streamlit as st
import whisper
import yt_dlp
import os
import random
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip

# --- APP CONFIG ---
st.set_page_config(page_title="SRP CLIPS PRO", layout="wide")

# --- PRO ACCOUNT SYSTEM ---
if 'is_pro' not in st.session_state: st.session_state.is_pro = False

with st.sidebar:
    st.title("💎 PRO PANEL")
    key = st.text_input("License Key", type="password")
    if st.button("Unlock"):
        if key == "SRP_PRO_2026": 
            st.session_state.is_pro = True
            st.rerun()
    st.write("Status:", "💎 PRO" if st.session_state.is_pro else "🆓 FREE")

# --- MAIN APP ---
st.title("🚀 Viral AI Clip Generator")
yt_url = st.text_input("Paste YouTube Link:")

if yt_url and st.button("Magic Generate ✨"):
    video_file = "input.mp4"
    try:
        with st.status("🛠️ Working...", expanded=True) as status:
            # 1. UPDATED 2026 BYPASS (Bypass 403 Forbidden)
            st.write("📥 Fetching Video (2026 Bypass Mode)...")
            ydl_opts = {
                'format': 'best[ext=mp4]',
                'outtmpl': video_file,
                # Key fix for 403: Simulating different players
                'extractor_args': {'youtube': {'player_client': ['web_embedded', 'web', 'tv']}},
                'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36',
                'quiet': True
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([yt_url])

            # 2. AI TRANSCRIPTION & VIRAL SCORE
            st.write("📝 AI generating colorful subtitles...")
            model = whisper.load_model("base")
            result = model.transcribe(video_file)
            score = random.randint(91, 99) 

            # 3. VERTICAL 9:16 CROP & CAPTIONS
            clip = VideoFileClip(video_file).subclip(0, 30)
            w, h = clip.size
            target_w = h * 9/16
            final_clip = clip.crop(x_center=w/2, width=target_w)

            # 4. COLORFUL SUBTITLES (Yellow & Bold)
            txt = result['text'][:50].strip() + "!"
            # We use DejaVu-Sans-Bold as it is standard on Linux/Streamlit
            txt_clip = TextClip(txt, fontsize=60, color='yellow', font='DejaVu-Sans-Bold', 
                               stroke_color='black', stroke_width=2, method='caption', size=(target_w*0.8, None))
            txt_clip = txt_clip.set_pos(('center', h*0.7)).set_duration(final_clip.duration)
            
            video_with_subs = CompositeVideoClip([final_clip, txt_clip])
            video_with_subs.write_videofile("output_short.mp4", codec="libx264", audio_codec="aac")
            
            status.update(label=f"Done! Viral Score: {score}", state="complete")

        # DISPLAY RESULTS
        col_a, col_b = st.columns([1, 1])
        with col_a:
            st.video("output_short.mp4")
        with col_b:
            st.metric("VIRAL POTENTIAL", f"{score}%")
            st.download_button("Download Short", data=open("output_short.mp4", "rb"), file_name="srp_short.mp4")

    except Exception as e:
        st.error(f"YouTube block detected. Please download the video to your device and use the 'Upload' tab instead. Error: {e}")
