# -*- coding: utf-8 -*-
"""
Created on Tue Jul 12 11:10:45 2022

@author: 49923
"""

import datetime
import requests
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep
import random
import re

base_url = 'https://www.baidu.com/s?tn=news&rtt=4&bsst=1&cl=2&wd={}&medium=2&pn={}'
headers = {
          "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Mobile Safari/537.36",
          "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
          "accept-encoding": "gzip, deflate, br"
          }

def baijiahao_search(keyword, max_page, update=False):
    title_list = []
    href_list = []
    desc_list = []
    source_list = []
    text_list = []
    time_list = []
    
    if update is True:
        f = open("href.txt",'r')
        address = f.readlines()
        address = [i.replace('\n','') for i in address]
        flag = 0
        f.close()
        
    for page in range(max_page):
        print("开始爬取第{}页".format(page+1))
        wait_seconds = random.uniform(1, 2)
        print("开始等待{}秒".format(wait_seconds))
        sleep(wait_seconds)
        url = base_url.format(keyword, page*10)
        r = requests.get(url, headers=headers)
        html = r.text
        print("响应码为{}".format(r.status_code))
        soup = BeautifulSoup(html, "html.parser")
        
        url_title_list = soup.find_all(class_="news-title-font_1xS-F")
        description_list = soup.find_all(class_="c-font-normal c-color-text")
        site_list = soup.find_all(class_="news-source_Xj4Dv")
        
        #print("正在爬取：{}，共查询到{}个结果".format(url, len(url_title_list)))
        if update == True:
            for result_1 in url_title_list:
                title = re.findall('标题：.*?"',str(result_1))
                #print("title is:", title)
                href = re.findall('href=.*?pc',str(result_1))
                #print("href is:", href)
                
                if str(href)[8:-2] in address:
                    flag = 1
                    index_num = url_title_list.index(result_1)
                    break
                else:
                    print(111111)
                    title_list.append(str(title)[5:-3])
                    href_list.append(str(href)[8:-2])
                
            for result_2 in description_list[:index_num]:
                desc = re.findall('摘要.*?摘要结束',str(result_2))
                #print("desc is:", desc)
                print(222222)
                desc_list.append(str(desc)[5:-7])
        
            for result_3 in site_list[:index_num]:
                source = re.findall('新闻来源：.*?"', str(result_3))
                print(333333)
                source_list.append(str(source)[7:-3])
                
            if flag == 1:
                break    

        else:
            for result_1 in url_title_list:
                title = re.findall('标题：.*?"',str(result_1))
                #print("title is:", title)
                
                href = re.findall('href=.*?pc',str(result_1))
                #print("href is:", href)

                title_list.append(str(title)[5:-3])
                href_list.append(str(href)[8:-2])
                
            for result_2 in description_list:
                desc = re.findall('摘要.*?摘要结束',str(result_2))
                #print("desc is:", desc)
                desc_list.append(str(desc)[5:-7])
        
            for result_3 in site_list:
                source = re.findall('新闻来源：.*?"', str(result_3))
                source_list.append(str(source)[7:-3])

    for page in href_list:
        print("正在抓取网页{}的文字信息".format(page))
        r = requests.get(page, headers=headers)
        soup = BeautifulSoup(r.text, "lxml")
        text_tmp = soup.find_all("div", class_='contentText contentSize contentPadding newLandingUI')
        time_tmp = soup.find_all("span", class_='publishTime')
        
        text = re.sub('<.*?>','',str(text_tmp))
        text_list.append(text)
    
        time = re.sub('<.*?>','',str(time_tmp)).replace('[','').replace(']','')
        time = datetime.datetime.strptime(time, "%Y-%m-%d %H:%M")
        time_list.append(time)

    # print(len(title_list))
    # print(len(href_list))
    # print(len(desc_list))
    # print(len(source_list))
    # print(len(time_list))
    # print(len(text_list))
    tmp_dict = {"网页标题": title_list, "网页链接": href_list, "网页简介": desc_list, "网页来源": source_list, "网页时间":time_list, "网页内容": text_list}
    df = pd.DataFrame(tmp_dict)
    df.to_csv("text/关键词{}共{}页.csv".format(keyword, max_page*10),encoding="GB18030", index=False)
    
    #df_href = pd.DataFrame({"网页链接": href_list})
    #.to_csv("text/href.csv", encoding='utf-8',index=False)
    



    with open("href.txt","w") as f:
        for i in href_list:
            f.write(str(i)+'\n')
        f.close()
#    return title_list, href_list, desc_list, source_list, text_list, time_list





# def get_text(keyword, max_page, To_csv):
#     text_str = ""
#     title, href, _, _ = baijiahao_search(keyword, max_page, To_csv)
#     del(_)

#     for page,name in zip(href,title):
#         print("正在抓取网页{}的文字信息".format(page))
#         r = requests.get(page, headers=headers)
#         soup = BeautifulSoup(r.text, "lxml")
#         text_tmp = soup.find_all("span", class_='bjh-p')
        
#         for text in text_tmp:
#             text = re.findall('bjh-p.*?</span>', str(text))
#             text_str += str(text)[9:-9]
#             text_str = re.sub('<span class="bjh-strong">','',text_str)
        
#         name = re.findall('[\u4e00-\u9fa5a-zA-Z0-9]+',name,re.S)
#         with open('text/{}.txt'.format(name),'w') as f:
#             f.write(text_str)


if __name__ == "__main__":
    # get_text("乌克兰", 10, True)
    #title, href, desc, source, text, time = baijiahao_search("杭州水务", 5)
    baijiahao_search("杭州", 1, update=True)
    