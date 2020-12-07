import requests, time

while 1:
    try:
        #requests.post(url="http://127.0.0.1:5002/send_command" ,json={'command':'a'})
        req = requests.post(url="http://127.0.0.1:5002/get_info" ,json={'command':'r'})
        if req.ok:
            print(req.json())
    except:
        print('Falha')

    time.sleep(.1)