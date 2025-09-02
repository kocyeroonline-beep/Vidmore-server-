from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from pytube import YouTube, Search
import os

app = Flask(__name__)
CORS(app)  # 🔑 kugirango app ya Kivy ibone data

@app.route("/")
def home():
    return {"message": "Vidmore API Running ✅"}

@app.route("/search")
def search():
    query = request.args.get("q")
    if not query:
        return jsonify([])
    s = Search(query)
    results = []
    for video in s.results[:10]:  # 10 za mbere
        results.append({
            "title": video.title,
            "url": video.watch_url,
            "thumbnail": f"https://img.youtube.com/vi/{video.video_id}/0.jpg"
        })
    return jsonify(results)

@app.route("/info")
def info():
    url = request.args.get("url")
    if not url:
        return jsonify([])
    yt = YouTube(url)
    streams = []
    for s in yt.streams.filter(progressive=True, file_extension="mp4"):
        streams.append({
            "itag": s.itag,
            "resolution": s.resolution,
            "type": "video",
            "filesize": s.filesize
        })
    for s in yt.streams.filter(only_audio=True):
        streams.append({
            "itag": s.itag,
            "abr": s.abr,
            "type": "audio",
            "filesize": s.filesize
        })
    return jsonify(streams)

@app.route("/download")
def download():
    url = request.args.get("url")
    itag = request.args.get("itag")
    yt = YouTube(url)
    stream = yt.streams.get_by_itag(itag)
    out_file = stream.download(output_path="downloads")
    return send_file(out_file, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
