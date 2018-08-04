import email
import imaplib
import os

class MailClient:
    def __init__(self):
        self.account = ''
        self.pwd = ''
        self.scope = -1
        self.BASE_DIR = '.'

    def login(self, account, pwd):
        self.account = account
        self.pwd = pwd

    def set_download_path(self, path):
        self.BASE_DIR = path

    def set_mail_scope(self, scope):
        self.scope = int(scope)

    def fatch_attachments(self):
        imap = imaplib.IMAP4_SSL('imap.gmail.com') # connect google mail server
        resp_status, accountDetails = imap.login(self.account, self.pwd)

        if resp_status == 'OK':
            print(resp_status, accountDetails)

            imap.select('inbox')
            resp_status, data = imap.search(None, 'ALL')
            selected_data = data[0].split()[-self.scope:] # 想查看郵件的範圍
            
            for msgId in selected_data:
                resp_status, message = imap.fetch(msgId, '(RFC822)')
                mail_body = message[0][1]
                
                mail = email.message_from_bytes(mail_body)
                
                for part in mail.walk():            
                    if part.get_content_maintype() == 'multipart':
                        continue
                    
                    if part.get('Content-Disposition') is None:
                        continue
                        
                    file_name = part.get_filename() # 取得附件檔名
                    
                    if bool(file_name):
                        file_path = os.path.join(self.BASE_DIR, file_name)
                        
                        if not os.path.isfile(file_path):
                            with open(file_path, 'wb') as fp:
                                fp.write(part.get_payload(decode=True))
                            print('attachment is downloaded !')
                        else:
                            print('file is already exist !')

            imap.logout()