# ChatGPT Telegram Bot

Welcome to the ChatGPT Telegram Bot! This bot allows you to have a conversation with ChatGPT, a language model trained by OpenAI. ChatGPT will generate responses to your messages based on the conversation so far.

## Getting Started

### Installation

To install the ChatGPT Telegram Bot, follow these steps:

1. choose between **Official** or **Reversed** API:

    - **Official API (Browserless)**

        > *COMPLETELY FREE AND NO RATE LIMITS (Unpatched Bug - Might be fixed later)*

        Run the following command:

        for linux/macos:
        ```sh
        curl https://raw.githubusercontent.com/NicKoehler/chatgpt_telegram_bot/official-api/install.sh | sh
        ```
        for windows:
        ```powershell
        irm https://raw.githubusercontent.com/NicKoehler/chatgpt_telegram_bot/official-api/install.ps1 | iex
        ```

    - **Reversed API (Browser required)**

        > *This breaks terms of service*

        Run the following command:
            
        for linux/macos:
        ```sh
        curl https://raw.githubusercontent.com/NicKoehler/chatgpt_telegram_bot/main/install.sh | sh
        ```
        for windows:
        ```powershell
        irm https://raw.githubusercontent.com/NicKoehler/chatgpt_telegram_bot/main/install.ps1 | iex
        ```

2. Follow the prompts to complete the installation process.

### Starting the Bot

To start the ChatGPT Telegram Bot, follow these steps:

1. Navigate to the chatgpt_telegram_bot directory in your terminal:

```sh
cd chatgpt_telegram_bot
```

2. Run the start.sh script:
    - for linux/macos:
    ```sh
    ./start.sh
    ```
    - for windows:
    ```powershell
    .\start.ps1
    ```
## Using the Bot

To use the ChatGPT Telegram Bot, simply send it a message in Telegram. The bot will use ChatGPT to generate a response based on your message. You can continue the conversation by sending more messages, and the bot will use ChatGPT to generate responses based on the previous conversation.

You can rollback the conversation by sending the `/rollback` command, and you can reset the conversation by sending the `/reset` command.

You can update the bot by sending the `/update` command, and you can stop the bot by sending the `/stop` command.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome to the ChatGPT Telegram Bot! To contribute, you can fork the repository and send a pull request, or create an issue.
