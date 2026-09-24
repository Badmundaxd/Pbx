import os
from pydub import AudioSegment
from pydub.effects import speedup

from . import HelpMenu, on_message, Pbxbot


# ─────────────────────────────────────────────
#  HELPER — download & send audio, then cleanup
# ─────────────────────────────────────────────
async def _process_audio(client, message, effect_fn, output_name: str):
    """Download replied audio, apply effect_fn, send result, clean up."""
    reply = message.reply_to_message

    if not reply or not reply.audio:
        return await message.reply_text(
            f"Please reply to an audio file to use .{output_name}!"
        )

    status = await message.reply_text("⏳ Processing audio...")

    try:
        audio_path = await client.download_media(reply.audio.file_id)
        output_path = effect_fn(audio_path)
        await message.reply_audio(audio=output_path)
    except Exception as e:
        await message.reply_text(f"❌ Failed to process audio: `{e}`")
    finally:
        await status.delete()
        for path in (audio_path, output_path):
            try:
                os.remove(path)
            except Exception:
                pass


# ─────────────────────────────────────────────
#  EFFECTS
# ─────────────────────────────────────────────
def _bass_boost(audio_path: str) -> str:
    """Heavy low-end boost."""
    audio = AudioSegment.from_file(audio_path)
    result = audio.low_pass_filter(100).high_pass_filter(30).apply_gain(10)
    out = "_bass_out.mp3"
    result.export(out, format="mp3")
    return out


def _dj_boost(audio_path: str) -> str:
    """Loud volume / DJ boost."""
    audio = AudioSegment.from_file(audio_path)
    result = audio.low_pass_filter(250).high_pass_filter(100).apply_gain(40)
    out = "_dj_out.mp3"
    result.export(out, format="mp3")
    return out


def _nightcore(audio_path: str) -> str:
    """Speed up + pitch raise (nightcore effect)."""
    audio = AudioSegment.from_file(audio_path)
    # Speed up by 1.25x; pydub speedup keeps pitch close to original rate
    result = speedup(audio, playback_speed=1.25)
    out = "_nightcore_out.mp3"
    result.export(out, format="mp3")
    return out


def _bass_slowed(audio_path: str) -> str:
    """Bass boost + slowed reverb combo effect."""
    audio = AudioSegment.from_file(audio_path)
    # Step 1: Apply bass boost
    bass = audio.low_pass_filter(100).high_pass_filter(30).apply_gain(10)
    # Step 2: Slow it down to 0.85x
    slowed = bass._spawn(
        bass.raw_data,
        overrides={"frame_rate": int(bass.frame_rate * 0.85)}
    ).set_frame_rate(bass.frame_rate)
    out = "_bass_slowed_out.mp3"
    slowed.export(out, format="mp3")
    return out


def _slowed(audio_path: str) -> str:
    """Slow down audio for a lofi / slowed-reverb feel."""
    audio = AudioSegment.from_file(audio_path)
    # Slow to 0.85x by stretching sample width manually via frame rate trick
    slow = audio._spawn(
        audio.raw_data,
        overrides={"frame_rate": int(audio.frame_rate * 0.85)}
    ).set_frame_rate(audio.frame_rate)
    out = "_slowed_out.mp3"
    slow.export(out, format="mp3")
    return out


# ─────────────────────────────────────────────
#  COMMANDS
# ─────────────────────────────────────────────
@on_message("bass", allow_stan=True, Bad_user=True)
async def bass_cmd(client, message):
    await _process_audio(client, message, _bass_boost, "bass")


@on_message("dj", allow_stan=True, Bad_user=True)
async def dj_cmd(client, message):
    await _process_audio(client, message, _dj_boost, "dj")


@on_message("nightcore", allow_stan=True, Bad_user=True)
async def nightcore_cmd(client, message):
    await _process_audio(client, message, _nightcore, "nightcore")


@on_message("bassslowed", allow_stan=True, Bad_user=True)
async def bassslowed_cmd(client, message):
    await _process_audio(client, message, _bass_slowed, "bassslowed")


@on_message("slowed", allow_stan=True, Bad_user=True)
async def slowed_cmd(client, message):
    await _process_audio(client, message, _slowed, "slowed")


# ─────────────────────────────────────────────
#  HELP MENU
# ─────────────────────────────────────────────
HelpMenu("audiofx").add(
    "bass",
    "<reply to audio>",
    "Apply a heavy bass boost effect to the replied audio!",
    "bass",
).add(
    "dj",
    "<reply to audio>",
    "Apply a loud DJ volume boost to the replied audio!",
    "dj",
).add(
    "bassslowed",
    "<reply to audio>",
    "Apply bass boost + slowed reverb combo — deep & chill vibes!",
    "bassslowed",
).add(
    "nightcore",
    "<reply to audio>",
    "Speed up the audio with a nightcore effect!",
    "nightcore",
).add(
    "slowed",
    "<reply to audio>",
    "Slow down the audio for a lofi / slowed-reverb vibe!",
    "slowed",
).info(
    "Reply to any audio file with these commands 🎧"
).done()
