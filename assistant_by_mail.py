import re
import sys
import time
#from query_model_api import query_model

import mail_in
import mail_out
from configuration import engine, sender_passwords


def to_file(text):

    # 'a' mode appends to the file without overwriting
    with open("/Users/slawekpiela/pycharmprojects/mail_llm/mail_log.txt", 'a') as file:
        file.write(text + "\n")
        return


def extract_email_address(raw_from):
    # Use regular expression to find text between < and >
    match = re.search(r'<(.+?)>', raw_from)
    if match:
        return match.group(1)
    else:
        return None


# def main
counter = 0

while True:

    email_details = mail_in.fetch_mail_content_and_sender()

    print("email details: ", email_details[1])
    file_text = f"email details:,{email_details[1]}" #only body of email
    to_file(file_text)

    sys.stdout.write("\033[F\033[K")
    if email_details is not None and len(email_details) > 0:

        body = email_details[1]
        body = f"Krótko odpowiedz: , {email_details[1]}"
        file_text = f"Krótko odpowiedz: , {email_details[1]}"
        to_file(file_text)
        sender_email = email_details[0]

        model = engine
        #response = query_model(body)
        #file_text = response[0]
        #to_file(file_text)

        mail_out.send_email("slawek.piela@koios-mail.pl", sender_passwords,
                            sender_email, "KOIOS AI response", file_text)

        print("Ai response sent")

        counter = counter+1

    #time.sleep(60)
