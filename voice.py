from pypinyin import lazy_pinyin
from pydub import AudioSegment
import os
import re
import requests
from time import sleep
from tqdm import tqdm
import random
from dict import *
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
res2=input("特殊语音key：")
workdir=os.getcwd()
operator=re.search('char_(\d+)_(\w+)',res).group(2) if re.search('char_(\d+)_(\w+)',res) else ""
num=re.search('char_(\d+)_(\w+)',res).group(1)
#zh=urllib.parse.unquote(re.search("(%.*)_+",url).group(1)) if re.search("([\u4e00-\u9fa5]+)",urllib.parse.unquote(re.search("(%.*)_+",url).group(1))).group(1)==urllib.parse.unquote(re.search("(%.*)_+",url).group(1)) else None
os.mkdir(workdir+"\\"+op+"\\") if not os.path.exists(workdir+"\\"+op+"\\") else print(op+"语音目录已存在！")
os.mkdir(workdir+"\\temp\\") if not os.path.exists(workdir+"\\temp\\") else print("缓存目录已存在")
py=lazy_pinyin(op)
pinyin=[]
for a in py:
    pinyin.append(a.title())
pinyin="".join(pinyin)
pinyin_=input("确认干员名称拼音（与预期不一致时输入拼音）：" + pinyin)
if pinyin_:
    pinyin=pinyin_
def download(lang:str,kind="",res=res):
    zh="_zh" if lang=="中文" else ""
    cn="_cn" if lang=="中文" else ""
    if kind:
        zh="_skin1"+zh
    os.mkdir(workdir+"\\"+op+"\\"+kind+lang+"语音") if not os.path.exists(workdir+"\\"+op+"\\"+kind+lang+"语音") else print(""+kind+lang+"语音目录已存在！")
    pbar=tqdm(id,unit="file")
    for key in pbar:
        filename=pinyin+zh+"_CN_"+id[key]+".wav"
        if not os.path.exists(workdir+"\\"+op+"\\"+kind+lang+"语音\\"+filename.rstrip("wav")+"mp3"):
            pbar.set_description("正在获取"+filename.rstrip("wav")+"mp3...")
            response=requests.get("https://static.prts.wiki/voice"+cn+"/"+res+"/"+"CN_"+id[key]+".wav",headers={'User-Agent': random.choice(header)})
            with open(workdir+"\\temp\\"+filename,"wb") as f:
                f.write(response.content)
            mp3=AudioSegment.from_wav(workdir+"\\temp\\"+filename)
            mp3.export(workdir+"\\"+op+"\\"+kind+lang+"语音\\"+filename.rstrip("wav")+"mp3",format="mp3")
            os.remove(workdir+"\\temp\\"+filename)
            #pbar.set_description(filename.rstrip("wav")+"mp3已获取完成！")
            #sleep(0.2)
        else:
            pbar.set_description(filename.rstrip("wav")+"mp3已存在!")
        sleep(0.05)

download("日文")
download("中文")
if res2:
    download("日文",kind="特殊",res=res2)
    download("中文",kind="特殊",res=res2)
#amount=0
#lost=[]
#for key in id:
#    filename=pinyin+"_CN_"+id[key]+".wav"
#    os.remove(workdir+"\\temp\\"+filename) if os.path.exists(workdir+"\\temp\\"+filename) else ""
#    if os.path.exists(workdir+"\\"+op+"\\日文语音\\"+filename.rstrip("wav")+"mp3"):
#        amount+=1
#    else:
#        lost.append(filename.rstrip("wav")+"mp3")
#    filename=pinyin+"_zh_CN_"+id[key]+".wav"
#    if os.path.exists(workdir+"\\"+op+"\\中文语音\\"+filename.rstrip("wav")+"mp3"):
#        amount+=1
#    else:
#        lost.append(filename.rstrip("wav")+"mp3")
#    os.remove(workdir+"\\temp\\"+filename) if os.path.exists(workdir+"\\temp\\"+filename) else ""
#if amount==70:
#    print("\n语音文件获取完成")
#else:
#    print("\n、".join(lost).rstrip("、")+"未获取成功，请重试")
os.rmdir(workdir+"\\temp\\")
input("\n\n按下回车关闭窗口")
