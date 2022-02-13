from tracemalloc import start
from typing import final
from flask import Flask,request, jsonify,render_template
from flask_ngrok import run_with_ngrok
from flask_cors import CORS
import json
import requests
from pytube import YouTube
import pathlib
import os
import time
import database
import symbl

app = Flask(__name__,static_folder='/content/static')
#run_with_ngrok(app)

CORS(app)


start = time.perf_counter()

#database.create_tables()
#data = 'https://www.youtube.com/watch?v=ZSt9tm3RoUU'

def youtube_video_download(data):    
    path = r"C:\Users\DELL\Desktop\2022\flask\public\videos\\"
    url = data
    youtube = YouTube(url)
    youtube.streams.first().download(filename = "my.mp4", output_path = path)   
    print('download completed')

#youtube_video_download('https://www.youtube.com/watch?v=ZSt9tm3RoUU')



@app.route('/video', methods=["POST","GET"])
def video_caption():
    data = request.json
    print(data)
    youtube_video_download(data)
    print(data)

    url = "https://api.symbl.ai/v1/process/video"

    payload = None

    try:
        video_file = open(r'C:\Users\DELL\Desktop\2022\flask\public\videos\my.mp4', 'rb')  # use (r"path/to/file") when using windows path
        payload = video_file.read()
    except FileNotFoundError:
        print("Could not find the file provided.")
        exit()

    access_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlFVUTRNemhDUVVWQk1rTkJNemszUTBNMlFVVTRRekkyUmpWQ056VTJRelUxUTBVeE5EZzFNUSJ9.eyJodHRwczovL3BsYXRmb3JtLnN5bWJsLmFpL3VzZXJJZCI6IjUwMzI1MjMyOTU4ODMyNjQiLCJpc3MiOiJodHRwczovL2RpcmVjdC1wbGF0Zm9ybS5hdXRoMC5jb20vIiwic3ViIjoiZWs0ZVUxSk93bnI3dGZpYkRXYjQyZGxxd0ZqSlBES01AY2xpZW50cyIsImF1ZCI6Imh0dHBzOi8vcGxhdGZvcm0ucmFtbWVyLmFpIiwiaWF0IjoxNjQ0NjgwNTMwLCJleHAiOjE2NDQ3NjY5MzAsImF6cCI6ImVrNGVVMUpPd25yN3RmaWJEV2I0MmRscXdGakpQREtNIiwiZ3R5IjoiY2xpZW50LWNyZWRlbnRpYWxzIn0.UJ2o_CKFCQ2jbpvewGM_rJa_eYxzU1hfh7n-TVVLvzPk2oLjefoZ-2kd5UmK1U34spWAD2kmmlpH3wfTHWrf4wNkerf8FwRle9_cdmsuz2uIKNy3aeeUfGHr3WoCEymvlcgfDDpv37m_rAquu_xrxPW_AASHN74AxsrLvSc7fmAquzDimmRWZgjRLBSC844zo7sQkwbAVwOt3QDHjgd5xCAUiYB9f7Slg_5EN0Il2OR7AkRugJlcrqPZ8Gmzc9ziUNMX_lpSBcyEK2yzNtoXJpG7K_e09ycVeyfxJWa1hqEKw0pYwfXMJu4aFChHdVb-AsK_lIQhsi9mA6SZHj9fCA'

    headers = {
        'Authorization': 'Bearer ' + access_token,
        'Content-Type': 'video/mp4'  
    }

    params = {
        'name': "Business Meeting",
        'confidenceThreshold': 0.6,      
    }

    responses = {
        400: 'Bad Request! Please refer docs for correct input fields.',
        401: 'Unauthorized. Please generate a new access token.',
        404: 'The conversation and/or it\'s metadata you asked could not be found, please check the input provided',
        429: 'Maximum number of concurrent jobs reached. Please wait for some requests to complete.',
        500: 'Something went wrong! Please contact support@symbl.ai'
    }

    response = requests.request("POST", url, headers=headers, data=payload, params='?enableSummary=true')

    if response.status_code == 201:
        # Successful API execution
        print("conversationId => " + response.json()['conversationId'])  # ID to be used with Conversation API.
        conversationId = str(response.json()['conversationId'])
        print(response.json()['jobId']) 
        jobid = response.json()['jobId'] # ID to be used with Job API.
    elif response.status_code in responses.keys():
        print(responses[response.status_code])  # Expected error occurred
    else:
        print("Unexpected error occurred. Please contact support@symbl.ai" + ", Debug Message => " + str(response.text))

    conversationId = str(response.json()['conversationId'])

    headerss = {
        'Authorization': 'Bearer ' + access_token,
        'Content-Type': 'application/json'  
    }

    urls = "https://api.symbl.ai/v1/job/"+jobid

    response = requests.request("GET", urls, headers=headerss)
    print(response.json())
    print(response.json()['status'])
    jobstatus = response.json()['status']

    final = " "
    out = " "

    time.sleep(40)
  

    url = "https://api.symbl.ai/v1/conversations/"+conversationId+"/summary"


    headers = {
        'Authorization': 'Bearer ' + access_token,
        'Content-Type': 'application/json'
    }

    response = requests.request("GET", url, headers=headers)

    print(response)
    print( response.json()['summary']) 
    print(response.json()['summary'][0]['text'])
    final =  response.json()['summary'][0]['text']

    msg = symbl.Conversations.get_topics(conversationId)

    

    for i in range(len(msg.topics)):
        out = msg.topics[i].text+',  ' + out 
        print(out)

    return jsonify({'data':final},{'topics':out})
        

    


	
app.run()
