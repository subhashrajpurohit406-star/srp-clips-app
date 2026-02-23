from moviepy.editor import VideoFileClip
import os

def create_vertical_short(path, duration=30):
    clip = VideoFileClip(path).subclip(0, duration)
    w, h = clip.size

    vertical = clip.crop(x_center=w/2, width=h*9/16)

    output = "static/output.mp4"

    vertical.write_videofile(
        output,
        codec="libx264",
        audio_codec="aac",
        threads=4,
        preset="medium"
    )

    return output
