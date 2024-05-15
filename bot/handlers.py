import json
import pytz
import datetime
from utils.common import escape_special_chars
from telegram import Update
from telegram.ext import CallbackContext


async def paul(update: Update, context: CallbackContext):
    """Funktion zum Verarbeiten von Telegram-Nachrichten und Interaktion mit dem Kalender-Tool"""
    calendar_tool_instance = context.application.bot_data['calendar_tool_instance']
    model = context.application.bot_data['model']
    chat_id = update.effective_chat.id

    if 'message_history' not in context.chat_data:
        context.chat_data['message_history'] = [
            Content(
                role='user',
                parts=[Part.from_text(
                    f"Du bist Paul. Ein freundlicher, deutschsprachiger, ChatBot der mir hilft meinen Google Calendar zu managen. Du gibst detaillierte und übersichtlich formatierte Antworten. Du stellst sicher stehts nur mit einem Part pro Content object zu antworten. Ich werde meine zukünftigen Nachrichten mit der aktuellen dateTime, sowie Zeitzone beginnen auf welche sich meine Anfragen beziehen."
                    """
                    Du kannst folgende Syntax zur Formatierung verwenden:
                    *text* für fetten Text.
                    _text_ für kursiven Text.

                    Achte darauf NUR diese Syntax zu verwenden und keine anderen Versuche zu unternehmen. Kombiniere NICHT mehrere Formatierungen miteinander.
                    """
                )]
            ),
            Content(
                role='model',
                parts=[Part.from_text(
                    f"Sehr gerne! 😊\nWenn ich dir helfen soll, gib mir eine Aufgabe oder frage mich etwas zu deinem Kalender. 📅 Ich werde dann Anhand deiner Angaben die konketen Daten selbstständig ermitteln.\nWenn du möchtest, können wir uns auch einfach unterhalten! 💬")]
            )
        ]

    def extract_text(update):
        """Extrahiert den Text aus der Nachricht oder ihren Antworten/Weiterleitungen"""
        if update.message.text and not update.message.text.startswith('/paul'):
            return update.message.text
        elif update.message.reply_to_message and update.message.reply_to_message.text:
            return update.message.reply_to_message.text
        return None

    def clean_message_history(messages):
        """Bereinigt die Nachrichtenhistorie, um Duplikate zu entfernen"""
        seen_messages = set()
        unique_messages = []
        for message in messages:
            message_text = "".join(part.text for part in message.parts)
            if message_text not in seen_messages:
                seen_messages.add(message_text)
                unique_messages.append(message)

        cleaned_messages = []
        last_role = None
        for message in unique_messages:
            if message.role != last_role:
                cleaned_messages.append(message)
                last_role = message.role

        return cleaned_messages

    user_text = extract_text(update)

    if not user_text:
        await context.bot.send_message(chat_id=chat_id, text="Please provide some input for the calendar assistant.")
        return

    utc_time = update.message.date
    berlin_tz = pytz.timezone('Europe/Berlin')
    berlin_time = utc_time.astimezone(berlin_tz)
    timestamp = berlin_time.strftime('%Y-%m-%d %H:%M:%S')

    chat = model.start_chat(history=clean_message_history(context.chat_data['message_history']))
    context.chat_data['message_history'].append(
        Content(role='user',
                parts=[Part.from_text(f"[Aktueller Timestamp: {timestamp}; Zeitzone: Europe/Berlin] {user_text}")])
    )

    try:
        if user_text and user_text.lower().startswith('/paul'):
            text = user_text[5:].strip()
            response = chat.send_message([Part.from_text(f"[{timestamp}:Europe/Berlin] {text}")])
            if hasattr(response.candidates[0].content, "text"):
                escaped_text = escape_special_chars(response.candidates[0].content.text)
                await context.bot.send_message(chat_id=chat_id, text=escaped_text, parse_mode="MarkdownV2")
                context.chat_data['message_history'].append(
                    Content(role='model', parts=[Part.from_text(response.candidates[0].content.text)])
                )

            if response.candidates[0].function_calls:
                for function_call in response.candidates[0].function_calls:
                    if hasattr(calendar_tool_instance, function_call.name):
                        func = getattr(calendar_tool_instance, function_call.name)
                        function_response = func(**function_call.args)
                        try:
                            response = chat.send_message(
                                Part.from_text(json.dumps(function_response)))
                            if hasattr(response.candidates[0].content, "text"):
                                escaped_text = escape_special_chars(response.candidates[0].content.text)
                                await context.bot.send_message(chat_id=chat_id, text=escaped_text,
                                                               parse_mode="MarkdownV2")
                                context.chat_data['message_history'].append(
                                    Content(role='model', parts=[Part.from_text(response.candidates[0].content.text)])
                                )
                        except ResourceExhausted as e:
                            await context.bot.send_message(chat_id=chat_id,
                                                           text="Quota exceeded. Please wait a minute and try again.")
    except ResourceExhausted as e:
        await context.bot.send_message(chat_id=chat_id, text="Quota exceeded. Please wait a minute and try again.")
