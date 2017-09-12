# -*- coding: utf-8 -*-
from __future__ import print_function
import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from email.header import Header

url_prefix_1 = 'http://www.hrssgz.gov.cn/rczp/gwyzk/gwyzkgg/'
url_prefix_2 = 'http://www.hrssgz.gov.cn/rczp/sydwzp/sydwzpgg/'
key_words = frozenset(['环保', '水务', '环境', '开发区', '萝岗', '黄埔'])

sender = 'yubo1911@163.com'
password = 'password'
receiver = 'yubo1911@163.com'
subject = '柚子的招考通知(自动发送)'
smtpserver = 'smtp.163.com'


def has_keyword(text):
    for w in key_words:
        if w in text:
            return True
    return False


def get_recruit_data(url_prefix, cls_type):
    recruit_data = []
    r = requests.get(url_prefix + 'index.html')
    r.encoding = 'gb2312'
    soup = BeautifulSoup(r.text, 'lxml')
    a_tags = soup.find_all('a')
    for a in a_tags:
        if cls_type not in a.get('class'):
            continue
        href = a.get('href')
        text = a.get_text().encode('utf-8')
        if a.get('title'):
            text = a.get('title').encode('utf-8')
        if href.startswith('./'):
            href = url_prefix + href[2:]
        if has_keyword(text):
            recruit_data.append((href, text))
            print('{} {}'.format(href, text))
    return recruit_data


def send_mail(data):
    words = ''
    for href, text in data:
        words += '{} {}\n'.format(text, href)
    if not words:
        words = '今日无招考消息'

    msg = MIMEText(words, 'plain', 'utf-8')
    msg['Subject'] = Header(subject, 'utf-8')
    msg['from'] = sender
    msg['to'] = receiver
    smtp = smtplib.SMTP()
    smtp.connect(smtpserver)
    smtp.login(sender, password)
    smtp.sendmail(sender, receiver, msg.as_string())
    smtp.quit()


def main():
    recruit_data_1 = get_recruit_data(url_prefix_1, 'rsjfont8')
    recruit_data_2 = get_recruit_data(url_prefix_2, 'sydwzp_11')
    recruit_data = recruit_data_1 + recruit_data_2
    send_mail(recruit_data)

if __name__ == '__main__':
    main()
