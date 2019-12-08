# Gmail Client

下載Gmail信件？ 好簡單！

溫馨提醒：須先將google帳號的 **低安全性應用程式存取權** 打開

![release](https://img.shields.io/badge/release-v1.0.2-blue.svg) [![Python](https://img.shields.io/badge/python-3.7-blue.svg)](https://www.python.org/downloads/release/python-370/)



## Requirements

* imaplib
* email



## Features

* 輕鬆下載不同格式的email，目前支援 text 與 html
* 選取想查看的範圍，好自在
* 支援找到特定 信件標題（mail subject）模式



## Get Started

> 點擊右上角按鈕 "Clone or download"，將 gmail_client 模組移動到欲import的目錄，開始輕鬆下載gmail信件

* You need to login with your Google Account first

  ~~~python
  from gmail_client import MailClient
  
  account = 'YOUR GOOGLE ACCOUNT'
  pwd = 'YOUR GOOGLE PASSWORD'
  
  client = MailClient()
  client.login(account, pwd)
  ~~~

* Set `fmt=text`, means fetch text/plain format from mail.

  Then will return a **list** including what your mail content.

  ~~~python
  result_list = client.fetch_msg(fmt='text')
  ~~~

  

  **fetch_msg parameters：**

  * `fmt` *String*：取得的mail格式。支援 **text**, **html**
  * `heaedr` *Boolean*：是否包含mail header
  * `subject` *String*：只取特定subject的內容
  * `cont` *Boolean*：若有指定subject，是否繼續找完相同subject的信件。若cont=False，則找到第一封就結束執行

* Example of getting HTML from mail and specify subject

  ~~~python
  result_list = client.fetch_msg(fmt='html', header=False, subject='清大校務訊息系統', cont=False)
  
  print(result_list[0])
  ~~~

  Part of return：

  ~~~html
  <div dir="ltr"><br><br><div class="gmail_quote"><div dir="ltr" class="gmail_attr">---------- Forwarded message ---------<br>寄件者： <strong class="gmail_sendername" dir="auto">清大校務訊息系統</strong> <span dir="auto">&lt;<a href="mailto:nthumsg@my.nthu.edu.tw">nthumsg@my.nthu.edu.tw</a>&gt;</span><br>Date: 2019年12月6日 週五 下午12:43<br>Subject: &lt;NTHU Bulletin Board&gt;<br>To:  &lt;<a href="mailto:music1353@gmail.com">music1353@gmail.com</a>&gt;<br></div><br><br>
            
            <div>
              <div align="center">
                <table width="90%" border="0">
                  
                  <tbody><tr>
                    <td style="letter-spacing:2pt">
                      
                      <center style="font-size:8pt;color:red">For English version, please scroll down through the Chinese version.</center>
                    </td>
                  </tr>
                  <tr>
                    <td align="right">2019-12-06 12PM</td>
                  </tr>
                </tbody></table>
                <table width="95%" border="0">
                  <tbody><tr>
                    <td colspan="2" style="font-size:10pt">Chinese Version</td>
                  </tr>
                </tbody></table>
  ~~~



## Document

#### *class* **MailClient**

* `login(account, pwd)`
  * account *String*：your google account 
  * pwd *String*：your google password 
* `set_download_path(path)`
* `set_mail_scope(scope)`
  - scope *Int*：欲查看的信件範圍
* `fetch_msg(fmt='text', header=True, subject=None, cont=True)`
  * fmt *String*：取得的mail格式. 支援text, html
  * header *Boolean*：是否包含mail header
  * subject *String*：只取特定subject
  * cont *Boolean*：若有指定subject, 是否繼續找完相同subject的信件



## License

2019, Ching-Hsuan Su 蘇靖軒