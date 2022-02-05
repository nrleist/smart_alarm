from datetime import datetime   
from playsound import playsound
import requests as req
import bs4

ADDRESS = 'http://192.168.200.200'
AUDIO_PATH = 'C:/Users/nrlei/OneDrive/Documents/python/alarm-broken.mp3'

alarm_preset = True
alarm_preset_time = ['13', '14', '00']
alarm_days = [False, True, True, True, True, True, True]

def connection_test(address):
    try:
        req.get(address, timeout=5)
        print(f'Succesfully connected to {address}')
        return True
    except req.exceptions.ConnectionError and req.exceptions.Timeout:
        print(f'Could not connect to {address}. Check your connection and the connection of the device\nyour trying to connect to.\n Attemting to reconnect in 20 seconds. ')
        return False

def make_request(extention):
    try:
        return req.get(ADDRESS + '/' + extention, timeout=2)
    except (req.exceptions.ConnectionError, req.exceptions.Timeout):
        print(f'Could not connect to robot. Check your connection and the connection of the device\nyour trying to connect to.')

def get_status():
    try:
        soup = bs4.BeautifulSoup(req.get(ADDRESS).text, 'lxml')
        return soup.find('span').text
    except:
        return 'error'

def alarm_times(number):
    for i in range(number):
        playsound(AUDIO_PATH)

def alarm_loop():
    while True:
        playsound(AUDIO_PATH)
        if(get_status() == 'dismissed'):
            break
        elif(not get_status() == 'active'):
            alarm_times(3)
            break

def time_loop(alarm_time):
    while True:
        now = datetime.now()

        if(alarm_days[int(now.strftime("%w"))]):
            if(alarm_time[0] == now.strftime("%H")):
                if(alarm_time[1] == now.strftime("%M")):
                    if(alarm_time[2] == now.strftime("%S")):
                        print("Wake Up!")
                        make_request('A')
                        alarm_loop()
                        make_request('R')
                        break

def main_loop():
    make_request('R')
    while True:
        if not alarm_preset:
            alarm_time = input("Enter the time of alarm to be set:HH:MM:SS\n").split(':')
            print("Setting up alarm..")
            time_loop(alarm_time)
        else:
            print("Setting up alarm..")
            time_loop(alarm_preset_time)
        

if __name__ == "__main__":
    main_loop()