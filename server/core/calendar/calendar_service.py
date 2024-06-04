from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import pickle 
import os
from datetime import timedelta

from config.settings.base import CALENDAR_CREDS_PATH, TEMP_TOKEN_PATH

class CalendarService:
    def __init__(self) -> None:
        self.scopes = ["https://www.googleapis.com/auth/calendar"]

    def __get_calendar_service(self):
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists(TEMP_TOKEN_PATH):
            with open(TEMP_TOKEN_PATH, 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    CALENDAR_CREDS_PATH, self.scopes)
                creds = flow.run_local_server(port=0)

            # Save the credentials for the next run
            with open(TEMP_TOKEN_PATH, 'wb') as token:
                pickle.dump(creds, token)

        service = build('calendar', 'v3', credentials=creds)
        return service
    
    def add_event(self, event_name, time):
        
        service = self.__get_calendar_service()
        end = (time + timedelta(hours=1)).isoformat()



        event_result = service.events().insert(calendarId='primary',
            body={
                "summary": event_name,
                "description": 'Automated by ANA chat bot',
                "start": {"dateTime": time.isoformat(), "timeZone": 'America/Edmonton'},
                "end": {"dateTime": end, "timeZone": 'America/Edmonton'},
            }
        ).execute()

    
    def get_event(self, time):
        service = self.__get_calendar_service()
        
        if service is not None:
            timeMax = time + timedelta(days=1)

            time = time.isoformat() +'Z'
            timeMax = timeMax.isoformat() + 'Z'

            events = service.events().list(
                calendarId='primary', 
                timeMin=time,
                timeMax = timeMax,
                maxResults=10, 
                singleEvents=True,
                orderBy='startTime'
            ).execute().get("items",[])

            if len(events) > 0 :
                print(events[0]["summary"])
                return events[0]["summary"]
            
            else : 
                answer = 'no event'
                return answer  
        else:
            print("Unable to establish connection with the service")
            return None