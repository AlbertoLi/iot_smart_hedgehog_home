#!/usr/bin/env python
import flask
from flask import request, render_template, jsonify
import boto3
from boto3.dynamodb.conditions import Key, Attr
import cPickle as pickle
import datetime
import time
import json
import sys
import os
import logging
import logging.handlers

AWS_ACCESS_KEY="AKIAJ5K42O4X7PNSVQHA" 
AWS_SECRET_KEY="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"
REGION="us-east-2"

dynamodb = boto3.resource('dynamodb', aws_access_key_id=AWS_ACCESS_KEY,
                            aws_secret_access_key=AWS_SECRET_KEY,
                            region_name=REGION)

table = dynamodb.Table('SensorData')

APP = flask.Flask(__name__)
statisticstimestamp=""
averages={"temperature":0,"speed":0,'rpm':0}
averagecount=0
runningaverages={"temperature":0,"speed":0,"rpm":0}



@APP.route('/data')
def get_Data():
    global statisticstimestamp
    global averages
    global averagecount
    global runningaverages

    if(statisticstimestamp==""):
        statisticstimestamp=time.time()
    try:
        data = {}
        ts=time.time()
        
        timestampold = datetime.datetime.fromtimestamp(ts-10).strftime('%Y-%m-%d %H:%M:%S')
        timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        
        response = table.scan(FilterExpression=Key('Timestamp').between(timestampold, timestamp))
        if(statisticstimestamp<(time.time()-60)):
            averages["temperature"]=float(runningaverages["temperature"])/averagecount
            runningaverages["temperature"]=0
            averages["speed"]=float(runningaverages["speed"])/averagecount
            runningaverages["speed"]=0
            averages["rpm"]=float(runningaverages["rpm"])/averagecount
            runningaverages["rpm"]=0
            statisticstimestamp=time.time()
            averagecount=0
            print(averages)
        items = response['Items']
        if len(items) > 0:
            averagecount+=1
            runningaverages["speed"]+=int(items[0]["speed"])
            runningaverages["temperature"]+=int(items[0]["temperature"])
            runningaverages["rpm"]+=int(items[0]["rpm"])
            data["Timestamp"] = str(items[0]["Timestamp"])
            data["temperature"] = int(items[0]["temperature"])
            data["speed"] = int(items[0]["speed"])
            data["rpm"] = int(items[0]["rpm"])
            data["co2avg"] = float(averages["co2"])
            data["temperatureavg"] = float(averages["temperature"])
            data["speedaverage"] = float(averages["speed"])
            data["rpmaverage"] = float(averages["rpm"])
            logger.info(json.dumps(data))
            return jsonify(json.dumps(data))

        else:
            return jsonify({'temperature': 0, 'speed': 0,'rpm':0})


    except Exception as err:
        print("Unexpected error:", err)
        pass
            
    return jsonify({'temperature': 0, 'speed': 0,'rpm':0})

@APP.route('/', methods=['GET'])
def home_page():
    return render_template('dashboard.html',avs=averages)

@APP.route('/musicsubmission', methods=['GET'])
def musicsubmission_page():
    return render_template('musicsubmission.html')

@APP.route('/snacksubmission', methods=['GET'])
def snacksubmission_page():
    return render_template('snacksubmission.html')

if __name__ == '__main__':
    APP.debug=True
    APP.run(host='0.0.0.0', port=5000)