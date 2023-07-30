from imap_tools import MailBox, OR, NOT
import logging
from logging.handlers import RotatingFileHandler
import os


# Set up logfile and message logging.
logger = logging.getLogger("Logger")
logger.setLevel(logging.info)
# Create the rotating file handler. Limit the size to ~ 5MB .
handler = RotatingFileHandler("/volume1/paperless/email_att_downloader_script/mail_att_dl.log", mode='a', maxBytes=5*1024*1024, backupCount=1, encoding='utf-8', delay=0)
handler.setLevel(logging.info)
# Create a formatter.
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# Add handler and formatter.
handler.setFormatter(formatter)
logger.addHandler(handler)


host = "yourhost"
user = "youruser"
secret = ""
out_dir = "output directory"
msg_processed = []
msg_unknown = []
trusted_senders = "email adresses", "of", "trusted", "senders"

# connecting to host
try:
    logger.debug("connecting to %s",host)
    mailbox = MailBox(host).login(user, secret)
except:
    logger.error("Could not connect to host %s with user %s, check credentials or connection", host, user)
    exit(1)

# getting messages from trusted senders
for msg in mailbox.fetch(OR(from_=trusted_senders)):
    logger.info("processing email with uid '%s' and title '%s' from '%s'", msg.uid, msg.subject, msg.from_)
    att_count = len(msg.attachments)    #count attachments to decide how to proceed
    att_index = 1
    msg_title = ''.join(e for e in msg.subject if e.isalnum() or e.isspace()) # sanitize msg title for later use
    for att in msg.attachments:
        att_name, att_ext = os.path.splitext(att.filename)
        if att_count == 1:
            with open(out_dir + "/" + msg_title + att_ext, 'wb') as f: 
                f.write(att.payload)
                logger.debug("saved file '"+ msg_title + att_ext + "'")
        elif att_count > 1:
            with open(out_dir + "/" + msg_title + " "+ str(att_index) + att_ext, 'wb') as f: 
                f.write(att.payload)
                att_index = att_index + 1
                logger.debug("saved file '"+ msg_title + " " + str(att_index) + att_ext + "'")
        elif att_count == 0:
            logger.debug("email with uid '%s' from '%s' with title '%s' did not include an attachment", msg.uid, msg.from_, msg.subject)
    msg_processed.append(msg.uid) #collect the processed emails

#delete processed emails
if len(msg_processed) != 0:
    mailbox.delete(msg_processed) #deleting the processed emails
    logger.info("processed and deleted messages with UIDs "+", ".join(msg_processed))
else:
    logger.info("no messages from trusted senders found")

#deleting messages from non trusted senders
for msg in mailbox.fetch(NOT(OR(from_=trusted_senders))):
    logger.info("email with uid '%s' and title '%s' from '%s' was not in the list of trusted senders and will be deleted", msg.uid, msg.subject, msg.from_)
    msg_unknown.append(msg.uid)
if len(msg_unknown) != 0:
    mailbox.delete(msg_unknown) #deleting the processed emails
