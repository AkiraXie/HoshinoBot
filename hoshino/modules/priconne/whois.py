from hoshino.util import FreqLimiter
from .chara import Chara
from hoshino import Service
from hoshino import R
sv = Service('whois')
_lmt = FreqLimiter(5)
_lmt1 = FreqLimiter(5)


@sv.on_rex(r'^[谁誰]是\s*(.{1,20})$', normalize=False, can_private=1)
async def whois(bot, ctx, match):
    uid = ctx['user_id']
    if not _lmt.check(uid):
        await bot.send(ctx, '您查询得太快了，请稍等一会儿', at_sender=True)
        return
    _lmt.start_cd(uid)

    name = match.group(1)
    chara = Chara.fromname(name, star=0)
    if chara.id == Chara.UNKNOWN:
        msg = [f'兰德索尔似乎没有叫"{name}"的人']
        if uid not in bot.config.SUPERUSERS:
            _lmt.start_cd(uid, 300)
            msg.append('您的下次查询将于5分钟后可用')
        await bot.send(ctx, '\n'.join(msg), at_sender=True)
        return

    msg = f'\n{chara.name}\n{chara.icon.cqcode}'
    await bot.send(ctx, msg, at_sender=True)
STARDIC = {"一": 1, "二": 2, "三": 3, "四": 4, "五": 5, "六": 6}


@sv.on_rex(r'^[看查]?\s?([1-6一二三四五六][xX星])?\s?(.{1,20})(立绘|卡面)$', can_private=1)
async def lookcard(bot, ctx, match):
    uid = ctx['user_id']
    if not _lmt1.check(uid):
        await bot.send(ctx, '您查询得太快了，请稍等一会儿', at_sender=True)
        return
    _lmt1.start_cd(uid)
    name = match.group(2)
    star = match.group(1)[0] if match.group(1) else 0
    star = STARDIC.get(star, star)
    chara = Chara.fromname(name, star=int(star))
    if chara.id == Chara.UNKNOWN:
        msg = [f'兰德索尔似乎没有叫"{name}"的人']
        if uid not in bot.config.SUPERUSERS:
            _lmt1.start_cd(uid, 300)
            msg.append('您的下次查询将于5分钟后可用')
        await bot.send(ctx, '\n'.join(msg), at_sender=True)
        return
    await bot.send(ctx, "图片较大，请稍等片刻")
    msg = f'\n{chara.card}'
    await bot.send(ctx, msg, at_sender=True)
