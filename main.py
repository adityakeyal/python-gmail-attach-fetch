import os.path
import base64
import json
import re
import time
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import logging
import requests

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def readEmails():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                # your creds file here. Please create json file as here https://cloud.google.com/docs/authentication/getting-started
                'my_cred_file.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    try:
        # Call the Gmail API
        service = build('gmail', 'v1', credentials=creds)
        results = service.users().messages().list(userId='me',  q="from:hr@nrifintech.com has:attachment filename:pdf", maxResults=500).execute()
        messages = results.get('messages',[]);
        if not messages:
            print('No new messages.')
        else:
            message_count = 0
            for message in messages:
                msg = service.users().messages().get(userId='me', id=message['id']).execute()
                for part in msg['payload']['parts']:
                    try:
                        if part['filename'] != "":
                            data = part['body']["attachmentId"]
                            manyparts = service.users().messages().attachments().get(userId='me', messageId=message['id'], id=data).execute()
                            with  open(f"{message_count}-{part['filename']}",'wb') as f:
                                d=manyparts['data'].replace("_","/").replace("-","+")
                                f.write(base64.standard_b64decode(d))
                                message_count=message_count+1



                    except BaseException as error:
                        raise error
                        pass

    except Exception as error:
        raise error
        print(f'An error occurred: {error}')


readEmails()