import random

import requests
import time
import json
import os
from bs4 import BeautifulSoup
import pandas as pd
import re

def fetchUrl(url, kw, page, pagesize):
    """
    url : Request Url
    kw  : Keyword
    page: Page number
    pagesize: One page size
    """
    # 请求头
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
        # "Cookie": "show_vpn=1; show_faq=1; wengine_vpn_ticketwebvpn_xjtu_edu_cn=c8b41a059b247c53; refresh=0",
        "Cookie": "show_vpn=1; show_faq=1; wengine_vpn_ticketwebvpn_xjtu_edu_cn=60010d7e08e9e0f7; refresh=0",
        "Host": "webvpn.xjtu.edu.cn"
    }

    # 请求参数
    qs = {"cds": [{"cdr": "AND",
                  "cds": [{"fld": "title", "cdr": "OR", "hlt": "true", "vlr": "OR", "val": kw},
                          {"fld": "subTitle", "cdr": "OR", "hlt": "true", "vlr": "OR", "val": kw},
                          {"fld": "introTitle", "cdr": "OR", "hlt": "true", "vlr": "OR", "val": kw},
                          {"fld": "contentText", "cdr": "OR", "hlt": "true", "vlr": "OR", "val": kw}]}],
          "obs": [{"fld": "dataTime", "drt": "DESC"}]}

    query_string_parameter = {
        "qs": json.dumps(qs),
        "tr": "A",
        "ss": 1,
        "pageNo": page,
        "pageSize": pagesize
    }

    # 发起 get 请求
    r = requests.get(url, headers=headers, params=query_string_parameter)
    # print(r.url)
    return r.text

def parseLi(webpage):
    '''
    :param webpage: 从网站接收的文本
    :return: 筛选出的信息
    '''
    soup = BeautifulSoup(webpage, "lxml")
    tag_a = soup.find_all("a", attrs={"class": "open_detail_link"})
    href_list = []
    article_url = "https://webvpn.xjtu.edu.cn"
    # article_url = "https://webvpn.xjtu.edu.cn/http/77726476706e69737468656265737421f4f6559d69206d5f6e048ce29b5a2e7b74a4"
    for a in tag_a:
        href_list.append(article_url + a.attrs["href"])
    return href_list, len(href_list)

def getText(article_url_list):
    # 请求头
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
        "Cookie": "show_vpn=1; show_faq=1; wengine_vpn_ticketwebvpn_xjtu_edu_cn=60010d7e08e9e0f7; refresh=0",
        "Host": "webvpn.xjtu.edu.cn"
    }

    web_text_list = []
    # param = {"deviceType": "COMPUTER"}
    for article_url in article_url_list:
        temp_res = requests.get(article_url, headers=headers)
        print(temp_res.url)
        web_text_list.append(temp_res.text)
        time.sleep(random.randint(0,9))
    return web_text_list

def parseText(web_text_list, n):
    # 获取文章列表
    passage_list = []
    for web in web_text_list:
        # print(web)
        n += 1
        websoup = BeautifulSoup(web, "lxml")
        try:
            title = websoup.find_all("div", attrs={"class": "title"})[0]
        except IndexError:
            print("这是第{}篇文章，没检测出标题，应该要输验证码！！".format(n))
            break
        try:
            subtitle = websoup.find_all("div", attrs={"class": "subtitle"})[0]
        except IndexError:
            subtitle = BeautifulSoup('', 'lxml')
        date = websoup.find_all("div", attrs={"class": "sha_left"})[0]
        p_list = websoup.find_all("p")
        article = ""
        for part in p_list:
            article += part.text
        # 过滤字符串中的英文，只保留中文字符和汉字
        title = re.sub('[a-zA-Z]', "", title.text)
        subtitle = re.sub('[a-zA-Z]', "", subtitle.text)
        date = re.sub('[a-zA-Z]', "", date.text).strip()
        date = re.sub('\r', "", date)
        date = re.sub('\t', "", date)
        date = re.sub('\n', "", date)
        article = re.sub('<p>', "", article)
        article = re.sub('</p>', "", article)
        passage_list.append('{}'.format(n) + '——'*50 + '\n' +
                            title + '\n' +
                            subtitle + '\n' +
                            date + '\n' +
                            article + '\n' + '——'*100 + '\n\n')
        # print(article)
    return passage_list

def saveText(passage_list):
    with open('result.txt', 'a') as f:
        for passage in passage_list:
            try:
                f.write(passage)
            except UnicodeEncodeError:
                print(passage)

# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':
    url = "https://webvpn.xjtu.edu.cn/http/77726476706e69737468656265737421f4f6559d69206d5f6e048ce29b5a2e7b74a4/rmrb/s"
    # url = "http://data.people.com.cn/rmrb/s"
    kw = "北京"
    one_page_size = 20
    all_page_num = 30
    for i in range(all_page_num):
        # 请求搜索页面
        temp_text = fetchUrl(url, kw, i + 1, one_page_size)
        # 解析搜索页面数据，获得链接列表
        href_list, href_list_len = parseLi(temp_text)
        if href_list_len == 0:
            print("没拿到链接！！")
            break
        else:
            print(href_list_len)
        # 请求内容页面
        web_text_list = getText(href_list)
        # 解析内容页面数据，获得内容字符串
        passage_list = parseText(web_text_list, n=i * one_page_size)
        # 写入数据到文件
        saveText(passage_list)
        print("已保存第{}个搜索页面".format(i+1))