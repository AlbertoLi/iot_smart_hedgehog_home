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
            averages["co2"]=float(runningaverages["co2"])/averagecount
            runningaverages["co2"]=0
            averages["temperature"]=float(runningaverages["temperature"])/averagecount
            runningaverages["temperature"]=0
            averages["light"]=float(runningaverages["light"])/averagecount
            runningaverages["light"]=0
            averages["humidity"]=float(runningaverages["humidity"])/averagecount
            runningaverages["humidity"]=0
            statisticstimestamp=time.time()
            averagecount=0
            print(averages)
        items = response['Items']
            if len(items) > 0:
            averagecount+=1
            runningaverages["co2"]+=int(items[0]["co2"])
            runningaverages["humidity"]+=int(items[0]["humidity"])
            runningaverages["light"]+=int(items[0]["light"])
            runningaverages["temperature"]+=int(items[0]["temperature"])
            data["Timestamp"] = str(items[0]["Timestamp"])
            data["co2"] = int(items[0]["co2"])
            data["temperature"] = int(items[0]["temperature"])
            data["light"] = int(items[0]["light"])
            data["humidity"] = int(items[0]["humidity"])
            data["co2avg"] = float(averages["co2"])
                        data["temperatureavg"] = float(averages["temperature"])
                        data["lightavg"] = float(averages["light"])
                        data["humidityavg"] = float(averages["humidity"])
            logger.info(json.dumps(data))
            return jsonify(json.dumps(data))

        else:
            return jsonify({'temperature': 0, 'humidity': 0,'co2': 0,'light': 0})

    except Exception as err:
        print("Unexpected error:", err)
        pass
            
    return jsonify({'temperature': 0, 'humidity': 0,'co2': 0,'light': 0})