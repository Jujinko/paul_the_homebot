import os
import datetime
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/calendar']


class GoogleCalendarAPI:
    def __init__(self, calendar_id):
        self.creds = None
        self.authenticate()
        self.calendar_id = calendar_id

    def list(self):
        """Listet alle Kalender-IDs auf"""
        calendar_list = self.get_service().calendarList().list().execute()
        for calendar in calendar_list['items']:
            print(f"Calendar Summary: {calendar['summary']}, Calendar ID: {calendar['id']}")

    def authenticate(self):
        """Authentifiziert den Benutzer und holt die notwendigen Anmeldeinformationen"""
        print("Google Creds Authentication...")
        if os.path.exists('credentials.json'):
            print("credentials.json found")
            if os.path.exists('token.json'):
                print("token.json found")
                creds = Credentials.from_authorized_user_file('token.json', SCOPES)
            else:
                print("token.json not found")
                print("requesting auth flow from credentials.json...")
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
                creds = flow.run_local_server(port=8080, prompt='consent')
                with open('token.json', 'w') as token:
                    token.write(creds.to_json())
                    print("token generated")

            if not creds or not creds.valid:
                print("credentials need to be refreshed...")
                if creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                    with open('token.json', 'w') as token:
                        token.write(creds.to_json())
                        print("credentials refreshed")

            self.creds = creds
            print("credentials for session set")
        else:
            print("Missing credentials.json in root directory")

    def get_service(self):
        """Erstellt den Google Calendar API Service"""
        return build('calendar', 'v3', credentials=self.creds)

    def fetch_events(self, start_date, end_date):
        """Holt Ereignisse aus dem Google Kalender"""
        service = self.get_service()
        start_of_day = datetime.datetime.combine(start_date, datetime.datetime.min.time()).isoformat() + 'Z'
        end_of_day = datetime.datetime.combine(end_date, datetime.datetime.max.time()).isoformat() + 'Z'
        events_result = service.events().list(calendarId=self.calendar_id, timeMin=start_of_day, timeMax=end_of_day,
                                              singleEvents=True, orderBy='startTime').execute()
        return events_result.get('items', [])

    def add_event(self, event):
        """Fügt ein Ereignis zum Google Kalender hinzu"""
        service = self.get_service()
        return service.events().insert(calendarId=self.calendar_id, body=event).execute()

    def delete_event(self, event_id):
        """Löscht ein Ereignis aus dem Google Kalender"""
        service = self.get_service()
        service.events().delete(calendarId=self.calendar_id, eventId=event_id).execute()
