from udp import UDPclient
import time

udp_client = UDPclient("10.0.0.29",5900,1024)
while True:
    msg = input('Comando :')
    udp_client.send_message(str(msg))
    time.sleep(.2)
    msg = udp_client.receive_message(1)
    print(msg)
    
