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
    print(form['id'])

# using the first form for exploratory data analysis
formId = resp.json()[0]['id']
resp = requests.get(apiUrl + "form/" + formId + "?key=" + apiKey)
if resp.status_code != 200:
    # This means something went wrong.
    raise Exception

payload = resp.json()
# explore payload
print(payload)

# explore questions and answers
fieldnamesIds = []
fieldnamesIdsMap = {}
for question in payload['questions']:
    print(question)
    fieldnamesIds.append(question['id'])
    fieldnamesIdsMap[question['id']] = question['question'].replace(u'\xa0', u' ')

print(fieldnamesIds)
print(fieldnamesIdsMap)
print(fieldnamesIds[0])
print(fieldnamesIdsMap[fieldnamesIds[0]])

for response in payload['responses']:
    print(response)

# create CSV
with open(formId + '.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')

    # write csv header
    header = [fieldnamesIdsMap[fieldnamesIds[0]]]
    i = 1
    while i < len(fieldnamesIds):
        header.append(fieldnamesIdsMap[fieldnamesIds[i]])
        i += 1
    writer.writerow(header)

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

        print(responseRow)
        writer.writerow(responseRow)
