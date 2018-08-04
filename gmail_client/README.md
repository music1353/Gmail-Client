# Gmail Client

> Use IMAP construct a google mail client

## Get Started

* 須先將google帳號的 **低安全性應用程式存取權** 打開

~~~python
from gmail_client.client import MailClient

myClient = MailClient()
myClient.login(account, pwd) # login with your gmail
myClient.set_mail_scope(1) # 選擇要查看前幾封信件, 預設最新的一封信件
myClient.fatch_attachments() # 若有附件, 下載信件附件
~~~

