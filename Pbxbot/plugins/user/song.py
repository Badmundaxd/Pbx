import os
import time
import requests
import subprocess
from pyrogram.types import Message
from youtube_search import YoutubeSearch  

from Pbxbot.core import ENV
from Pbxbot.functions.paste import post_to_telegraph
from Pbxbot.functions.tools import progress
from . import HelpMenu, Symbols, db, Pbxbot, on_message

API_URL = "http://18.136.212.47:5050/api/yt-audio-video"
API_KEY = "92fde40dc5cf563dd64cd6ba74af2361a0009ad3c386232caae9d5e53feca57f"
HEADERS = {"X-API-Key": API_KEY, "Content-Type": "application/json"}


def search_youtube(query):
    results = YoutubeSearch(query, max_results=1).to_dict()
    if not results:
        return None
    return f"https://www.youtube.com/watch?v={results[0]['id']}"


async def download_stream(url, path):
    """Stream ko download karne ka helper"""
    with requests.get(url, stream=True) as r:
        if r.status_code != 200:
            return False
        with open(path, "wb") as f:
            for chunk in r.iter_content(1024):
                f.write(chunk)
    return True


@on_message("song", allow_stan=True, Bad_user=True)
async def dwlSong(_, message: Message):
    if len(message.command) < 2:
        return await Pbxbot.delete(message, "Provide a song name to download.")

    query = await Pbxbot.input(message)
    Pbx = await Pbxbot.edit(message, f"🔎 __Searching Song__ `{query}`...")

    yt_url = search_youtube(query)
    if not yt_url:
        return await Pbxbot.delete(Pbx, "No YouTube results found.")

    # API request
    payload = {"url": yt_url, "quality": "audio"}
    response = requests.post(API_URL, json=payload, headers=HEADERS)
    data = response.json()

    audio_url = data.get("audio_stream_url")
    if not audio_url:
        return await Pbxbot.delete(Pbx, "Audio URL not found in API response.")

    title = data.get("title", "Unknown")[:50]
    duration = data.get("duration", "Unknown")
    views = data.get("views", "Unknown")
    thumbnail = data.get("thumbnail", "")

    # Thumbnail
    thumb_path = f"{title}.jpg"
    try:
        resp = requests.get(thumbnail)
        with open(thumb_path, "wb") as f:
            f.write(resp.content)
    except:
        thumb_path = None

    # Audio
    audio_path = f"{title}.mp3"
    success = await download_stream(audio_url, audio_path)
    if not success:
        return await Pbxbot.delete(Pbx, "Failed to download audio.")

    # Upload
    upload_text = f"**⬆️ Uploading Song ...** \n\n**🎵 Title:** `{title}`\n**⌛ Duration:** `{duration}`"
    await Pbx.edit(upload_text)
    start_time = time.time()
    await message.reply_audio(
        audio_path,
        caption=f"**🎧 Title:** {title} \n**👀 Views:** `{views}` \n**⌛ Duration:** `{duration}`",
        performer="[ᴛʜᴇ ᴘʙx 4.0]",
        title=title,
        thumb=thumb_path,
        progress=progress,
        progress_args=(Pbx, start_time, upload_text),
    )

    await Pbx.delete()
    os.remove(audio_path)
    if thumb_path:
        os.remove(thumb_path)


@on_message("video", allow_stan=True, Bad_user=True)
async def dwlVideo(_, message: Message):
    if len(message.command) < 2:
        return await Pbxbot.delete(message, "Provide a song name to download.")

    query = await Pbxbot.input(message)
    Pbx = await Pbxbot.edit(message, f"🔎 __Searching Video Song__ `{query}`...")

    yt_url = search_youtube(query)
    if not yt_url:
        return await Pbxbot.delete(Pbx, "No YouTube results found.")

    # Step 1: Try API
    payload = {"url": yt_url, "quality": "video"}
    try:
        response = requests.post(API_URL, json=payload, headers=HEADERS)
        data = response.json()
        video_url = data.get("video_stream_url")
        audio_url = data.get("audio_stream_url")
        title = data.get("title", "Unknown")[:50]
        duration = data.get("duration", "Unknown")
        views = data.get("views", "Unknown")
        thumbnail = data.get("thumbnail", "")
    except:
        video_url = audio_url = None

    # Step 2: If API fails, fallback to ffmpeg HLS
    if not video_url or not audio_url:
        title = yt_url.split("v=")[-1]
        duration = "Unknown"
        views = "Unknown"
        thumbnail = None
        video_url = f"{yt_url}"  # direct URL
        audio_url = None  # HLS se ffmpeg extract karega

        final_path = f"{title}.mp4"
        cmd = [
            "ffmpeg", "-y",
            "-i", yt_url,
            "-c:v", "copy",
            "-c:a", "aac",
            "-t", "300",  # first 5 minutes
            final_path
        ]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        await message.reply_video(final_path, caption=f"**🎥 Title:** {title}", progress=progress, progress_args=(Pbx, time.time(), "Uploading..."))
        await Pbx.delete()
        if os.path.exists(final_path):
            os.remove(final_path)
        return

    # Step 3: Normal download + merge
    thumb_path = f"{title}.jpg"
    try:
        resp = requests.get(thumbnail)
        with open(thumb_path, "wb") as f:
            f.write(resp.content)
    except:
        thumb_path = None

    video_path_raw = f"{title}_raw.mp4"
    audio_path_raw = f"{title}_audio.mp4"

    success_v = await download_stream(video_url, video_path_raw)
    success_a = await download_stream(audio_url, audio_path_raw)
    if not (success_v and success_a):
        return await Pbxbot.delete(Pbx, "Failed to download video/audio streams.")

    final_path = f"{title}.mp4"
    subprocess.run([
        "ffmpeg", "-y",
        "-i", video_path_raw,
        "-i", audio_path_raw,
        "-c:v", "copy",
        "-c:a", "aac",
        "-shortest",
        final_path
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    upload_text = f"**⬆️ Uploading Video Song ...** \n\n**🎥 Title:** `{title}`\n**⌛ Duration:** `{duration}`"
    await Pbx.edit(upload_text)
    start_time = time.time()

    await message.reply_video(
        final_path,
        caption=f"**🎧 Title:** {title} \n**👀 Views:** `{views}` \n**⌛ Duration:** `{duration}`",
        thumb=thumb_path,
        progress=progress,
        progress_args=(Pbx, start_time, upload_text),
    )

    await Pbx.delete()
    for path in [video_path_raw, audio_path_raw, final_path, thumb_path]:
        if path and os.path.exists(path):
            os.remove(path)

@on_message("lyrics", allow_stan=True, Bad_user=True)
async def getlyrics(_, message: Message):
    if len(message.command) < 2:
        return await Pbxbot.delete(message, "Provide a song name to fetch lyrics.")

    api = await db.get_env(ENV.lyrics_api)
    if not api:
        return await Pbxbot.delete(message, "Lyrics API not found.")

    query = await Pbxbot.input(message)
    if "-" in query:
        artist, song = query.split("-")
    else:
        artist, song = "", query

    Pbx = await Pbxbot.edit(message, f"🔎 __Lyrics Song__ `{query}`...")

    genius = Genius(
        api,
        verbose=False,
        remove_section_headers=True,
        skip_non_songs=True,
        excluded_terms=["(Remix)", "(Live)"],
    )

    song = genius.search_song(song, artist)
    if not song:
        return await Pbxbot.delete(Pbx, "No results found.")

    title = song.full_title
    image = song.song_art_image_url
    artist = song.artist
    lyrics = song.lyrics

    outStr = f"<b>{Symbols.anchor} Title:</b> <code>{title}</code>\n<b>{Symbols.anchor} Artist:</b> <code>{artist}</code>\n\n<code>{lyrics}</code>"
    try:
        await Pbx.edit(outStr, disable_web_page_preview=True)
    except MessageTooLong:
        content = f"<img src='{image}'/>\n\n{outStr}"
        url = post_to_telegraph(title, content)
        await Pbx.edit(
            f"**{Symbols.anchor} Title:** `{title}`\n**{Symbols.anchor} Artist:** `{artist}`\n\n**{Symbols.anchor} Lyrics:** [Click Here]({url})",
            disable_web_page_preview=True,
        )


HelpMenu("songs").add(
    "song",
    "<song name>",
    "Download the given audio song from YouTube!",
    "song believer",
).add(
    "video",
    "<song name>",
    "Download the given video song from YouTube!",
    "video believer",
).add(
    "lyrics",
    "<song name>",
    "Get the lyrics of the given song! Give artist name after - to get accurate results.",
    "lyrics believer - imagine dragons",
    "Need to setup Lyrics API key from https://genius.com/developers",
).info(
    "Song and Lyrics"
).done()
