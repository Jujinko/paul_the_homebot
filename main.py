import json

from telegram.ext import Application, CommandHandler
from vertexai.preview.generative_models import GenerativeModel, ToolConfig

from google_calendar.api import GoogleCalendarAPI
from google_calendar.tool import CalendarTool, initialize_vertex_ai, define_tool
from bot.handlers import paul

# Configurations from config.json
with open('config.json') as config_file:
    config = json.load(config_file)

def list_calendars_and_generate_token():
    """Listet alle Kalender-IDs auf und erzeugt das Token."""
    calendar_api = GoogleCalendarAPI(config['calendar_id'])
    calendar_api.list()


def start_bot():
    print("Starting Bot...")
    """Startet den Telegram-Bot."""
    project_id = config['project_id']
    location = config['location']
    calendar_id = config['calendar_id']

    initialize_vertex_ai(project_id, location)

    allowed_functions = ["get_calendar_events", "get_events_for_date_range", "add_calendar_event",
                         "delete_calendar_event"]

    calendar_tool_instance = CalendarTool(calendar_id)
    calendar_tool = define_tool()
    tool_config = ToolConfig(
        function_calling_config=ToolConfig.FunctionCallingConfig(
            mode=ToolConfig.FunctionCallingConfig.Mode.ANY,
            allowed_function_names=allowed_functions,
        ))
    model = GenerativeModel(model_name="gemini-1.5-pro-preview-0514", tools=[calendar_tool], tool_config=tool_config)

    TOKEN = config['telegram_token']
    application = Application.builder().token(TOKEN).build()

    application.bot_data['model'] = model
    application.bot_data['calendar_tool_instance'] = calendar_tool_instance

    paul_handler = CommandHandler('paul', paul)
    application.add_handler(paul_handler)

    application.run_polling()

def main():
    """Hauptfunktion zum Starten des Bots"""
    list_calendars_and_generate_token()
    if config['calendar_id'] == "primary":
        print("Token erzeugt und Kalender-IDs ausgegeben. Bitte aktualisiere die config.json mit der gewünschten Kalender-ID und starte das Skript erneut.")
    else:
        start_bot()

if __name__ == "__main__":
    main()