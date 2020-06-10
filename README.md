# 🤖📼 GIFMAKER: A Video to GIF Telegram Bot

## 💻 Installation

***Note:** the project has been only tested on Python `3.8`. Feel free to submit a PR to fix any issues.*

* Get your hands on `pipenv` if it's not already the case:
`pip install pipenv`

* Clone the git repository on your machine:
`git clone https://github.com/sjfbo/video-to-gif-telegram-bot`

* Create your virtual environment and install the dependencies: `pipenv install`

* Activate it and play with the project: `pipenv shell`

The application requires two environment variables:
* `BOT_TOKEN` the token that Telegram gave you when you created your bot instance through [Botfather](https://core.telegram.org/bots#6-botfather).
* `WEB_HOST` the URL of the server hosting your application.

The webserver running the bot and offering the route for the webhook might run over HTTPS as it is a requirement from Telegram. A practical way to easily play with the bot on your local is to use [ngrok](https://ngrok.com/) and run it in parallel with your application. 

On your local machine, the port on which `ngrok` should be launched is the one on which your application is listening to, by default for Flask it's the port `5000`: `./ngrok http 5000`.

Once `ngrok` configured and launched, get the `HTTPS` URL provided in the output of the previous command. Set it as the value of the `WEB_HOST` environment variable and that's it.

## 🐛 Contributing

Feel free to report issues and submit patches. Thank you!