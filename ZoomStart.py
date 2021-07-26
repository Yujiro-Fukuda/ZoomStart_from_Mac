from __future__ import print_function
import datetime
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import subprocess
import speech_recognition as sr

# If modifying these scopes, delete the file token.json.
#SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


def gcalender():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('/Users/UJ/PycharmProjects/ZoomStart/token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials2.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    #print('Getting the upcoming 10 events')
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                        maxResults=1, singleEvents=True,
                                        #maxResults=10, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    #if not events:
        #print('No upcoming events found.')
    for event in events:
        #start = event['start'].get('dateTime', event['start'].get('date'))
        #print(start, event['summary'])
        START = event['start'].get('dateTime', event['start'].get('date'))
        EVENT = event['summary']
    return START, EVENT


def gcalender2():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
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
                'credentials2.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    #print('Getting the upcoming 10 events')
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                          maxResults=10, singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])

    #if not events:
    #print('No upcoming events found.')
    LISTS = []
    for event in events:
        TMP = [event['start'].get('dateTime', event['start'].get('date')) ,event['summary']]
        DAY = TMP[0][0:10]
        TIME = TMP[0][11:16]
        MEETING = [DAY, TIME, event['summary']]
        LISTS.append(MEETING)
    return LISTS


def zoomstart(ZID, ZPASS):
    CMD = 'zoommtg://zoom.us/join?confno=' + ZID + '&pwd=' + ZPASS + ''
    res = subprocess.call(['/usr/bin/open', CMD])

def voice2txt():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("何時のZoom?")
        audio = r.listen(source)

    try:
        TIME = r.recognize_google(audio, language="ja-JP")
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

    if TIME == '16時':
        TIME = '16:00'

    return TIME

# 音声指示
def main():
    print("")
    TIME = voice2txt()
    START, EVENT = gcalender()
    EVENT = EVENT.split()
    if TIME == START[11:16]: zoomstart(EVENT[0], EVENT[1])

# リスト
def main2():
    LISTS = gcalender2()
    for id, list in enumerate(LISTS): print(id, list[:2])
    print("")
    no = int(input("打ち合わせの番号を入力して下さい --> "))
    EVENT = LISTS[no][2]
    EVENT = EVENT.split()
    print("")
    print("ZoomID:", EVENT[0], ", Pass:", EVENT[1])
    zoomstart(EVENT[0], EVENT[1])


if __name__ == '__main__':
    main2()