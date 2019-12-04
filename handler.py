import json
import boto3
import os

region_name = 'eu-central-1'    

#curlataan GETillä 'kalium', joka palauttaa finelin taulukosta DESCRIPTIONin kaliumille
#lähetetään curlattu RESPONSE emailina

tulos = "Valitettavasti haullasi ei löytynyt yhtään tulosta"

def getDescription(event, context):

    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}
    data = requests.get('https://fineli.fi/fineli/api/v1/components', headers=headers).json()

    search_criteria = event['search']

    for item in data:
                
        description = item['description']['fi']
        if search_criteria in description.casefold():
            tulos = description
           

def sendEmail(event, context):
    data = event['body']
    name = data['name'] 
    destination = data['destination']
    source = data['source']
    subject = data['subject']
    _message = "Message from: " + name + "\nEmail: " + source + "\nMessage content: " + tulos 
    
    client = boto3.client('ses' )    
        
    response = client.send_email(
        Destination={
            'ToAddresses': [destination]
            },
        Message={
            'Body': {
                'Text': {
                    'Charset': 'UTF-8',
                    'Data': _message,
                },
            },
            'Subject': {
                'Charset': 'UTF-8',
                'Data': subject,
            },
        },
        Source=source,
    )
    return _message + str(region_name)