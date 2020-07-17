import requests
from bs4 import BeautifulSoup
import smtplib
from email.message import EmailMessage
import os

os.path.join(os.path.dirname(__file__), 'data_store.txt')

def get_page_num():
    with open('data_store.txt', 'r') as f:
        return int(f.readline())

def query_website(page_num):
    return requests.get('https://ctrader.com/jobs/'+str(page_num))

def increment_page_num(page_num, status_code):
    if status_code == 200:
        page_num += 1
        with open('data_store.txt', 'w') as f:
            f.write(str(page_num))
    else:
        print('ERROR: ' + str(status_code))
        exit()

def get_title(text):
    soup = BeautifulSoup(text, features="html.parser")
    return soup.find('title').text

def do_email(page_num, status_code, title):
    if status_code == 200:
        s = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        s.set_debuglevel(1)
        address = ''
        password = ''
        s.login(address, password)
        # Open the plain text file whose name is in textfile for reading.
        msg = EmailMessage()
        msg.set_content('https://ctrader.com/jobs/' + str(page_num-1))

        # me == the sender's email address
        # you == the recipient's email address
        msg['Subject'] = title
        msg['From'] = [address]
        msg['To'] = address

        # Send the message via our own SMTP server.
        s.send_message(msg, address, address)
        s.quit()

if __name__ == '__main__':
    page_num = get_page_num()
    response = query_website(page_num)
    increment_page_num(page_num, response.status_code)
    title = get_title(response.text)
    do_email(page_num, response.status_code, title)
