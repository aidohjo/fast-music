#/usr/bin/python

import requests
import json
import re
import os
import patch

import argparse


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3970.5 Safari/537.36',
    'Referer': 'https://www.bilibili.com/'
}

def get_bid(keyword,name):
    keyword = keyword.replace(' ','+')
    #print(keyword)

    base_url = 'https://search.bilibili.com/all?keyword='+keyword+'&from_source=webtop_search&spm_id_from=333.1007&search_source=5'
    page_url = requests.get(url=base_url,headers=headers).text

    mainbid_pat = re.compile('<a href="//www.bilibili.com/video/.*?/"')
    bid = mainbid_pat.findall(page_url)[0]
    bid = bid.replace('<a href="//www.bilibili.com/video/','')
    bid = bid.replace('/"','')

    patch.GetBiliVideo(bid,name)

def data_use():
    with open('usr_data.json','rb') as f:
        tjson = f.read()
        data = json.loads(tjson)
    if data == {}:
        data.update({'User':'uname','song_num':0,'song_name':['head']})
    else:
        print(data['User'])
    bids=input('name Of song \n')
    get_bid(bids,bids)



while True:
    data_use()
    #




