#该色图功能取自tngsohack的色图api，十分感谢
from hoshino import Service, Privilege as Priv
import os
import requests
import base64
import random
from hoshino.util import FreqLimiter, DailyNumberLimiter
sv = Service('ysetu',visible=False)
_nlmt = DailyNumberLimiter(15)
_flmt = FreqLimiter(15)


def getsetu():
    urls=['https://api.photo.lolicon.plus/stv2/','http://www.dmoe.cc/random.php','https://s0.xinger.ink/acgimg/acgurl.php','https://img.ijglb.com/api.php?action=pc']
    sturl=random.choice(urls)
    resp=requests.get(sturl,timeout=5)
    img=base64.b64encode(resp.content).decode()
    return f'[CQ:image,cache=0,file=base64://{img}]'


@sv.on_command('色图',aliases=('铜','不够色','不够涩','瑟图','涩图'))
async def pushsetu(session):
    uid = session.ctx['user_id']
    if not _nlmt.check(uid):
        session.finish( "您今天已经冲了15次了,请明天再来！", at_sender=True)
    if not _flmt.check(uid):
        session.finish('您冲得太快了，请稍候再冲', at_sender=True)
    _flmt.start_cd(uid)
    try:
        msg = getsetu()
        await session.send(msg)
        _nlmt.increase(uid)
    except:
        session.finish('它太色了,被吃掉了qaq', at_sender=True)
