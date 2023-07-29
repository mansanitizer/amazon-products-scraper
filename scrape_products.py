import re
from selenium.webdriver.common.action_chains import ActionChains
import time
import random
import os
import requests
import uuid
from lxml import etree
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import csv
import pandas as pd
driver = webdriver.Chrome(executable_path=ChromeDriverManager().install())
fields=['links']

session_id=""
def read():
    with open('list_copy.csv', newline='') as f:
        reader = csv.reader(f)
        your_list = list(reader)
        #print(your_list)
    for i in your_list:
        new_link_list.append(i[0])
    #print(new_link_list[0])
    new_link_list.pop(0)
    print(f'Read from list.csv. Found {len(new_link_list)} elements')

def readcsv():
    global lastrow, count_row,df2
    df2 = pd.read_csv('final_master.csv', engine='python',on_bad_lines='skip')
    lastrow= df2.iloc[-1]['Sno']
    #print("lastrow",lastrow)
    count_row = df2.shape[0]
    #print("countrow", count_row)
def combine():
    try:
        df1 = pd.read_csv('final_master.csv', engine='python',on_bad_lines='skip')
        df2 = pd.read_csv('scrape.csv', engine='python',on_bad_lines='skip')
        df3 = pd.concat([df1, df2], axis=0)
        df3.to_csv('final_master.csv', index=False)
    except:
        pass
err=0
combine()
while True:
    new_link_list = []
    read()
    h = len(new_link_list)
    readcsv()
    global count_row
    global lastrow
    g = lastrow
    a = []
    columns = ['Sno', 'URL', 'name', 'price', 'imgsrc', 'product_parent', 'product_child']
    i = count_row

    try:
        for x in range (g,-1,-1):
            #print("x=",x)
            #print(f"g= {g}")
            URL = new_link_list[x]
            #print(URL)
            HEADERS = ({'User-Agent':
                            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
                            (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36', "cookie":f"sessionid={session_id}" })

            webpage = requests.get(URL, headers=HEADERS)
            soup = BeautifulSoup(webpage.content, "html.parser")
            dom = etree.HTML(str(soup))
            try:
                name = (dom.xpath('//*[@id="productTitle"]/text()'))
                if name != []:
                    #print(name)
                    write = True
                else:
                    write = False
            except:
                name=""
                print("!")
            try:
                price = (dom.xpath('// *[@id="corePriceDisplay_desktop_feature_div"] / div[1] / span[2] / span[2] / span[2]')[0].text)
                #print(price)
            except:
                price=""
                pass
            try:
                imgsrc = (dom.xpath('//*[@id="landingImage"]/@src'))
            except:
                imgsrc=""
                pass
            try:
                product_parent = (dom.xpath('//*[@id="wayfinding-breadcrumbs_feature_div"]/ul/li[5]/span/a')[0].text)
                product_child = (dom.xpath('//*[@id="wayfinding-breadcrumbs_feature_div"]/ul/li[7]/span/a')[0].text)
                product_crumb=product_parent+">"+product_child
                #print(product_crumb)
            except:
                product_child=""
                product_parent=""
                pass
            if write == True:
                i += 1
                row=[g,URL,name,price,imgsrc,product_parent,product_child]
                #print(row)
                a.append(row)
                df = pd.DataFrame(a,columns=columns)
                df.to_csv('scrape.csv', index=False)
                df.to_csv('scrape_copy.csv', index=False)
                #print("wrote")
                randundancy=random.randint(0,100)
                if randundancy==33:
                    df.to_csv(f'scrape_redundancy_copy_{i}.csv', index=False)
                print(f'{i} done. {x} left. {(i/h)*100} percent completed. stand by')
            g-=1
            URL=""
    except:
        combine()
        err+=1
        print("combined to master final file")
        if err==3:
            g-=1
        pass

combine()