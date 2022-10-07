from pypinyin import lazy_pinyin
from pydub import AudioSegment
import os
import re
import requests
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
res=re.search("语音key=(.*?)\\n",str(res)).group(1)
id={'任命助理':'001','交谈1':'002','交谈2':'003','交谈3':'004','晋升后交谈1':'005','晋升后交谈2':'006','信赖提升后交谈1':'007','信赖提升后交谈2':'008','信赖提升后交谈3':'009','闲置':'010','干员报到':'011','观看作战记录':'012','精英化晋升1':'013','精英化晋升2':'014','编入队伍':'017','任命队长':'018','行动出发':'019','行动开始':'020','选中干员1':'021','选中干员2':'022','部署1':'023','部署2':'024','作战中1':'025','作战中2':'026','作战中3':'027','作战中4':'028','完成高难行动':'029','3星结束行动':'030','非3星结束行动':'031','行动失败':'032','进驻设施':'033','戳一下':'034','信赖触摸':'036','标题':'037','问候':'042'}
workdir=os.getcwd()
operator=re.search('char_(\d+)_(\w+)',res).group(2) if re.search('char_(\d+)_(\w+)',res) else ""
num=re.search('char_(\d+)_(\w+)',res).group(1)
#zh=urllib.parse.unquote(re.search("(%.*)_+",url).group(1)) if re.search("([\u4e00-\u9fa5]+)",urllib.parse.unquote(re.search("(%.*)_+",url).group(1))).group(1)==urllib.parse.unquote(re.search("(%.*)_+",url).group(1)) else None
os.mkdir(workdir+"\\"+op+"\\") if not os.path.exists(workdir+"\\"+op+"\\") else print(op+"语音目录已创建！")
os.mkdir(workdir+"\\temp\\") if not os.path.exists(workdir+"\\"+"temp"+"\\") else print("缓存目录已创建")
py=lazy_pinyin(op)
pinyin=[]
for a in py:
    pinyin.append(a.title())
pinyin="".join(pinyin)
os.mkdir(workdir+"\\"+op+"\\"+"日文语音") if not os.path.exists(workdir+"\\"+op+"\\"+"日文语音") else print("日文语音目录已创建！")
for key in id:
    filename=pinyin+"_CN_"+id[key]+".wav"
    if not os.path.exists(workdir+"\\"+op+"\\"+"日文语音\\"+filename.rstrip("wav")+"mp3"):
        print("正在获取"+filename.rstrip("wav")+"mp3...")
        response=requests.get("https://static.prts.wiki/voice/"+res+"/"+op+"_"+key+".wav")
        open(workdir+"\\temp\\"+filename,"wb").write(response.content)
        mp3=AudioSegment.from_wav(workdir+"\\temp\\"+filename)
        mp3.export(workdir+"\\"+op+"\\"+"日文语音\\"+filename.rstrip("wav")+"mp3",format="mp3")
        os.remove(workdir+"\\temp\\"+filename)
        print(filename.rstrip("wav")+"mp3已获取完成！")
    else:
        print(filename.rstrip("wav")+"mp3已存在!")
os.mkdir(workdir+"\\"+op+"\\"+"中文语音") if not os.path.exists(workdir+"\\"+op+"\\"+"中文语音") else print("中文语音目录已创建！")
for key in id:
    filename=pinyin+"_zh_CN_"+id[key]+".wav"
    if not os.path.exists(workdir+"\\"+op+"\\"+"中文语音\\"+filename.rstrip("wav")+"mp3"):
        print("正在获取"+filename.rstrip("wav")+"mp3...")
        response=requests.get("https://static.prts.wiki/voice_cn/"+res+"/"+op+"_"+key+".wav")
        open(workdir+"\\temp\\"+filename,"wb").write(response.content)
        mp3=AudioSegment.from_wav(workdir+"\\temp\\"+filename)
        mp3.export(workdir+"\\"+op+"\\"+"中文语音\\"+filename.rstrip("wav")+"mp3",format="mp3")
        os.remove(workdir+"\\temp\\"+filename)
        print(filename.rstrip("wav")+"mp3已获取完成！")
    else:
        print(filename.rstrip("wav")+"mp3已存在!")
amount=0
lost=[]
for key in id:
    filename=pinyin+"_CN_"+id[key]+".wav"
    os.remove(workdir+"\\temp\\"+filename) if os.path.exists(workdir+"\\temp\\"+filename) else ""
    if os.path.exists(workdir+"\\"+op+"\\"+"日文语音\\"+filename.rstrip("wav")+"mp3"):
        amount+=1
    else:
        lost.append(filename.rstrip("wav")+"mp3")
    filename=pinyin+"_zh_CN_"+id[key]+".wav"
    if os.path.exists(workdir+"\\"+op+"\\"+"中文语音\\"+filename.rstrip("wav")+"mp3"):
        amount+=1
    else:
        lost.append(filename.rstrip("wav")+"mp3")
    os.remove(workdir+"\\temp\\"+filename) if os.path.exists(workdir+"\\temp\\"+filename) else ""
if amount==70:
    print("\n语音文件获取完成")
else:
    print("\n"+"、".join(lost).rstrip("、")+"未获取成功，请重试")
os.rmdir(workdir+"\\"+"temp"+"\\")
input("\n\n按下回车关闭窗口")
