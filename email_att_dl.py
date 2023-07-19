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
        att_count = len(msg.attachments)    #count attachments to decide how to proceed
        att_index = 1
        msg_title = ''.join(e for e in msg.subject if e.isalnum() or e.isspace()) # sanitize msg title for later use
        for att in msg.attachments:
            att_name, att_ext = os.path.splitext(att.filename)
            if att_count == 1:
                with open(out_dir + "/" + msg_title + att_ext, 'wb') as f: 
                    f.write(att.payload)
            elif att_count > 1:
                with open(out_dir + "/" + msg_title + " "+ str(att_index) + att_ext, 'wb') as f: 
                    f.write(att.payload)
                    att_index = att_index + 1
            else:
                logging.debug("this email didnt include an attachment")
        msg_processed.append(msg.uid) #collect the processed emails
    mailbox.delete(msg_processed) #deleting the processed emails
