import requests
import json
import re
from lxml import etree
import time
import os

requests.packages.urllib3.disable_warnings()

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3970.5 Safari/537.36',
    'Referer': 'https://www.bilibili.com/'
}



def download(homeurl,url, names, session=requests.session()):

    name = "source/"+names+".mp3"

    headers.update({'Referer': homeurl})
    session.options(url=url, headers=headers,verify=False)
    # 每次下载1M的数据
    begin = 0
    end = 1024*512-1
    flag=0
    print('进度：',end='')
    while True:
        headers.update({'Range': 'bytes='+str(begin) + '-' + str(end)})
        res = session.get(url=url, headers=headers,verify=False)
        if res.status_code != 416:
            begin = end + 1
            end = end + 1024*512
        else:
            headers.update({'Range': str(end + 1) + '-'})
            res = session.get(url=url, headers=headers,verify=False)
            flag=1
        with open(name, 'ab') as fp:
            fp.write(res.content)
            fp.flush()
            print('▓▓',end = '')


        # data=data+res.content
        if flag==1:
            print('||done')
            fp.close()
            break


def GetBiliVideo(bid,pname):

    homeurl='https://www.bilibili.com/video/'+bid
    session=requests.session()
    res = session.get(url=homeurl, headers=headers, verify=False)
    name_pat = re.compile('<title data-vue-meta="true">.*?</title>')
    name = name_pat.search(res.text)[0]

    if name == '':
        return 'none audio'
    name = name.replace('<title data-vue-meta="true">','')
    name = name.replace('</title>','')
    name = name.replace('_哔哩哔哩_bilibili','')
    print(name)

    html = etree.HTML(res.content)
    video_xml = str(html.xpath('//html/head/script[4]/text()')[0])
    video_xml = video_xml.replace('window.__playinfo__=','')


    video_json = json.loads(video_xml,strict=False)

    #VideoURL = video_json['data']['dash']['video'][0]['baseUrl']
    AudioURl = video_json['data']['dash']['audio'][0]['baseUrl']

    download(homeurl,AudioURl,names=pname,session=session) print(name)

    html = etree.HTML(res.content)
    video_xml = str(html.xpath('//html/head/script[4]/text()')[0])
    video_xml = video_xml.replace('window.__playinfo__=','')


    video_json = json.loads(video_xml,strict=False)

    #VideoURL = video_json['data']['dash']['video'][0]['baseUrl']
    AudioURl = video_json['data']['dash']['audio'][0]['baseUrl']

    download(homeurl,AudioURl,names=pname,session=session)




