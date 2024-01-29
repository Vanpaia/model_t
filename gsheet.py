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

def get_new(range=RANGE):
    creds = authentication()
    try:
        service = build("sheets", "v4", credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()
        result = (sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=range).execute())
        values = result.get("values", [])
        df = pd.DataFrame(values[1:], columns=values[0])
        filtered_df = df.loc[df['nature'].str.contains("New")]
        changed = filtered_df.to_json(orient="records")
        parsed = loads(changed)
        return parsed
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


def get_id(search, range=RANGE):
    creds = authentication()
    try:
        service = build("sheets", "v4", credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()
        result = (sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=range).execute())
        values = result.get("values", [])
        df = pd.DataFrame(values[1:], columns=values[0])
        filtered_df = df.loc[df['internal_id'].str.contains(search)]
        changed = filtered_df.to_json(orient="records")
        parsed = loads(changed)
        return parsed
    except HttpError as err:
        print(err)

def entry_update(history, entry_base, entry_history):
    for x in history:
        if len(x["development"]) > 0:
            entry_history.append({"date": x["date_development"], "development":x["development"], "step":x["legislative_step"]})
        if len(x["related_id"]) > 0:
            entry_base["related_id"] = x["related_id"]
        if len(x["document_id"]) > 0:
            entry_base["document_id"] = x["document_id"]
        if len(x["native_title"]) > 0:
            entry_base["native_title"] = x["native_title"]
        if len(x["title"]) > 0:
            entry_base["title"] = x["title"]
        if len(x["description"]) > 0:
            entry_base["description"] = x["description"]
        if len(x["initiative_type"]) > 0:
            entry_base["initiative_type"] = x["initiative_type"]
        if len(x["legally_binding"]) > 0:
            entry_base["legally_binding"] = x["legally_binding"]
        if len(x["issue"]) > 0:
            entry_base["issue"] = x["issue"]
        if len(x["sub_issue"]) > 0:
            entry_base["sub_issue"] = x["sub_issue"]
        if len(x["likelihood"]) > 0:
            entry_base["likelihood"] = x["likelihood"]
        if len(x["impact_score"]) > 0:
            entry_base["impact_score"] = x["impact_score"]
        if len(x["impact"]) > 0:
            entry_base["impact"] = x["impact"]
        if len(x["adoption_year"]) > 0:
            entry_base["adoption_year"] = x["adoption_year"]
        if len(x["adoption_month"]) > 0:
            entry_base["adoption_month"] = x["adoption_month"]
        if len(x["enforcement_year"]) > 0:
            entry_base["enforcement_year"] = x["enforcement_year"]
        if len(x["enforcement_month"]) > 0:
            entry_base["enforcement_month"] = x["enforcement_month"]
        if len(x["relevant_links"]) > 0:
            entry_base["relevant_links"] = x["relevant_links"]
        if x["date_first_introduction"] is not None:
            entry_base["date_first_introduction"] = x["date_first_introduction"]