from hoshino import R, CommandSession, util, Service,sucmd,aiorequests
import numpy as np
sv = Service('query')
p1 = R.img('priconne/quick/tqian.png')
p2 = R.img('priconne/quick/tzhong.png')
p3 = R.img('priconne/quick/thou.png')
p4 = R.img('priconne/quick/bqian.png')
p5 = R.img('priconne/quick/bzhong.png')
p6 = R.img('priconne/quick/bhou.png')
p7 = R.img('priconne/quick/rqian.png')
p8 = R.img('priconne/quick/rzhong.png')
p9 = R.img('priconne/quick/rhou.png')
brank=(p4,p5,p6)
trank=(p1,p2,p3)
rrank=(p7,p8,p9)
posdic={"前":0,"中":1,"后":2}
serdic={'b':brank,'国':brank,'台':trank,'日':rrank,'t':trank,'j':rrank}

async def send_rank(bot, ctx,ser,pos):
    msg=['Rank表仅供参考,以公会要求为准','不定期更新，来源见图']
    poslist=set([posdic[i] for i in pos]) if pos else [0,1,2]
    serlist=set([serdic[i] for i in ser])
    for s in serlist:
        msg.extend([f'{s[p].cqcode}' for p in poslist])
    await bot.send(ctx, '图片较大，请稍等片刻')
    await bot.send(ctx,'\n'.join(msg))
    
    
@sv.on_rex(r'^([台国日btj]{1,3})服?([前中后]{0,3})rank表?', normalize=True, event='group',can_private=1)
async def rank_sheet(bot, ctx, match):
    await send_rank(bot,ctx,match.group(1),match.group(2))




this_season = np.zeros(15001, dtype=int)
all_season = np.zeros(15001, dtype=int)

this_season[1:11] = 50
this_season[11:101] = 10
this_season[101:201] = 5
this_season[201:501] = 3
this_season[501:1001] = 2
this_season[1001:2001] = 2
this_season[2001:4000] = 1
this_season[4000:8000:100] = 50
this_season[8100:15001:100] = 15

all_season[1:11] = 500
all_season[11:101] = 50
all_season[101:201] = 30
all_season[201:501] = 10
all_season[501:1001] = 5
all_season[1001:2001] = 3
all_season[2001:4001] = 2
all_season[4001:7999] = 1
all_season[8100:15001:100] = 30

@sv.on_command('挖矿计算', aliases=('挖矿', 'jjc钻石', '竞技场钻石', 'jjc钻石查询', '竞技场钻石查询'),can_private=1)
async def arena_miner(session: CommandSession):
    try:
        rank = int(session.current_arg_text)
    except:
        return
    rank = np.clip(rank, 1, 15001)
    s_all = all_season[1:rank].sum()
    s_this = this_season[1:rank].sum()
    msg = f"\n最高排名奖励还剩{s_this}钻\n历届最高排名还剩{s_all}钻"
    session.finish(msg,at_sender=1)


yukari_pic = R.img('priconne/quick/yukari.jpg').cqcode
YUKARI_SHEET = f'''
{yukari_pic}
※大圈是1动充电对象 PvP测试
※黄骑四号位例外较多
※对面羊驼或中后卫坦 有可能歪
※我方羊驼算一号位'''
@sv.on_command('yukari_charge', aliases=('黄骑充电', '黄骑充电表', '酒鬼充电', '酒鬼充电表'),can_private=1)
async def yukari(session: CommandSession):
    await session.send('图片较大，请稍等片刻',)
    await session.send(YUKARI_SHEET, at_sender=True)
    await util.silence(session.ctx, 60)


@sv.on_command('star', aliases=('星级表', '升星表'),can_private=1)
async def star(session: CommandSession):
    await session.send(R.img('priconne/quick/star.jpg').cqcode, at_sender=True)
    await util.silence(session.ctx, 60)

byk=R.img('priconne/quick/banyuekan.jpg')
@sv.on_command('半月刊',aliases=('活动半月刊','b服半月刊','国服半月刊'),can_private=1)
async def banyuekan(session):
    await session.send('图片较大，请稍等片刻')
    await session.send(f'{byk.cqcode}', at_sender=True)
    await util.silence(session.ctx, 60)

