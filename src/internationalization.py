_strings = {
    "en": {
        "start": (
            "Hi, this is ChatGPT Bot here are the supported commands:\n\n"
            "/start · Send this message\n"
            "/reset · Reset the conversation\n"
            "/rollback · Take the conversation back one message.\n"
            "/update · Updates the bot from github\n"
            "/stop · Stop the bot"
        ),
        "rollback_ok": "Conversation carried back one message",
        "rollback_fail": "You are already at the beginning of the conversation",
        "reset": "Conversation has been reset",
        "empty": "Empty message",
        "stop": "Bye 👋",
        "update_load": "Updating..",
        "update_done": "Updated, restarting..",
    },
    "it": {
        "start": (
            "Ciao, sono ChatGPT Bot ecco i comandi supportati:\n\n"
            "/start · Invia questo messaggio\n"
            "/reset · Resetta la conversazione\n"
            "/rollback · Porta la conversazione indietro di un messaggio\n"
            "/update · Aggiorna il bot da github\n"
            "/stop · Ferma il bot"
        ),
        "rollback_ok": "Conversazione riportata indietro di un messaggio",
        "rollback_fail": "Sei già all'inizio della conversazione",
        "reset": "Conversazione resettata",
        "empty": "Messaggio vuoto",
        "stop": "Arrivederci 👋",
        "update_load": "Aggiornamento in corso..",
        "update_done": "Aggiornato, riavvio in corso..",
    },
}


def get_translation(string: str, lang_code: str):
    # fallback to english
    if lang_code not in _strings:
        lang_code = "en"
    return _strings[lang_code][string]
