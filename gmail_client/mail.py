'''parse mail內容的類別'''

import email
import datetime

class MailParser:
    def __init__(self, imap, data, subject=None, cont=False):
        '''Init
            - imap: user的imap instance
            - data: 郵件內容data
            - subject: 只取特定subject後, 就結束執行
            - cont: 若有指定subject, 是否繼續找完相同subject的信件
        '''

        self.imap = imap
        self.data = data
        self.subject = subject
        self.cont = cont

    def init_parse(self, message):
        '''初步解析mail
            Params:
                - message: 從原始imap fetch出的message
            Return:
                - result: { byte_message(Byte), str_message(String), mail_info: {local_date, local_message_date, email_from, email_to, email_subject} }
        '''

        raw_email = message[0][1]
        raw_email_string = raw_email.decode('utf-8')

        byte_message = email.message_from_bytes(raw_email)
        str_message = email.message_from_string(raw_email_string)
        
        # Header Details
        date_tuple = email.utils.parsedate_tz(str_message['Date'])
        if date_tuple:
            local_date = datetime.datetime.fromtimestamp(email.utils.mktime_tz(date_tuple))
            local_message_date = "%s" %(str(local_date.strftime("%a, %d %b %Y %H:%M:%S")))
            email_from = str(email.header.make_header(email.header.decode_header(str_message['From'])))
            email_to = str(email.header.make_header(email.header.decode_header(str_message['To'])))
            email_subject = str(email.header.make_header(email.header.decode_header(str_message['Subject'])))

        result = {
            'byte_message': byte_message,
            'str_message': str_message,
            'mail_info': {
                'local_date': local_date,
                'local_message_date': local_message_date,
                'email_from': email_from,
                'email_to': email_to,
                'email_subject': email_subject
            }
        }
        return result

    
    def parse_html(self, header=True):
        '''將mail解析成html
            Params:
                - header(Boolean): 是否包含mail header
            Return:
                body_result(List)
        '''

        body_result = []
        print('---- Start to read email! ----')

        for msgId in self.data[::-1]: # 從最新的郵件開始找
            resp_status, message = self.imap.fetch(msgId, '(RFC822)')
            mail_content = self.init_parse(message)

            byte_message = mail_content['byte_message']
            str_message = mail_content['str_message']

            mail_info = mail_content['mail_info']
            local_date = mail_info['local_date']
            local_message_date = mail_info['local_message_date']
            email_from = mail_info['email_from']
            email_to = mail_info['email_to']
            email_subject = mail_info['email_subject']

            print('Email Subject:', email_subject)

            # Body details
            for part in byte_message.walk():
                if part.get_content_type() == "text/html": # get html
                    if self.subject:
                        if email_subject == self.subject:
                            body = part.get_payload(decode=True).decode('utf-8')

                            if header:
                                header_body = "From: %s\nTo: %s\nDate: %s\nSubject: %s\n\nBody: \n\n%s" %(email_from, email_to, local_message_date, email_subject, body)
                                body_result.append(header_body)
                            else:
                                body_result.append(body)

                            # parse by pq
                            # doc = pq(body)
                            # doc = doc.remove(".gmail_attr")
                            # # print(doc)
                            # for link in doc('a').items():
                            #     print(link)
                            #     print('------------------------')

                            # print("From: %s\nTo: %s\nDate: %s\nSubject: %s\n\nBody: \n\n%s" %(email_from, email_to, local_message_date, email_subject, body.decode('utf-8')))

                            if self.cont is False:  # 匹配第一個subject, 不繼續執行
                                print('---- Done! ----')
                                return body_result
                            else:
                                continue
                    else:
                        body = part.get_payload(decode=True).decode('utf-8')
                        body_result.append(body)
                else:
                    continue

        print('---- Done! ----')
        return body_result


    def parse_text(self, header=True):
        '''將mail解析成text
            Params:
                - header(Boolean): 是否包含mail header
            Return:
                body_result(List)
        '''

        body_result = []
        print('---- Start to read email! ----')

        for msgId in self.data[::-1]: # 從最新的郵件開始找
            resp_status, message = self.imap.fetch(msgId, '(RFC822)')
            mail_content = self.init_parse(message)

            byte_message = mail_content['byte_message']
            str_message = mail_content['str_message']

            mail_info = mail_content['mail_info']
            local_date = mail_info['local_date']
            local_message_date = mail_info['local_message_date']
            email_from = mail_info['email_from']
            email_to = mail_info['email_to']
            email_subject = mail_info['email_subject']

            print('Email Subject:', email_subject)

            # Body details
            for part in str_message.walk():
                if part.get_content_type() == "text/plain": # get text
                    if self.subject:
                        if email_subject == self.subject:
                            body = part.get_payload(decode=True).decode('utf-8')

                            if header:
                                header_body = "From: %s\nTo: %s\nDate: %s\nSubject: %s\n\nBody: \n\n%s" %(email_from, email_to, local_message_date, email_subject, body)
                                body_result.append(header_body)
                            else:
                                body_result.append(body)

                            if self.cont is False:  # 匹配第一個subject, 不繼續執行
                                print('---- Done! ----')
                                return body_result
                            else:
                                continue
                    else:
                        body = part.get_payload(decode=True).decode('utf-8')
                        body_result.append(body)
                else:
                    continue

        print('---- Done! ----')
        return body_result