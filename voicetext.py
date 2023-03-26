from bs4 import BeautifulSoup
import requests
import re
import urllib.parse

from pypinyin import lazy_pinyin
"""The MIT License (MIT)

Copyright (c) 2016 mozillazg, 闲耘 <hotoo.cn@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE."""

import clipboard
from dict import id

operator=input("输入干员名称：")
get_jp=input("获取日文语音列表？Y/N ")
html=requests.get("https://prts.wiki/w/"+urllib.parse.quote(operator)).text
soup=BeautifulSoup(html,features="html.parser")
py=lazy_pinyin(operator)
pinyin=[]
for a in py:
    pinyin.append(a.title())
pinyin="".join(pinyin)
zh=soup.find_all(name='div',attrs={'data-kind-name':'中文'})
jp=soup.find_all(name='div',attrs={'data-kind-name':'日文'})
content="""== 角色台词 ==\n{{Retext|N}}<br />{{Zhvoice}}\n{| class="wikitable  mw-collapsible mw-collapsed" style="background:#f9f9f9"\n|-\n! colspan="4" style="color:white;background:#333333"|台词列表\n|-\n! 场合 !! 台词 !! 日文语音 !! 中文语音\n|-\n"""
zh_text=[]
jp_text=[]
for voic in zh:
    zh_text.append(re.sub("\<div.*?\>|\</div\>","",str(voic)))
for voic in jp:
    jp_text.append(re.sub("\<div.*?\>|\</div\>","",str(voic)))
a=0
for key in id:
    content+="".join(["| ",key,"\n| ",zh_text[a],"\n"])
    if(get_jp=="Y" or get_jp=="y"):
        content+="".join(["----\n{{lj|",jp_text[a],"}}\n"])
    content+="".join(["| <sm2>",pinyin,"_CN_",id[key],".mp3</sm2>\n","| <sm2>",pinyin,"_zh_CN_",id[key],".mp3</sm2>\n|-\n"])
    a+=1
content+="|}\n\n"
clipboard.copy(content)
print(content)
input("内容已复制到剪切板中\n按回车键退出")
