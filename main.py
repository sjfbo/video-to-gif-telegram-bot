import logging
import os
import urllib.request
from pathlib import Path
from urllib.error import HTTPError, URLError

import telegram
from dotenv import load_dotenv
from flask import Flask, request, Response
from moviepy.editor import VideoFileClip
from telegram.ext import Updater, MessageHandler, Filters

env_path = Path(__file__).parent / '.env'
load_dotenv(env_path, override=True)

BOT_TOKEN = os.getenv('BOT_TOKEN')
WEBHOST = os.getenv('WEBHOST')

storage_path = 'downloads'

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)
logger = logging.getLogger(__name__)

# init app
app = Flask(__name__)
bot = telegram.Bot(token=BOT_TOKEN)


@app.route('/', methods=['GET'])
def index():
    return Response('', status=200)


# hook endpoint
@app.route('/webhook/' + BOT_TOKEN, methods=['POST', 'GET'])
def webhook_handler():
    if request.method == "POST":
        update = telegram.Update.de_json(request.get_json(force=True), bot)
        dispatcher.process_update(update)
    return Response('OK', status=200)


@app.route('/set_webhook', methods=['GET', 'POST'])
def set_webhook():
    s = updater.bot.setWebhook(url=WEBHOST + '/webhook/' + BOT_TOKEN)
    if s:
        return 'WebHook was set'

    return 'WebHook setup failed'


def get_video_id_from_message(message):
    return message.video.file_id


def save_video(chat_id, video_id):
    video_path = "{0}/{1}.mp4".format(storage_path, video_id)
    gif_path = "{0}/{1}.gif".format(storage_path, video_id)
    video_url = bot.get_file(video_id).file_path

    if not os.path.exists(storage_path):
        os.makedirs(storage_path)

    if not video_url:
        return

    try:
        bot.send_message(chat_id=chat_id,
                         text="🤖 Beep boop, please be patient. I'm working on it.")
        urllib.request.urlretrieve(video_url, video_path)
        clip = VideoFileClip(video_path).resize(0.8)
        clip.write_gif(gif_path, fps=15, program='ffmpeg')
    except IOError as e:
        logger.error(e)
    except (HTTPError, URLError) as e:
        logger.error(e)

    return gif_path


def cleanup_files(video_id):
    for f in Path(storage_path).glob("{0}.*".format(video_id)):
        f.unlink()


def media_handler(update, __):
    message = update.message
    chat_id = update.message.chat_id
    video_id = get_video_id_from_message(message)

    gif_to_send = save_video(chat_id, video_id)
    bot.send_animation(chat_id, animation=open(gif_to_send, 'rb'), caption='Voila')
    cleanup_files(video_id)


updater = Updater(BOT_TOKEN, use_context=True)
dispatcher = updater.dispatcher

dispatcher.add_handler(MessageHandler(Filters.video, media_handler))

if __name__ == '__main__':
    app.run(debug=True)
