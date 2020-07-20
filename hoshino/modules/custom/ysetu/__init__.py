#该色图功能为取自setu.db，该db由yoshino提供，不保证符合您的系统
from hoshino import Service, Privilege as Priv
import base64
import sqlite3
import os
import random
from hoshino.util import FreqLimiter, DailyNumberLimiter
sv = Service('ysetu', visible=False, enable_on_default=False,
             manage_priv=Priv.SUPERUSER)
_nlmt = DailyNumberLimiter(10)
_flmt = FreqLimiter(15)

db = sqlite3.connect(os.path.join(os.path.dirname(__file__), 'setu.db'))


def getsetu():
    setuid = random.randint(1, 4624)
    a = db.execute(f'select url from setu where id={setuid}')
    i = a.fetchall()[0][0]
    return f'[CQ:image,cache=0,url={i}]'


@sv.on_rex(r'^(不够[涩瑟色]|[涩瑟色]图|来一?[点份张].*[涩瑟色]|再来[点份张]|看过了|铜)', normalize=True)
async def pushsetu(bot, ctx, match):
    uid = ctx['user_id']
    if not _nlmt.check(uid):
        await bot.send(ctx, "您今天已经冲了10次了,请明天再来！", at_sender=True)
        return
    if not _flmt.check(uid):
        await bot.send(ctx, '您冲得太快了，请稍候再冲', at_sender=True)
        return
    _flmt.start_cd(uid)
    _nlmt.increase(uid)
    try:
        msg = getsetu()
        await bot.send(ctx, msg)
    except:
        await bot.send(ctx, '它太色了，被吃掉了QAQ')
        return
