#该色图功能取自tngsohack的色图api，十分感谢
from hoshino import Service, Privilege as Priv
import os
import random
from hoshino.util import FreqLimiter, DailyNumberLimiter
sv = Service('ysetu',visible=False)
_nlmt = DailyNumberLimiter(15)
_flmt = FreqLimiter(15)



def getsetu():
    return f'[CQ:image,cache=0,url=https://api.photo.lolicon.plus/stv2/]'


@sv.on_rex(r'^(不够[涩瑟色]|[涩瑟色]图|来一?[点份张].*[涩瑟色]|再来[点份张]|铜)', normalize=True)
async def pushsetu(bot, ctx, match):
    uid = ctx['user_id']
    if not _nlmt.check(uid):
        await bot.send(ctx, "您今天已经冲了15次了,请明天再来！", at_sender=True)
        return
    if not _flmt.check(uid):
        await bot.send(ctx, '您冲得太快了，请稍候再冲', at_sender=True)
        return
    _flmt.start_cd(uid)
    try:
        msg = getsetu()
        await bot.send(ctx, msg)
        _nlmt.increase(uid)
    except:
        await bot.send(ctx, '它太色了，被吃掉了QAQ')
        return
