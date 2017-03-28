#!/usr/bin/env python
"""
Title:          extractData.py
Description:    Extracts data from Typeform form via API requests.
Author:         Stanley Lee
Date:           March 27, 2017
Version:        0.1
Usage:          python extractData.py
Python Version: 3.5.3

This python script will connect to Typeform via API requests to gather user entered form responses. It requires the
API url and API key to access the data. The output of the python script will be a csv formatted file named after the
form where the data is sourced form. Any missing response data is replaced with 'NaN' in the output file.

Todo:
    * Add option to provide API url via command line
    * Add option to provide API key via command line
    * Add option to specify which form to extract data
"""
import requests
import csv

apiUrl = "https://api.typeform.com/v1/"
apiKey = "ac83034cfa742c0f79c26e9a612b4ba7e2aa0d3d"

# get all forms available to apiKey
resp = requests.get(apiUrl + "forms?key=" + apiKey)
if resp.status_code != 200:
    # This means something went wrong.
    raise Exception

# accessing and getting a list of forms on account
for form in resp.json():

    # grab data from current form
    resp = requests.get(apiUrl + "form/" + form['id'] + "?key=" + apiKey)
    if resp.status_code != 200:
        # This means something went wrong.
        raise Exception

    # gather payload and generate fieldnames from payload
    payload = resp.json()
    fieldnamesIds = []
    fieldnamesIdsMap = {}

    for question in payload['questions']:
        fieldnamesIds.append(question['id'])
        fieldnamesIdsMap[question['id']] = question['question'].replace(u'\xa0', u' ')

    # create out CSV with the name of the current form
    with open(form['id'] + '.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')

        # write csv header
        header = [fieldnamesIdsMap[fieldnamesIds[0]]]
        i = 1
        while i < len(fieldnamesIds):
            header.append(fieldnamesIdsMap[fieldnamesIds[i]])
            i += 1
        writer.writerow(header)

        # write response data, replacing missing keys with NaN
        for response in payload['responses']:
            try:
                responseRow = [response['answers'][fieldnamesIds[0]]]
            except KeyError:
                responseRow = ['NaN']
            i = 1
            while i < len(fieldnamesIds):
                try:
                    responseRow.append(response['answers'][fieldnamesIds[i]])
                except KeyError:
                    responseRow.append('NaN')
                i += 1
            writer.writerow(responseRow)

    print("Typeform form data from UID {} has been created as {}.csv".format(form['id'], form['id']))
