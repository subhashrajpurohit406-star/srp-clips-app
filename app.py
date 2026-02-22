import streamlit as st
import whisper
import yt_dlp
import os
import random
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip

# --- APP CONFIG ---
st.set_page_config(page_title="SRP CLIPS PRO", layout="wide")

# --- PRO SYSTEM ---
if 'is_pro' not in st.session_state: st.session_state.is_pro = False

# --- SIDEBAR ---
with st.sidebar:
    st.title("🎬 PRO SETTINGS")
    key = st.text_input("License Key", type="password")
    if st.button("Activate"):
        if key == "SRP_PRO_2026": st.session_state.is_pro = True
    st.markdown("---")
    st.write("Status:", "💎 PRO" if st.session_state.is_pro else "🆓 FREE")

# --- MAIN APP ---
st.title("🚀 Viral Clip Generator & Auto-Captions")
yt_url = st.text_input("Paste YouTube Link:")

if yt_url and st.button("Generate Pro Short"):
    video_file = "input.mp4"
    
    with st.status("🛠️ Working...", expanded=True) as status:
        # 1. FIXED DOWNLOADER (Bypass 403 Forbidden)
        st.write("📥 Downloading Video...")
        ydl_opts = {
            'format': 'best[ext=mp4]',
            'outtmpl': video_file,
            'quiet': True,
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([yt_url])
        except Exception as e:
            st.error(f"Download Error: {e}")
            st.stop()

        # 2. AI TRANSCRIPTION FOR CAPTIONS
        st.write("📝 AI generating colorful subtitles...")
        model = whisper.load_model("base")
        result = model.transcribe(video_file)
        
        # 3. VERTICAL 9:16 CROP & SUBTITLES
        clip = VideoFileClip(video_file).subclip(0, 30) # 30-second clip
        w, h = clip.size
        target_w = h * 9/16
        final_clip = clip.crop(x_center=w/2, width=target_w)

        # 4. OVERLAY SUBTITLES (Colorful & Bold)
        # Taking the first 5 words as a sample caption
        caption_text = result['text'][:50] + "..." 
        txt_clip = TextClip(caption_text, fontsize=70, color='yellow', font='Arial-Bold', 
                           stroke_color='black', stroke_width=2, method='caption', size=(target_w*0.8, None))
        txt_clip = txt_clip.set_pos(('center', h*0.7)).set_duration(final_clip.duration)
        
        video_with_subs = CompositeVideoClip([final_clip, txt_clip])
        video_with_subs.write_videofile("output_short.mp4", codec="libx264")
        
        status.update(label="Viral Short Ready!", state="complete")

    st.video("output_short.mp4")
    st.download_button("Download Viral Short", data=open("output_short.mp4", "rb"), file_name="srp_short.mp4")
