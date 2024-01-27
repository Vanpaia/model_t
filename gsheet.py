import configparser
import os.path
import pandas as pd
from json import loads, dumps

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

config = configparser.ConfigParser()
config.read('example.ini')

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SPREADSHEET_ID = config['DEFAULT']['SPREADSHEET_ID']
RANGE = "Sheet1!A2:Y"


def authentication():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
            "credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return(creds)

def get_all():
    creds = authentication()
    try:
        service = build("sheets", "v4", credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()
        result = (sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE).execute())
        values = result.get("values", [])
        df = pd.DataFrame(values[1:], columns=values[0])
        print(values)
        print(df)
    except HttpError as err:
        print(err)

def get_row(search):
    creds = authentication()
    try:
        service = build("sheets", "v4", credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()
        result = (sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE).execute())
        values = result.get("values", [])
        df = pd.DataFrame(values[1:], columns=values[0])
        filtered_df = df.loc[df['internal_id'].str.contains(search)]
        changed = filtered_df.to_json(orient="records")
        parsed = loads(changed)
        return parsed[0]
    except HttpError as err:
        print(err)


def get_id(search):
    creds = authentication()
    try:
        service = build("sheets", "v4", credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()
        result = (sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE).execute())
        values = result.get("values", [])
        df = pd.DataFrame(values[1:], columns=values[0])
        filtered_df = df.loc[df['internal_id'].str.contains(search)]
        changed = filtered_df.to_json(orient="records")
        parsed = loads(changed)
        return parsed
    except HttpError as err:
        print(err)

