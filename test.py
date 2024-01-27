import urllib.parse
import configparser
import os.path
import gspread
import pandas as pd
from json import loads, dumps

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

config = configparser.ConfigParser()
config.read('example.ini')
API_KEY = config['DEFAULT']['API_KEY']`
SPREADSHEET_ID = config['DEFAULT']['SPREADSHEET_ID']
RANGE = "Sheet1!A1:Y"
SPREADSHEET_URL = config['DEFAULT']['SPREADSHEET_URL']
url_correct = urllib.parse.quote_plus(SPREADSHEET_URL)




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

print(get_row("43266"))

"""client = gspread.authorize(authentication())
sheet = client.open_by_url(SPREADSHEET_URL)
sheet_instance = sheet.get_worksheet(0)
record = sheet_instance.get_all_records()
record"""