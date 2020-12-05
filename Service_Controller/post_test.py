import requests

req = requests.post(url="http://127.0.0.1:5002/send_command" ,json={'command':'left'})
if req.ok:
    print('OK')