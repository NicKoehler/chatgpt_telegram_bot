powershell -Command {

    function command_exist($command) {
        if (!(Get-Command $command -ErrorAction SilentlyContinue)) {
            Write-Output "Install '$command' and run again."
            exit 1
        }
    }

    command_exist git
    command_exist python

    git clone https://github.com/nickoehler/chatgpt_telegram_bot.git

    cd chatgpt_telegram_bot
    python -m venv venv
    .\venv\Scripts\pip install -r requirements.txt

    Clear-Host

    Write-Output "Dependencies installed."
    Write-Output ""

    $owner_id = Read-Host "Enter your Telegram ID > "
    $telegram_token = Read-Host "Enter your Telegram Bot Token > "
    $openai_token = Read-Host "Enter your OpenAI Session Token > "

    New-Item -ItemType File -Path ".env" -Force | Out-Null
    Add-Content -Path ".env" -Value "OWNER_ID=$owner_id"
    Add-Content -Path ".env" -Value "TELEGRAM_BOT_TOKEN=$telegram_token"
    Add-Content -Path ".env" -Value "OPENAI_SESSION_TOKEN=$openai_token"

    Write-Output "Installation complete."
    Write-Output "Enter the chatgpt_telegram_bot folder and run 'start.ps1' to start the bot."

    exit 0
}
