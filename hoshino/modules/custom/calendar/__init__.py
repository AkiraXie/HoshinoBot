from hoshino import Service,R,sucmd
from .calendar import *

svjp = Service('calendar-jp', enable_on_default=False)
svbl = Service('calendar-bili', enable_on_default=False)
maiyao=R.img('maiyao.png').cqcode

@svjp.scheduled_job('cron', hour='*/3', jitter=40)
async def jp_check_ver():
    await check_ver(svjp, 'jp')


@svbl.scheduled_job('cron', hour='*/3', jitter=40)
async def bl_check_ver():
    await check_ver(svbl, 'bili')


@svjp.scheduled_job('cron',hour='5,11,17,23',minute='00')
async def push_jp_maiyao():
    await svjp.broadcast(f'{maiyao}', 'maiyao-jp')


@svbl.scheduled_job('cron',hour='0,6,12,18',minute='00')
async def push_bl_maiyao():
    await svbl.broadcast(f'{maiyao}', 'maiyao-bl')


@svjp.scheduled_job('cron', hour='15', minute='05')
async def push_jp_calendar():
    await svjp.broadcast(await db_message(svjp, 'jp'), 'calendar-jp')


@svbl.scheduled_job('cron', hour='15', minute='15')
async def push_bl_calendar():
    await svbl.broadcast(await db_message(svbl, 'bili'), 'calendar-bilibili')


@svjp.on_rex(r'^日服(当前|预定)?日程$', normalize=True, event='group')
async def look_jp_calendar(bot, ctx, match):
    is_now = match.group(1) == '当前'
    is_future = match.group(1) == '预定'
    is_all = not match.group(1)
    if is_now:
        await bot.send(ctx, await db_message(svjp, 'jp', 'now'), at_sender=True)
    if is_future:
        await bot.send(ctx, await db_message(svjp, 'jp', 'future'), at_sender=True)
    if is_all:
        await bot.send(ctx, await db_message(svjp, 'jp', 'all'), at_sender=True)

@sucmd('updatedb',aliases=('更新数据库'),force_private=False)
async def forceupdatedb(session):
    codejp=await check_ver(svjp, 'jp')
    codebl=await check_ver(svbl, 'bili')
    upcount=0
    for i in [codebl,codejp]:
        if i==0:
            upcount+=1
    if  (codebl==-1 and codejp==-1):
        session.finish('检测数据库更新失败')
    else:
        session.finish(f'检测数据库版本成功,{upcount}个数据库有更新')
        
    
@svbl.on_rex(r'^[bB国]服(当前|预定)?日程$', normalize=True, event='group')
async def look_bilibili_calendar(bot, ctx, match):
    is_now = match.group(1) == '当前'
    is_future = match.group(1) == '预定'
    is_all = not match.group(1)
    if is_now:
        await bot.send(ctx,await db_message(svbl, 'bili', 'now'), at_sender=True)
    if is_future:
        await bot.send(ctx,await db_message(svbl, 'bili', 'future'), at_sender=True)
    if is_all:
        await bot.send(ctx,await db_message(svbl, 'bili', 'all'), at_sender=True)
