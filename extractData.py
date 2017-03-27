import requests

resp = requests.get('https://api.typeform.com/v1/forms?key=ac83034cfa742c0f79c26e9a612b4ba7e2aa0d3d')
if resp.status_code != 200:
    # This means something went wrong.
    raise Exception
for item in resp.json():
    print(item)
