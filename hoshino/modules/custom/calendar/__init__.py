from hoshino import Service, R, sucmd, scheduled_job
from .calendar import *
from PIL import ImageFont
from hoshino.util import text2CQ
svjp = Service('calendar-jp', enable_on_default=False)
svbl = Service('calendar-bili', enable_on_default=False)
svtw = Service('calendar-tw', enable_on_default=False)
fontpath = R.img('priconne/gadget/simhei.ttf').path
font = ImageFont.truetype(fontpath, 20)


@scheduled_job('cron', hour='*/3', jitter=40)
async def db_check_ver():
    await check_ver(svjp, 'jp')
    await check_ver(svbl, 'bili')
    await check_ver(svtw, 'tw')


@svjp.scheduled_job('cron', hour='15', minute='05')
async def push_jp_calendar():
    await svjp.broadcast(text2CQ(await db_message(svjp, 'jp'), font), 'calendar-jp')


@svbl.scheduled_job('cron', hour='15', minute='15')
async def push_bl_calendar():
    await svbl.broadcast(text2CQ(await db_message(svbl, 'bili'), font), 'calendar-bilibili')


@svtw.scheduled_job('cron', hour='15', minute='25')
async def push_bl_calendar():
    await svtw.broadcast(text2CQ(await db_message(svtw, 'tw'), font), 'calendar-tw')


@sucmd('updatedb', aliases=('更新数据库'), force_private=False)
async def forceupdatedb(session):
    codejp = await check_ver(svjp, 'jp')
    codebl = await check_ver(svbl, 'bili')
    codetw = await check_ver(svbl, 'tw')
    successcount = 0
    failcount = 0
    for i in [codebl, codejp, codetw]:
        if i == 0:
            successcount += 1
        elif i == -1:
            failcount += 1
    if failcount != 0:
        session.finish(f'检测数据库更新失败,失败数量:{failcount}.请前往后台查看')
    else:
        session.finish(f'检测数据库版本成功,{successcount}个数据库有更新')


@svbl.on_rex(r'^[bB国]服(当前|预定)?日程$', normalize=True, event='group')
async def look_bilibili_calendar(bot, ctx, match):
    is_now = match.group(1) == '当前'
    is_future = match.group(1) == '预定'
    is_all = not match.group(1)
    if is_now:
        await bot.send(ctx, text2CQ(await db_message(svbl, 'bili', 'now'), font), at_sender=True)
    if is_future:
        await bot.send(ctx, text2CQ(await db_message(svbl, 'bili', 'future'), font), at_sender=True)
    if is_all:
        await bot.send(ctx, text2CQ(await db_message(svbl, 'bili', 'all'), font), at_sender=True)


@svjp.on_rex(r'^日服(当前|预定)?日程$', normalize=True, event='group')
async def look_jp_calendar(bot, ctx, match):
    is_now = match.group(1) == '当前'
    is_future = match.group(1) == '预定'
    is_all = not match.group(1)
    if is_now:
        await bot.send(ctx, text2CQ(await db_message(svjp, 'jp', 'now'), font), at_sender=True)
    if is_future:
        await bot.send(ctx, text2CQ(await db_message(svjp, 'jp', 'future'), font), at_sender=True)
    if is_all:
        await bot.send(ctx, text2CQ(await db_message(svjp, 'jp', 'all'), font), at_sender=True)


@svtw.on_rex(r'^台服(当前|预定)?日程$', normalize=True, event='group')
async def look_tw_calendar(bot, ctx, match):
    is_now = match.group(1) == '当前'
    is_future = match.group(1) == '预定'
    is_all = not match.group(1)
    if is_now:
        await bot.send(ctx, text2CQ(await db_message(svtw, 'tw', 'now'), font), at_sender=True)
    if is_future:
        await bot.send(ctx, text2CQ(await db_message(svtw, 'tw', 'future'), font), at_sender=True)
    if is_all:
        await bot.send(ctx, text2CQ(await db_message(svtw, 'tw', 'all'), font), at_sender=True)
