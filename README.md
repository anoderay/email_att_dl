# Email Attachment Downloader
Simple Python script to receive emails, save attached files to a local folder and delete the email. 

There are several similar and more complex solutions out there but I got none of them working so I made my own. This script checks for emails via IMAP, downloads them, extracts attached files to a local folder and deletes the processed emails. Largely based on Vladimirs comment on [this Stackoverflow thread](https://stackoverflow.com/questions/58320352/how-to-download-all-attachments-of-a-mail-using-python-imap). 
