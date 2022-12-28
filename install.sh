#!/bin/bash

command_exist() {
    if ! command -v $1 &> /dev/null
    then
        echo "Install '$1' and run again."
        exit
    fi
}

command_exist git
command_exist python3

git clone https://github.com/nickoehler/chatgpt_telegram_bot.git

cd chatgpt_telegram_bot
python3 -m venv venv
./venv/bin/pip3 install -r requirements.txt

clear

echo -e "Dependencies installed.\n"

read -p "Enter your Telegram ID > " owner_id
read -p "Enter your Telegram Bot Token > " telegram_token
read -p "Enter your OpenAI Session Token > " openai_token

echo "OWNER_ID=$owner_id" >> .env
echo "TELEGRAM_BOT_TOKEN=$telegram_token" >> .env
echo "OPENAI_SESSION_TOKEN=$openai_token" >> .env

echo "./venv/bin/python3 src/bot.py" > start.sh
chmod +x start.sh

echo "Installation complete."
echo "Run 'start.sh' to start the bot."

exit 0
