import requests

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
for question in payload['questions']:
    print(question)

for response in payload['responses']:
    print(response)
