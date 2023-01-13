from bs4 import BeautifulSoup
import requests
import re
import urllib.parse
from pypinyin import lazy_pinyin
import clipboard

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
id={'任命助理':'001',
    '交谈1':'002',
    '交谈2':'003',
    '交谈3':'004',
    '晋升后交谈1':'005',
    '晋升后交谈2':'006',
    '信赖提升后交谈1':'007',
    '信赖提升后交谈2':'008',
    '信赖提升后交谈3':'009',
    '闲置':'010',
    '干员报到':'011',
    '观看作战记录':'012',
    '精英化晋升1':'013',
    '精英化晋升2':'014',
    '编入队伍':'017',
    '任命队长':'018',
    '行动出发':'019',
    '行动开始':'020',
    '选中干员1':'021',
    '选中干员2':'022',
    '部署1':'023',
    '部署2':'024',
    '作战中1':'025',
    '作战中2':'026',
    '作战中3':'027',
    '作战中4':'028',
    '完成高难行动':'029',
    '3星结束行动':'030',
    '非3星结束行动':'031',
    '行动失败':'032',
    '进驻设施':'033',
    '戳一下':'034',
    '信赖触摸':'036',
    '标题':'037',
    '问候':'042'}
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
