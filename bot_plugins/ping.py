from nonebot.command import CommandSession
from nonebot.experimental.plugin import on_command
import requests
import random
import time
cookies={'sf-userdata':'4lB1IGK5IVrMPeX4gOGQeZAM1RFxzKIw0kFYZuPDHGo='}
s=requests.session()
headers={'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36 Edg/97.0.1072.55'}

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

def try_get(link):
    global s
    global cookies
    read_cookies()
    ans=None
    while True:
        try:
            ans=s.get(link,cookies=cookies,headers=headers)
        except:
            continue
        
        if ans.text.find('登录过期')!=-1:
            print('登录 cookies 失效，重新获取 cookies...')
            s=requests.session()
            ret=s.post('https://sfe.simpfun.cn/login-redirect.php',data={'QQ':1780615143,'pass':'robot2007','check':'on'},headers=headers)
            cookies=s.cookies
            save_cookies()
            continue

        break
    return ans

def send_score():
    random.seed()
    nowt=try_get('https://sfe.simpfun.cn/point.php?action=main').text
    
    p=nowt.find('<td>')
    p=nowt.find('<td>',p+1)
    pd=nowt.find('</td>',p+1)
    score=nowt[p+4:pd]
    p=nowt.find('<td>',p+1)
    p=nowt.find('<td>',p+1)
    pd=nowt.find('</td>',p+1)
    diamond=nowt[p+4:pd]
    
    return (score+'\n'+diamond)

@on_command('query', permission=lambda sender: sender.is_superuser)
async def _(session: CommandSession):
    sends=''
    args=session.current_arg_text.strip()
    if args=='score':
        sends=send_score()
    if args=='change':
        txt=try_get('https://sfe.simpfun.cn/point.php?&action=change').text
        p=txt.find('奖池容量')

        if txt[p+len('奖池容量')]==':':
            pd=txt.find('/div',p)
            txt=txt[p+len('奖池容量')+1:pd-1]
            
        else:
            p=txt.find('<td>',p+1)
            p+=len('<td>')
            pd=txt.find('</td>',p+1)
            txt=txt[p:pd]

        ans=int(txt)*0.5*0.01
        sends=(txt+'\n'+str(ans))

    if args=='' or args=='server':
        try:
            with open('status.txt','r+') as file:
                sends=file.read()  
        except:
            pass

    if sends=='':
        l=args.split()
        if len(l)==1 and l[0]=='rand':
            sends=str(random.randint(1,100))

        if len(l)==3 and l[0]=='rand':
            try:
                ll=int(l[1])
                r=int(l[2])
            finally:
                sends=str(random.randint(ll,r))

    if sends!='':
        await session.send(sends)

@on_command('do', permission=lambda sender: sender.is_superuser)
async def _(session: CommandSession):
    random.seed()
    sends=''
    args=session.current_arg_text.strip()
    if args=='sign':
        t=try_get('https://sfe.simpfun.cn/point.php?&action=sign').text
        tt=0
        nowp=t.find('是')
        while nowp!=-1:
            nowp=t.find('是',nowp+1)
            tt=tt+1
        
        if tt!=3:
            await session.send('冷却时间未到！')
        
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
        
        #send_myself_qq(msg)
        time.sleep(3)
        ret=try_get('http://127.0.0.1:5700/send_group_msg?group_id=710735670&message='+last).text
        if ret.find('ok')==-1:
            await session.send('发送失败！')
        else:
            await session.send('发送成功！')
        
    if args=='change':
        txt=try_get('https://sfe.simpfun.cn/point.php?action=change&change=true&times=1').text
        if txt.find('<div class="alert alert-danger">')==-1:
            p=txt.find('<div class="alert alert-success">')
            p=txt.find('<div class="alert alert-success">',p+1)
            p+=len('<div class="alert alert-success">')
            pd=txt.find('</div>',p)
            sends=txt[p:pd]
        else:
            p=txt.find('<div class="alert alert-danger">')
            p+=len('<div class="alert alert-danger">')
            pd=txt.find('</div>',p)
            sends=txt[p:pd]

    if args=='change 3':
        txt=try_get('https://sfe.simpfun.cn/point.php?action=change&change=true&times=3').text
        if txt.find('<div class="alert alert-danger">')==-1:
            p=txt.find('<div class="alert alert-success">')
            p=txt.find('<div class="alert alert-success">',p+1)
            p+=len('<div class="alert alert-success">')
            pd=txt.find('</div>',p)
            sends=txt[p:pd]
        else:
            p=txt.find('<div class="alert alert-danger">')
            p+=len('<div class="alert alert-danger">')
            pd=txt.find('</div>',p)
            sends=txt[p:pd]

    if args=='change 10':
        txt=try_get('https://sfe.simpfun.cn/point.php?action=change&change=true&times=10').text
        if txt.find('<div class="alert alert-danger">')==-1:
            p=txt.find('<div class="alert alert-success">')
            p=txt.find('<div class="alert alert-success">',p+1)
            p+=len('<div class="alert alert-success">')
            pd=txt.find('</div>',p)
            sends=txt[p:pd]
        else:
            p=txt.find('<div class="alert alert-danger">')
            p+=len('<div class="alert alert-danger">')
            pd=txt.find('</div>',p)
            sends=txt[p:pd]

    await session.send(sends)