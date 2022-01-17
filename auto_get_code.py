import requests
import random
import time
import os
cookies={'sf-userdata':'4lB1IGK5IVrMPeX4gOGQeZAM1RFxzKIw0kFYZuPDHGo='}
s=requests.session()
headers={'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36 Edg/97.0.1072.55'}
random.seed()
yqqid=123456789
login_password_to_simpfun='asdfghjkl'
admin_qq=123456789

def read_cookies():
    global cookies
    cookies={}
    with open('cookies','r+') as file:
        str=file.read()
    s1=str.split('\n')
    for s in s1:
        if len(s)==0:
            continue
        s2=s.split()
        #print(s2)
        cookies[s2[0]]=s2[1]

def save_cookies():
    with open('cookies','w+') as file:
        for keys,value in cookies.items():
            file.write(str(keys)+' '+str(value)+'\n')

def sleep(tm):
    try:
        with open('status.txt','w+') as file:
            file.write(time.asctime(time.localtime(time.time()+tm)))
    except:
        pass
    
    time.sleep(tm)

def try_get(link):
    global s
    global cookies
    ans=None
    while True:
        try:
            ans=s.get(link,cookies=cookies,headers=headers)
        except:
            continue
        
        if ans.text.find('登录过期')!=-1:
            print('登录 cookies 失效，重新获取 cookies...')
            s=requests.session()
            ret=s.post('https://sfe.simpfun.cn/login-redirect.php',data={'QQ':yqqid,'pass':login_password_to_simpfun,'check':'on'},headers=headers)
            cookies=s.cookies
            save_cookies()
            continue

        break
    return ans

def send_myself_qq(msg):
    print(msg)
    print(try_get('http://127.0.0.1:5700/send_private_msg?user_id='+str(admin_qq)+'&message='+msg).text)

nscore=''
ndiamond=''

def ask_and_send_score():
    global nscore
    global ndiamond
    nowt=try_get('https://sfe.simpfun.cn/point.php?action=main').text
    
    p=nowt.find('<td>')
    p=nowt.find('<td>',p+1)
    pd=nowt.find('</td>',p+1)
    nscore=nowt[p+4:pd]
    p=nowt.find('<td>',p+1)
    p=nowt.find('<td>',p+1)
    pd=nowt.find('</td>',p+1)
    ndiamond=nowt[p+4:pd]
    
    send_myself_qq(nscore+'\n'+ndiamond)

read_cookies()
ask_and_send_score()


def send_qq(msg):
    send_myself_qq(msg)
    sleep(3)
    ret=try_get('http://127.0.0.1:5700/send_group_msg?group_id=710735670&message='+msg).text
    if ret.find('ok')==-1:
        print(ret)
        send_myself_qq(ret+'\n消息发送失败，三小时后尝试...')
        sleep(3*60*60)
        send_myself_qq('准备重试...')
    else:
        print('发送成功')
        send_myself_qq('发送成功！')
        sleep(5)
        lscore=nscore
        ask_and_send_score()
        if lscore==nscore:
            send_myself_qq('出现 url 解析错误。请手动重试。')
            sleep(60*60)

while True:
    t=try_get('https://sfe.simpfun.cn/point.php?&action=sign').text
    tt=0
    nowp=t.find('是')
    while nowp!=-1:
        nowp=t.find('是',nowp+1)
        tt=tt+1
    
    if tt!=3:
        print('not ok,sleep at '+time.asctime())
        sleep(60*60)
        continue
    
    send_myself_qq('尝试签到开始！')
    last='error'
    while last=='error':
        try_get('https://sfe.simpfun.cn/sign_code/tncode.php?t=0.4440376631543399')
        print('--')
        for i in range(0,11):
            x=random.randint(0,190)
            txt=try_get('https://sfe.simpfun.cn/sign_code/check.php?tn_r='+str(x)).text
            print(txt)
            if txt!='error':
                last=txt
                break
    
    send_qq(last)
