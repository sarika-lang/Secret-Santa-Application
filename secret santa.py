import random

print("Welcome to the Secret Santa selection!")

name = ''
nameList = []
nameDict = {}
while True:
    name = input("Please input the names and email (name,email)! (enter + to exit): ")
    if name != '+' :
        workList = name.split(",")
        nameDict[workList[0]] = workList[1]
        nameList.append(workList[0])
    else:
        break

random.shuffle(nameList)

for i in range (0,len(nameList)):
    if i == len(nameList) - 1:
        print(f"Pair {i+1}: Angel: {nameList[i]}, Mortal: {nameList[0]}") 
    else:
        print(f"Pair {i+1}: Angel: {nameList[i]}, Mortal: {nameList[i+1]}")

import base64
import google.auth
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os 

# The SCOPES variable defines the permissions the app will request.
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

# Path to the credentials file (OAuth 2.0 credentials you downloaded from Google Cloud Console)
CREDENTIALS_FILE = '/Users/sarika./python projects/client_secret_1070807498408-dhkfrhepob3ibfo85tmicnclbb5l9v4t.apps.googleusercontent.com.json'

# Function to authenticate and send an email
def send_email():
    creds = None
    # If we have valid credentials, use them; otherwise, prompt the user to login.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    # If no valid credentials, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save credentials for future use.
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    
    # Build the Gmail service object
    service = build('gmail', 'v1', credentials=creds)

    for i in range (0,len(nameList)):
        if i == len(nameList) - 1:
            # Create the email message
            sender_email = "sarika22kannan@gmail.com"  # Replace with your email
            recipient_email = nameDict[nameList[i]]  # Replace with recipient email
            
            message = MIMEMultipart()
            message['to'] = recipient_email
            message['from'] = sender_email
            message['subject'] = "Your secret santa"
            
            body = f"Your mortal is {nameList[0]}"
            message.attach(MIMEText(body, 'plain'))

        else:
            # Create the email message
            sender_email = "sarika22kannan@gmail.com"  # Replace with your email
            recipient_email = nameDict[nameList[i]]  # Replace with recipient email
            
            message = MIMEMultipart()
            message['to'] = recipient_email
            message['from'] = sender_email
            message['subject'] = "Your secret santa"
            
            body = f"Your mortal is {nameList[i+1]}"
            message.attach(MIMEText(body, 'plain'))

        # Encode the message to base64
        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

        # Send the email
        try:
            message = service.users().messages().send(userId="me", body={'raw': raw_message}).execute()
            print(f"Message sent successfully: {message['id']}")
        except Exception as error:
            print(f"An error occurred: {error}")

if __name__ == '__main__':
    send_email()





