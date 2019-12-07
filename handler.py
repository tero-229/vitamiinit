import json
import boto3
import os
from botocore.vendored import requests

region_name = 'eu-west-1'

def getDescription(search_criteria):

    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}
    data = requests.get('https://fineli.fi/fineli/api/v1/components', headers=headers).json()

    tulos = "Valitettavasti haullasi ei löytynyt yhtään tulosta"

    for item in data:
                
        description = item['description']['fi']
        if search_criteria.casefold() in description.casefold():
            tulos = description
        else:
            tulos

    return tulos

def sendEmail(event, context):
    data = event['body']
    name = "Qigolon nappikauppa Oy"
    destination = data['destination']
    search_criteria = data['search']
    source = "qigolo44@gmail.com"
    subject = "Qigolon nappikauppa Oy / Hakutulokset"
    tulos = getDescription(search_criteria)
    _message = "Viestin lähettäjä: " + name + "\nHakusi tulokset hakusanalla \"" + search_criteria.lower() + "\":\n" + tulos 
    
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
    return "Haku käynnissä... vastaus saapuu sähköpostiisi"

