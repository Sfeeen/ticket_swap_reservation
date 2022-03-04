# Created by Sven Onderbeke at 03/03/2022
# Python 3.8.0
import os
import smtplib
import time
import imaplib
import email
import traceback
# -------------------------------------------------
#
# Utility to read email from Gmail Using Python
#
# ------------------------------------------------

FROM_EMAIL = os.getenv('emailbot')
FROM_PWD = os.environ.get('emailbot_pw')
SMTP_SERVER = "imap.gmail.com"
SMTP_PORT = 993


# Function to get email content part i.e its body part
def get_body(msg):
    if msg.is_multipart():
        return get_body(msg.get_payload(0))
    else:
        return msg.get_payload(None, True)


# Function to search for a key value pair
def search(key, value, con):
    result, data = con.search(None, key, '"{}"'.format(value))
    return data


# Function to get the list of emails under this label
def get_emails(con, result_bytes):
    msgs = []  # all the email data are pushed inside an array
    for num in result_bytes[0].split():
        typ, data = con.fetch(num, '(RFC822)')
        msgs.append(data)

    return msgs

def read_email_from_gmail():
    try:
        mail = imaplib.IMAP4_SSL(SMTP_SERVER)
        mail.login(FROM_EMAIL,FROM_PWD)
        mail.select('inbox')

        msgs = get_emails(mail, search('FROM', "info@ticketswap.com", mail))

        # Uncomment this to see what actually comes as data
        # print(msgs)

        # Finding the required content from our msgs
        # User can make custom changes in this part to
        # fetch the required content he / she needs

        # printing them by the order they are displayed in your gmail
        for msg in msgs[::-1]:
            for sent in msg:
                if type(sent) is tuple:

                    # encoding set as utf-8
                    content = str(sent[1], 'utf-8')
                    data = str(content)

                    # Handling errors related to unicodenecode
                    try:
                        indexstart = data.find("https://browser.ticketswap.com/magic-link/")
                        indexend = data.find("platform=web")
                        url = data[indexstart: indexend + 12]
                        print("found url in mail:", url)
                        return {"url": url}

                    except UnicodeEncodeError as e:
                        pass

    except Exception as e:
        print("Exception")
        traceback.print_exc()
        print(str(e))
