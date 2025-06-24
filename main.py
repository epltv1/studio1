import os
import subprocess
from pyrogram import Client, filters
from pyrogram.types import Message
from dotenv import load_dotenv
import asyncio

# Load environment variables
load_dotenv()
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Initialize the bot
app = Client("m3u8_rtmp_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Store running ffmpeg processes
ffmpeg_processes = {}

@app.on_message(filters.command("start"))
async def start_command(client: Client, message: Message):
    await message.reply_text("Use /stream <m3u8_link> <rtmp_url> <stream_key> to start streaming.")

@app.on_message(filters.command("stream"))
async def stream_command(client: Client, message: Message):
    try:
        # Parse command: /stream <m3u8_link> <rtmp_url> <stream_key>
        args = message.text.split(maxsplit=3)[1:]
        if len(args) != 3:
            await message.reply_text("Usage: /stream <m3u8_link> <rtmp_url> <stream_key>")
            return
        m3u8_link, rtmp_url, stream_key = args

        # Validate inputs
        if not m3u8_link.endswith(".m3u8") or not rtmp_url.startswith("rtmp://"):
            await message.reply_text("Invalid M3U8 link or RTMP URL!")
            return

        # Check if a stream is already running
        chat_id = message.chat.id
        if chat_id in ffmpeg_processes:
            await message.reply_text("A stream is already running! Use /stop to end it.")
            return

        # Construct full RTMP URL
        full_rtmp_url = f"{rtmp_url}/{stream_key}"

        # ffmpeg command to stream M3U8 to RTMP
        ffmpeg_cmd = [
            "ffmpeg",
            "-i", m3u8_link,
            "-c:v", "copy",
            "-c:a", "aac",
            "-f", "flv",
            full_rtmp_url
        ]

        # Start ffmpeg process
        process = subprocess.Popen(ffmpeg_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        ffmpeg_processes[chat_id] = process

        await message.reply_text(f"Streaming {m3u8_link} to {rtmp_url}")
    except Exception as e:
        await message.reply_text(f"Error: {str(e)}")

@app.on_message(filters.command("stop"))
async def stop_command(client: Client, message: Message):
    chat_id = message.chat.id
    if chat_id not in ffmpeg_processes:
        await message.reply_text("No stream is running!")
        return

    # Stop ffmpeg process
    process = ffmpeg_processes.pop(chat_id)
    process.terminate()
    try:
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        process.kill()
    await message.reply_text("Stream stopped!")

async def main():
    await app.start()
    print("Bot is running...")
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
