'''連接imap server及執行fetch msg的主要類別'''

import imaplib
import os
from gmail_client.mail import MailParser

class MailClient:
    def __init__(self):
        '''Init
            - imap: user的imap instance
            - scope: 選擇要查看前幾封信件
            - BASE_DIR: 欲下載信件的基礎目錄
        '''

        self.imap = ''
        self.scope = -1
        self.BASE_DIR = '.'

    def login(self, account, pwd):
        self.imap = imaplib.IMAP4_SSL('imap.gmail.com') # connect google mail server
        resp_status, accountDetails = self.imap.login(account, pwd)

        if resp_status == 'OK':
            print('Connect Success!')
            print('Login Status:', resp_status)
            print('Login Details:', accountDetails)
        else:
            raise ConnectionError("Cannot connect to Google's IMAP Server")

    def set_download_path(self, path):
        self.BASE_DIR = path

    def set_mail_scope(self, scope):
        self.scope = int(scope)

    def fetch_msg(self, fmt='text', subject=None, cont=True):
        ''' 擷取信件標題及內容
            - fmt: 取得的mail格式. 支援text, html
            - subject: 只取特定subject後, 就結束執行
            - cont: 若有指定subject, 是否繼續找完相同subject的信件
        '''

        self.imap.select('inbox')
        resp_status, data = self.imap.search(None, 'ALL')
        
        if resp_status == 'OK':
            selected_data = data[0].split()[-self.scope:] # 想查看郵件的範圍

            mail_parser = MailParser(self.imap, selected_data, subject, cont)

            if fmt is 'text':
                return mail_parser.parse_text()
            elif fmt is 'html':
                return mail_parser.parse_html()

            self.imap.logout()
        else:
            raise ConnectionError('Cannot search mail from IMAP Server')

    
    # FIXME: 下載email附件
    # def fatch_attachments(self):
    #     if resp_status == 'OK':
    #         print(resp_status, accountDetails)

    #         self.imap.select('inbox')
    #         resp_status, data = self.imap.search(None, 'ALL')
    #         selected_data = data[0].split()[-self.scope:] # 想查看郵件的範圍
            
    #         for msgId in selected_data:
    #             resp_status, message = self.imap.fetch(msgId, '(RFC822)')
    #             mail_body = message[0][1]
                
    #             mail = email.message_from_bytes(mail_body)
                
    #             for part in mail.walk():            
    #                 if part.get_content_maintype() == 'multipart':
    #                     continue
                    
    #                 if part.get('Content-Disposition') is None:
    #                     continue
                        
    #                 file_name = part.get_filename() # 取得附件檔名
                    
    #                 if bool(file_name):
    #                     file_path = os.path.join(self.BASE_DIR, file_name)
                        
    #                     if not os.path.isfile(file_path):
    #                         with open(file_path, 'wb') as fp:
    #                             fp.write(part.get_payload(decode=True))
    #                         print('attachment is downloaded !')
    #                     else:
    #                         print('file is already exist !')

    #         self.imap.logout()