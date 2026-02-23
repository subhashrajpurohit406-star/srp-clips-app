from flask import Flask, render_template, request, send_file
from downloader import download_video
from processor import create_vertical_short
import os

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form.get("url")
        try:
            video = download_video(url)
            output = create_vertical_short(video)
            return render_template("index.html", video_ready=True)
        except Exception as e:
            return f"Error: {e}"
    return render_template("index.html", video_ready=False)

@app.route("/download")
def download():
    return send_file("static/output.mp4", as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
