import requests
from bs4 import BeautifulSoup
import os
from twilio.rest import Client

twilio_file = open("/home/dniewinski/.twilio/auth", 'r')
twilio_auth = twilio_file.readlines()
twilio_file.close()

SID = twilio_auth[0]
AUTH = twilio_auth[1]
TRIAL_NUMBER = twilio_auth[2]
MY_NUMBER = twilio_auth[3]

client = Client(SID, AUTH)

page = requests.get("https://www.instructables.com/contest/")

soup = BeautifulSoup(page.content, 'html.parser')
curr_contests_div = soup.find_all(id="cur-contests")[0]
curr_contests_imgs = curr_contests_div.find_all('img')

past_contests = []
past_contests_file_name = "prev_contests.txt"
if os.path.exists(past_contests_file_name):
    past_contests_file = open(past_contests_file_name, 'r')
    for line in past_contests_file:
        past_contests.append(line.rstrip().lstrip())
    past_contests_file.close()

past_contests_file = open(past_contests_file_name, 'w')

text_message = ""
new_contest = False
for img in curr_contests_imgs:
    contest = img.get('alt')
    past_contests_file.write(contest + "\n")
    if contest not in past_contests:
        new_contest = True
        text_message = "!NEW! " + contest + "\n" + text_message
    else:
        text_message = text_message + contest + "\n"

if new_contest:
    print(text_message)
    client.messages.create(to=MY_NUMBER, from_=TRIAL_NUMBER, body=text_message)
else:
    print("Nothing New")

past_contests_file.close()
