# -*- coding: utf-8 -*-
"""
Created on Thu May 26 19:16:48 2016

@author: Rikardo Jakus
"""
import argparse
import base64
import httplib2

from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

import gflags

FLAGS = gflags.FLAGS

parser = argparse.ArgumentParser(parents=[tools.argparser])
flags = parser.parse_args()
#print flags
SCOPES = 'https://www.googleapis.com/auth/cloud-platform'
CLIENT_SECRET = 'client_secret.json'

inputfile  = "/home/lenovo/Pictures/index.jpeg"

  
store = file.Storage('storage.json')
creds = store.get()
   
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets(CLIENT_SECRET, SCOPES)
    creds = tools.run_flow(flow, store, flags)
        
SERVICE = build('vision', 'v1', http=creds.authorize(Http()))
        
    # [START authenticate]
    #credentials = GoogleCredentials.get_application_default()
   # service = discovery.build('vision', 'v1', credentials=creds, discoveryServiceUrl=SCOPES)
                              
with open(inputfile, 'rb') as image:
    image_content = base64.b64encode(image.read())
    #print image_content
    service_request = SERVICE.images().annotate(body={
            'requests': [{
                'image': {
                    'content': image_content.decode('UTF-8')
                },
                'features': [{
						"type":"LABEL_DETECTION",
      						"maxResults": 10
      					},
      					{
      						"type":"TEXT_DETECTION",
      						"maxResults": 10
      					},
      					{
      						"type":"FACE_DETECTION",
      						"maxResults": 20
      					}]
            }]
        })
    response = service_request.execute()
    label = response['responses'][0]['labelAnnotations'][0]['description']
    #label2 = response['responses'][1]['labelAnnotations'][1]['description']
    print('Found label: %s for %s' % (label, inputfile))
    
  #  for r in response:
  #      print r['description']
    #print('Found label: %s for %s' % (label2, inputfile))
  #  f=open('foto',r+)
  #  jpgdata=f.read()
  #  f.close()

