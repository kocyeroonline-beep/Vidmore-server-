from flask import Flask, request, jsonify
from pytube import YouTube, Search
import os

app = Flask(__name__)

@app.route("/trending", methods=["GET"])
def trending():
    # Placeholder - YouTube API yifashishwa neza, aha turakoresha fake
    results = [
        {"title": "Trending Song", "channel": "Music Channel", "time": "2h ago",
         "url": "https://youtu.be/dQw4w9WgXcQ", "thumbnail": "https://i.ytimg.com/vi/dQw4w9WgXcQ/hqdefault.jpg"},
        {"title": "Funny Shorts", "channel": "Comedy Hub", "time": "1d ago",
         "url": "https://youtu.be/dQw4w9WgXcQ", "thumbnail": "https://i.ytimg.com/vi/dQw4w9WgXcQ/hqdefault.jpg"}
    ]
    return jsonify(results)

@app.route("/search", methods=["GET"])
def search():
    query = request.args.get("q")
    s = Search(query)
    results = []
    for v in s.results[:10]:
        results.append({
            "title": v.title,
            "channel": v.author,
            "time": "N/A",
            "url": v.watch_url,
            "thumbnail": v.thumbnail_url
        })
    return jsonify(results)

@app.route("/info", methods=["GET"])
def info():
    url = request.args.get("url")
    yt = YouTube(url)
    streams = []
    for s in yt.streams.filter(progressive=True):
        streams.append({
            "itag": s.itag,
            "type": "video" if s.resolution else "audio",
            "resolution": s.resolution,
            "abr": s.abr
        })
    return jsonify({"title": yt.title, "streams": streams})

@app.route("/download", methods=["GET"])
def download():
    url = request.args.get("url")
    itag = request.args.get("itag")
    yt = YouTube(url)
    stream = yt.streams.get_by_itag(int(itag))
    file_path = stream.download(output_path="downloads")
    return jsonify({"status": "ok", "file": file_path})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
