import datetime
import json

import vertexai
from vertexai.preview.generative_models import GenerativeModel, Tool, ToolConfig, FunctionDeclaration
from google_calendar.api import GoogleCalendarAPI
import json_examples

def initialize_vertex_ai(project_id, location):
    """Initialisiert Vertex AI mit dem gegebenen Projekt-ID und Standort"""
    vertexai.init(project=project_id, location=location)

def define_tool():
    """Definiert die Tool-Funktionalitäten für das Modell"""
    get_calendar_events_func = FunctionDeclaration(
        name="get_calendar_events",
        description="Fetch Google Calendar events for a specified date",
        parameters={
            "type": "object",
            "properties": {
                "date": {"type": "string",
                         "description": "The date for which to fetch calendar events in YYYY-MM-DD format."}
            },
            "required": ["date"]
        },
    )

    get_events_for_date_range_func = FunctionDeclaration(
        name="get_events_for_date_range",
        description="Fetch Google Calendar events for a specified date range",
        parameters={
            "type": "object",
            "properties": {
                "start_date": {"type": "string",
                               "description": "The start date for fetching calendar events in YYYY-MM-DD format."},
                "end_date": {"type": "string",
                             "description": "The end date for fetching calendar events in YYYY-MM-DD format."}
            },
            "required": ["start_date", "end_date"]
        },
    )

    add_calendar_event_func = FunctionDeclaration(
        name="add_calendar_event",
        description="Add a new event to Google Calendar",
        parameters={
            "type": "object",
            "properties": {
                "event": {
                    "type": "string",
                    "description": "The event details json string with required keys 'start' and 'end' and the following structure: " +
                                   json_examples.json_structure,
                    "required": ["summary", "start", "end"]
                }
            },
            "required": ["event"]
        },
    )

    delete_calendar_event_func = FunctionDeclaration(
        name="delete_calendar_event",
        description="Delete an event from Google Calendar",
        parameters={
            "type": "object",
            "properties": {
                "event_id": {"type": "string", "description": "The ID of the event to delete."}
            },
            "required": ["event_id"]
        },
    )

    return Tool(function_declarations=[
        get_calendar_events_func,
        get_events_for_date_range_func,
        add_calendar_event_func,
        delete_calendar_event_func
    ])

class CalendarTool:
    def __init__(self, calendar_id):
        self.api = GoogleCalendarAPI(calendar_id)

    def get_events_for_date_range(self, start_date, end_date):
        """Holt Ereignisse für einen bestimmten Datumsbereich"""
        try:
            start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
            end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()
            events = self.api.fetch_events(start_date, end_date)
            return events
        except Exception as e:
            return {"error": f"Failed to fetch events: {str(e)}"}

    def get_calendar_events(self, date):
        """Holt Ereignisse für ein bestimmtes Datum"""
        try:
            start_date = end_date = datetime.datetime.strptime(date, "%Y-%m-%d").date() if date.lower() != "today" else datetime.date.today()
            events = self.api.fetch_events(start_date, end_date)
            return events
        except Exception as e:
            return {"error": f"Failed to fetch events for date {date}: {str(e)}"}

    def add_calendar_event(self, event):
        """Fügt ein Ereignis zum Kalender hinzu"""
        try:
            return self.api.add_event(json.loads(event))
        except json.JSONDecodeError:
            return {"error": "Invalid JSON format"}
        except Exception as e:
            return {"error": f"Failed to add event: {str(e)}"}

    def delete_calendar_event(self, event_id):
        """Löscht ein Ereignis aus dem Kalender"""
        try:
            self.api.delete_event(event_id)
            return {"event_id": event_id, "status": "deleted"}
        except Exception as e:
            return {"error": f"Failed to delete event with ID {event_id}: {str(e)}"}
