import os
import time

import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import mail_sender
import email_reader

# link of event you want to reserve a ticket for
endpoint_rw = "https://www.ticketswap.com/event/rock-werchter-2022/combi-ticket/7ec76086-b660-48b9-97ec-220d143b484a/1639407"

def start_chromedriver_for_ticket(url):
    chrome_options = Options()
    chrome_options.headless = False
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    buy_ticket_btn = driver.find_element(by=By.XPATH, value='//button[text()="Buy ticket"]')
    buy_ticket_btn.click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "email")))
    email = driver.find_element(by=By.ID, value='email')

    email.send_keys(os.getenv('emailbot'))
    driver.find_element(by=By.XPATH, value="//button[text()='Continue with email']").click()
    driver.quit()


def start_chromedriver_for_aprove(url):
    chrome_options = Options()
    chrome_options.headless = False
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    input("Press any button to continue to search for tickets...")


def try_to_reserve_ticket():
    while True:
        ticket_available = False
        while not ticket_available:
            time.sleep(1)
            print("Trying " + endpoint_rw)
            resp = requests.get(endpoint_rw)
            soup = BeautifulSoup(resp.text, features="html.parser")
            for hdries in soup.find_all('h3'):
                if hdries.text == "Available":
                    a = hdries.nextSibling.find('a')
                    if not a:
                        ticket_available = False
                    else:
                        ticket_available = True
                        ticket_link = a["href"]
                        print("Ticket found!", ticket_link)

        start_chromedriver_for_ticket(ticket_link)

        gotmail = False
        while not gotmail:
            resp = email_reader.read_email_from_gmail()
            try:
                url = resp["url"]
                gotmail = True
            except:
                print("no mail")
                pass
        mail_sender.send_mail("Ticketswap", "A ticket should be reserved for 10 minutes... ", os.getenv('personal_mail'))
        start_chromedriver_for_aprove(url)


if __name__ == '__main__':
    try_to_reserve_ticket()
