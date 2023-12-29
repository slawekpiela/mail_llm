import email
import imaplib
import re

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



def fetch_mail_content_and_sender(folder_name):
    print("start")
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login(user_mailin, sender_passwords)
    mail.select(folder_name)

    result, data = mail.search(None, 'ALL')
    email_ids = data[0].split()
    count=0

    if email_ids:
        # Sort the email IDs
        sorted_email_ids = sorted(email_ids, key=int)

        # Initialize a list to store email details
        emails = []

        # Iterate through each email ID
        for email_id in sorted_email_ids:
            # Fetch the email
            result, email_data = mail.fetch(email_id, '(RFC822)')
            raw_email = email_data[0][1]
            msg = email.message_from_bytes(raw_email)

            # Extract relevant information
            sender = extract_email_address(msg['from'])
            subject = msg['subject']
            content = get_email_content(msg)

            # Store or process the information
            email_info = {
                'sender': sender,
                'subject': subject,
                'content': content
            }
            email_to_file=(f'{sender},{subject},{content}')
            with open("/Users/slawekpiela/pycharmprojects/mail_llm/mail_log.txt", 'a') as file:
                file.write(email_to_file)
            emails.append(email_info)
            print('\rEmail nr:',count ,end="")
            count+=1

        # Now 'emails' contains information about all emails
        return emails



while True:
    fetch_mail_content_and_sender('inbox')
    fetch_mail_content_and_sender('archive')
