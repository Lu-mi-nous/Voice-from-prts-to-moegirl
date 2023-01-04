from pypinyin import lazy_pinyin
from pydub import AudioSegment
import os
import re
import requests
from time import sleep
from tqdm import tqdm
import random
#import urllib.parse

op=input("输入干员名称以获取该干员全部语音文件：")
html=requests.get('https://m.prts.wiki/api.php', params={'action': 'query',
                                                         'prop': 'revisions',
                                                         'rvprop': 'content',
                                                         'titles': f'{op}|{op}/语音记录|后勤技能一览',
                                                         'format': 'json',
                                                         'formatversion': 'latest'
                                                        }).json()
for _ in html['query']['pages']:
    if _['title'] == op+'/语音记录':
        res = _['revisions'][0]['content']
header=['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36',
        "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14",
        "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)",
        'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
        'Opera/9.25 (Windows NT 5.1; U; en)',
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
        'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
        'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
        'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9',
        "Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Ubuntu/11.04 Chromium/16.0.912.77 Chrome/16.0.912.77 Safari/535.7",
        "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0 "]
res=re.search("语音key=(.*?)\\n",str(res)).group(1)
res2=input("特殊语音key：")
id={'任命助理':'001','交谈1':'002','交谈2':'003','交谈3':'004','晋升后交谈1':'005','晋升后交谈2':'006','信赖提升后交谈1':'007','信赖提升后交谈2':'008','信赖提升后交谈3':'009','闲置':'010','干员报到':'011','观看作战记录':'012','精英化晋升1':'013','精英化晋升2':'014','编入队伍':'017','任命队长':'018','行动出发':'019','行动开始':'020','选中干员1':'021','选中干员2':'022','部署1':'023','部署2':'024','作战中1':'025','作战中2':'026','作战中3':'027','作战中4':'028','完成高难行动':'029','3星结束行动':'030','非3星结束行动':'031','行动失败':'032','进驻设施':'033','戳一下':'034','信赖触摸':'036','标题':'037','问候':'042'}
workdir=os.getcwd()
operator=re.search('char_(\d+)_(\w+)',res).group(2) if re.search('char_(\d+)_(\w+)',res) else ""
num=re.search('char_(\d+)_(\w+)',res).group(1)
#zh=urllib.parse.unquote(re.search("(%.*)_+",url).group(1)) if re.search("([\u4e00-\u9fa5]+)",urllib.parse.unquote(re.search("(%.*)_+",url).group(1))).group(1)==urllib.parse.unquote(re.search("(%.*)_+",url).group(1)) else None
os.mkdir(workdir+"\\"+op+"\\") if not os.path.exists(workdir+"\\"+op+"\\") else print(op+"语音目录已创建！")
os.mkdir(workdir+"\\temp\\") if not os.path.exists(workdir+"\\temp\\") else print("缓存目录已创建")
py=lazy_pinyin(op)
pinyin=[]
for a in py:
    pinyin.append(a.title())
pinyin="".join(pinyin)
pinyin_=input("确认干员名称拼音（与预期不一致时输入拼音）：" + pinyin)
if pinyin_:
    pinyin=pinyin_
os.mkdir(workdir+"\\"+op+"\\日文语音") if not os.path.exists(workdir+"\\"+op+"\\日文语音") else print("日文语音目录已创建！")
pbar=tqdm(id,unit="file")
for key in pbar:
    filename=pinyin+"_CN_"+id[key]+".wav"
    if not os.path.exists(workdir+"\\"+op+"\\日文语音\\"+filename.rstrip("wav")+"mp3"):
        pbar.set_description("正在获取"+filename.rstrip("wav")+"mp3...")
        response=requests.get("https://static.prts.wiki/voice/"+res+"/"+"CN_"+id[key]+".wav",headers={'User-Agent': random.choice(header)})
        with open(workdir+"\\temp\\"+filename,"wb") as f:
            f.write(response.content)
        mp3=AudioSegment.from_wav(workdir+"\\temp\\"+filename)
        mp3.export(workdir+"\\"+op+"\\日文语音\\"+filename.rstrip("wav")+"mp3",format="mp3")
        os.remove(workdir+"\\temp\\"+filename)
        #pbar.set_description(filename.rstrip("wav")+"mp3已获取完成！")
        #sleep(0.2)
    else:
        pbar.set_description(filename.rstrip("wav")+"mp3已存在!")
    sleep(0.05)
os.mkdir(workdir+"\\"+op+"\\中文语音") if not os.path.exists(workdir+"\\"+op+"\\中文语音") else print("中文语音目录已创建！")
pbar2=tqdm(id,unit="file")
for key in pbar2:
    filename=pinyin+"_zh_CN_"+id[key]+".wav"
    if not os.path.exists(workdir+"\\"+op+"\\中文语音\\"+filename.rstrip("wav")+"mp3"):
        pbar2.set_description("正在获取"+filename.rstrip("wav")+"mp3...")
        response=requests.get("https://static.prts.wiki/voice_cn/"+res+"/"+"CN_"+id[key]+".wav",headers={'User-Agent': random.choice(header)})
        with open(workdir+"\\temp\\"+filename,"wb") as f:
            f.write(response.content)
        mp3=AudioSegment.from_wav(workdir+"\\temp\\"+filename)
        mp3.export(workdir+"\\"+op+"\\中文语音\\"+filename.rstrip("wav")+"mp3",format="mp3")
        os.remove(workdir+"\\temp\\"+filename)
        #pbar2.set_description(filename.rstrip("wav")+"mp3已获取完成！")
        #sleep(0.2)
    else:
        pbar2.set_description(filename.rstrip("wav")+"mp3已存在!")
    sleep(0.05)

if res2:
    os.mkdir(workdir+"\\"+op+"\\特殊日文语音") if not os.path.exists(workdir+"\\"+op+"\\特殊日文语音") else print("特殊日文语音目录已创建！")
    pbar=tqdm(id,unit="file")
    for key in pbar:
        filename=pinyin+"_skin1"+"_CN_"+id[key]+".wav"
        if not os.path.exists(workdir+"\\"+op+"\\特殊日文语音\\"+filename.rstrip("wav")+"mp3"):
            pbar.set_description("正在获取"+filename.rstrip("wav")+"mp3...")
            response=requests.get("https://static.prts.wiki/voice/"+res2+"/"+"CN_"+id[key]+".wav",headers={'User-Agent': random.choice(header)})
            with open(workdir+"\\temp\\"+filename,"wb") as f:
                f.write(response.content)
            mp3=AudioSegment.from_wav(workdir+"\\temp\\"+filename)
            mp3.export(workdir+"\\"+op+"\\特殊日文语音\\"+filename.rstrip("wav")+"mp3",format="mp3")
            os.remove(workdir+"\\temp\\"+filename)
            #pbar.set_description(filename.rstrip("wav")+"mp3已获取完成！")
            #sleep(0.2)
        else:
            pbar.set_description(filename.rstrip("wav")+"mp3已存在!")
        sleep(0.05)
    os.mkdir(workdir+"\\"+op+"\\特殊中文语音") if not os.path.exists(workdir+"\\"+op+"\\特殊中文语音") else print("特殊中文语音目录已创建！")
    pbar2=tqdm(id,unit="file")
    for key in pbar2:
        filename=pinyin+"_skin1"+"_zh_CN_"+id[key]+".wav"
        if not os.path.exists(workdir+"\\"+op+"\\特殊中文语音\\"+filename.rstrip("wav")+"mp3"):
            pbar2.set_description("正在获取"+filename.rstrip("wav")+"mp3...")
            response=requests.get("https://static.prts.wiki/voice_cn/"+res2+"/"+"CN_"+id[key]+".wav",headers={'User-Agent': random.choice(header)})
            with open(workdir+"\\temp\\"+filename,"wb") as f:
                f.write(response.content)
            mp3=AudioSegment.from_wav(workdir+"\\temp\\"+filename)
            mp3.export(workdir+"\\"+op+"\\特殊中文语音\\"+filename.rstrip("wav")+"mp3",format="mp3")
            os.remove(workdir+"\\temp\\"+filename)
            #pbar2.set_description(filename.rstrip("wav")+"mp3已获取完成！")
            #sleep(0.2)
        else:
            pbar2.set_description(filename.rstrip("wav")+"mp3已存在!")
        sleep(0.05)
amount=0
lost=[]
for key in id:
    filename=pinyin+"_CN_"+id[key]+".wav"
    os.remove(workdir+"\\temp\\"+filename) if os.path.exists(workdir+"\\temp\\"+filename) else ""
    if os.path.exists(workdir+"\\"+op+"\\日文语音\\"+filename.rstrip("wav")+"mp3"):
        amount+=1
    else:
        lost.append(filename.rstrip("wav")+"mp3")
    filename=pinyin+"_zh_CN_"+id[key]+".wav"
    if os.path.exists(workdir+"\\"+op+"\\中文语音\\"+filename.rstrip("wav")+"mp3"):
        amount+=1
    else:
        lost.append(filename.rstrip("wav")+"mp3")
    os.remove(workdir+"\\temp\\"+filename) if os.path.exists(workdir+"\\temp\\"+filename) else ""
if amount==70:
    print("\n语音文件获取完成")
else:
    print("\n、".join(lost).rstrip("、")+"未获取成功，请重试")
os.rmdir(workdir+"\\temp\\")
input("\n\n按下回车关闭窗口")
