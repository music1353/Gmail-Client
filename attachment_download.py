import email
import imaplib
import os

BASE_DIR = '.'
if 'attachments' not in os.listdir(BASE_DIR):
    os.mkdir('attachments')

account = input('your gmail accout:')
pwd = input('your gmail password:')
scope = input('請輸入要前幾封:')
scope = int(scope)

imap = imaplib.IMAP4_SSL('imap.gmail.com') # connect google mail server
resp_status, accountDetails = imap.login(account, pwd)

if resp_status == 'OK':
    print(resp_status, accountDetails)

    imap.select('inbox')
    resp_status, data = imap.search(None, 'ALL')
    selected_data = data[0].split()[-scope:] # 想查看郵件的範圍
    
    for msgId in selected_data:
        resp_status, message = imap.fetch(msgId, '(RFC822)')
        mail_body = message[0][1]
        
        mail = email.message_from_string(mail_body.decode())
        
        for part in mail.walk():            
            if part.get_content_maintype() == 'multipart':
                continue
            
            if part.get('Content-Disposition') is None:
                continue
                
            file_name = part.get_filename() # 取得附件檔名
            
            if bool(file_name):
                file_path = os.path.join(BASE_DIR, 'attachments', file_name)
                
                if not os.path.isfile(file_path):
                    with open(file_path, 'wb') as fp:
                        fp.write(part.get_payload(decode=True))
                    print('attachment is downloaded !')
                else:
                    print('file is already exist !')

    imap.logout()