# script for downloading email-attachments via IMAP and deleting the processed emails afterwards - created to consume files with paperless via sent emails. Tested on Python3.10

from imap_tools import MailBox
import logging
import os

logging.basicConfig(level=logging.ERROR)

host = "your mail server"
user = "your mail login"
secret = "your mail password"
out_dir = "directory"
msg_processed = []

try:
    os.makedirs(out_dir)
    logging.debug('created output directory named ' + out_dir)
except:
    logging.debug('Output directory exists')

# get all attachments for each email from INBOX folder
with MailBox(host).login(user, secret) as mailbox:
    for msg in mailbox.fetch():
        for att in msg.attachments:
            logging.info("downloaded " + att.filename, att.content_type)
            with open(out_dir + "/" + att.filename, 'wb') as f: 
                f.write(att.payload)
        msg_processed.append(msg.uid) #collect the processed emails
    logging.info("deleting processed messages") 
    mailbox.delete(msg_processed) #deleting the processed emails
