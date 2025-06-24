# Telegram M3U8 to RTMP Bot

A Telegram bot that streams M3U8 links to RTMP destinations using the `/stream <m3u8_link> <rtmp_url> <stream_key>` command.

## Setup
1. Clone the repository: `git clone https://github.com/yourusername/telegram-m3u8-rtmp-bot.git`
2. Install dependencies: `pip install -r requirements.txt`
3. Install ffmpeg: `sudo apt install ffmpeg` (Linux) or equivalent.
4. Create a `.env` file with `API_ID`, `API_HASH`, and `BOT_TOKEN`.
5. Run the bot: `python main.py`

## Commands
- `/start`: Displays welcome message.
- `/stream <m3u8_link> <rtmp_url> <stream_key>`: Streams an M3U8 link to an RTMP destination.
- `/stop`: Stops the current stream.

## Deployment
Deployed on Pella.app (ensure ffmpeg is installed on the host).
