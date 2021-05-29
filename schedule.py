import time
import requests
from requests.structures import CaseInsensitiveDict
import datetime
import json
import csv, smtplib, ssl
from email.message import EmailMessage

#mail constants
from_address = 'from@gmail.com'
password = input("Type your password and press enter: ")
msg = EmailMessage()
msg['Subject'] = 'Vaccination Slot Available Now!'
msg['From'] = "from@gmail.com"
msg['To'] = "to@gmail.com"

#scheduler contants
delay = 500 # time between your next script execution
t1 = time.time()
today = datetime.date.today() + datetime.timedelta(days=0)
today = today.strftime('%d-%m-%Y')

# headers and initializations
headers = CaseInsensitiveDict()
headers["Accept"] = "application/json"
headers["Accept-Language"] = "en"
headers["User-Agent"] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
url = 'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id=571&date='
payload = ""
greeting = """Hello, 

We have found COVAXIN Vaccination slots for you in the following location :

"""

def getRequest():
    response = requests.get(url+today, headers=headers)
    response_json = json.loads(str(response.text))
    message = ""
    for element in response_json['centers']:
        for sessions_element in element['sessions']:
            if(sessions_element.get("vaccine") == 'COVAXIN'):
                if(sessions_element['min_age_limit'] == 18):
                    if(sessions_element['available_capacity'] > 0):
                        message += "Date : " + sessions_element['date'] + '\n'
                        message += "Hospital name : " + element['name'] + '\n'
                        message += "Hospital Address : " + element['address'] + '\n'
                        message += "Open from : " + element['from'] + '\n'
                        message += "Open till : " + element["to"] + '\n'
                        message += "Slots : " + str(sessions_element['slots']) + '\n'
                        message += "Capacity : " + str(sessions_element['available_capacity']) + '\n'
                        message += '\n'
    
    if(len(message) > 0):
        sendEmailAlert(greeting + message)
        message = ""

def sendEmailAlert(message):
    # Send the message via our own SMTP server.
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login(from_address, password)
    msg.set_content(message)
    server.send_message(msg)
    server.quit()

def main():
    wait = delay
    while True:
        t2 = time.time() - t1

        if t2 >= wait:
            wait += delay
            getRequest()

if __name__=="__main__":
    main()




      
      