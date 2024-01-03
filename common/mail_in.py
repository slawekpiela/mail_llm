import email
import imaplib
import re
import sys

from configuration import sender_passwords, user_mailin


def extract_email_address(raw_from):
    # Use regular expression to find text between < and >
    match = re.search(r'<(.+?)>', raw_from)
    if match:
        return match.group(1)

    return None


def get_email_content(message):
    """Extract content from email message, only plain text."""
    parts = []
    for part in message.walk():
        # Ignore attachments and non-text parts
        if part.get_content_maintype() != 'text' or part.get("Content-Disposition"):
            continue

        # Get the payload, skip if it's None
        payload = part.get_payload(decode=True)
        if payload is None:
            continue

        # Check if the content type is plain text
        if part.get_content_type() == 'text/plain':
            # Decode and append the payload
            try:
                parts.append(payload.decode())
            except UnicodeDecodeError:
                # Handle decoding error (e.g., by skipping this part)
                continue

    return "\n".join(parts)


import imaplib
import email


import imaplib
import email

def fetch_mail_content_and_sender():
    print("start")

    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login(user_mailin, sender_passwords)

    status, folders = mail.list()

    print("Folders in your mailbox:")
    for folder in folders:
        folder_name = folder.decode().split(' "/" ')[-1].strip('"')
        imap_folder_name = folder_name

        # Handling Gmail's special folders
        if folder_name.lower() == "wersje robocze":
            imap_folder_name = "[Gmail]/Drafts"

        print(f"\nProcessing folder: {imap_folder_name}","\n")
        result, data = mail.select(f'"{imap_folder_name}"', readonly=True)
        if result == 'OK':
            email_count = int(data[0])  # Number of messages in the folder
            print(f"Number of emails in '{imap_folder_name}': {email_count}")

        try:
            mail.select(f'"{imap_folder_name}"') # set folder name

            result, data = mail.search(None, 'ALL') # we fetch ALL emails
            email_ids = data[0].split()
            count = 0

            if email_ids:                               #if not empty folder
                sorted_email_ids = sorted(email_ids, key=int)
                emails = []

                for email_id in sorted_email_ids:

                    result, email_data = mail.fetch(email_id, '(RFC822)')
                    raw_email = email_data[0][1]
                    msg = email.message_from_bytes(raw_email)
                    print(msg)
                    sender = extract_email_address(msg['from'])
                    recipient = extract_email_address(msg['to'])  # Extract recipient
                    subject = msg['subject']
                    content = get_email_content(msg)
                    message_id = msg.get('Message-ID', None)

                    email_info = {
                        'folder': imap_folder_name,
                        'id': email_id.decode(),  # Convert bytes to string
                        'message_id': message_id,
                        'sender': sender,
                        'recipient': recipient,
                        'subject': subject,
                        'content': content
                    }

                    email_to_file = f'{imap_folder_name},"\n",{email_info["id"]},"\n"," ", {message_id},"\n",{sender},"\n",{recipient},"\n",{subject},"\n",{content}'
                    with open("/Users/slawekpiela/pycharmprojects/mail_log.txt", 'a') as file: file.write(email_to_file + "\n")
                    with open("/Users/slawekpiela/pycharmprojects/mail_log_IDs.txt", 'a') as file: file.write(message_id + "\n")
                    emails.append(email_info)
                    #print(f'Folder: {imap_folder_name}, Email ID: {email_id.decode()}, Sender: {sender}, Recipient: {recipient}, Subject: {subject}')
                    count += 1
                    print("\r",count, end='') # show progres

        except Exception as e:
            print(f"Error processing folder {folder_name}: {e}")

    return emails


def main():
    fetch_mail_content_and_sender()

main()
