from hoshino import R, CommandSession, util, Service,sucmd,aiorequests
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
brank=[p4,p5,p6]
trank=[p1,p2,p3]
rrank=[p7,p8,p9]
posdic={"前":0,"中":1,"后":2}
serdic={'b':brank,'国':brank,'台':trank,'日':rrank}

async def send_rank(bot, ctx,ser,pos):
    msg=['Rank表仅供参考,具体以公会要求为准','不定期更新，来源见图']
    poslist=set([posdic[i] for i in pos]) if pos else [0,1,2]
    serlist=serdic[ser]
    for p in poslist:
        msg.append(f'{serlist[p].cqcode}')
    await bot.send(ctx, '图片较大，请稍等片刻')
    await bot.send(ctx,'\n'.join(msg))
    
    
@sv.on_rex(r'^([台国b日])服?([前中后]{0,3})rank表?', normalize=True, event='group')
async def rank_sheet(bot, ctx, match):
    await send_rank(bot,ctx,match.group(1),match.group(2))

@sv.on_command('挖矿计算', aliases=('挖矿', 'jjc钻石', '竞技场钻石', 'jjc钻石查询', '竞技场钻石查询'))
async def arena_miner(session: CommandSession):
    try:
        rank = int(session.current_arg_text)
    except:
        session.finish(f'请输入"挖矿 纯数字最高排名"', at_sender=True)
    if (rank > 15000):
        amount = 42029
    elif (rank > 12000):
        amount = (rank / 100 - 120) * 45 + 40679
    elif (rank > 11900):
        amount = 40599
    elif (rank > 7999):
        amount = (rank / 100 - 80) * 95 + 36799
    elif (rank > 4000):
        amount = (rank - 4001) + 32800
    elif (rank > 2000):
        amount = (rank - 2001) * 3 + 26800
    elif (rank > 1000):
        amount = (rank - 1001) * 5 + 21800
    elif (rank > 500):
        amount = (rank - 501) * 7 + 18300
    elif (rank > 200):
        amount = (rank - 201) * 13 + 14400
    elif (rank > 100):
        amount = (rank - 101) * 35 + 10900
    elif (rank > 10):
        amount = (rank - 11) * 60 + 5500
    elif (rank > 0):
        amount = (rank - 1) * 550
    else:
        amount = 0
    amount = int(amount)
    messages = f"矿里还剩{amount}钻石"
    await session.send(messages, at_sender=True)


yukari_pic = R.img('priconne/quick/yukari.jpg').cqcode
YUKARI_SHEET = f'''
{yukari_pic}
※大圈是1动充电对象 PvP测试
※黄骑四号位例外较多
※对面羊驼或中后卫坦 有可能歪
※我方羊驼算一号位'''
@sv.on_command('yukari_charge', aliases=('黄骑充电', '黄骑充电表', '酒鬼充电', '酒鬼充电表'))
async def yukari(session: CommandSession):
    await session.send('图片较大，请稍等片刻',)
    await session.send(YUKARI_SHEET, at_sender=True)
    await util.silence(session.ctx, 60)


@sv.on_command('star', aliases=('星级表', '升星表'))
async def star(session: CommandSession):
    await session.send(R.img('priconne/quick/star.jpg').cqcode, at_sender=True)
    await util.silence(session.ctx, 60)

byk=R.img('priconne/quick/banyuekan.jpg')
@sv.on_command('半月刊',aliases=('活动半月刊','b服半月刊','国服半月刊'))
async def banyuekan(session):
    await session.send('图片较大，请稍等片刻')
    await session.send(f'{byk.cqcode}', at_sender=True)
    await util.silence(session.ctx, 60)

'''#TODO
@sucmd('downloadquery',aliases=['下载','资料下载','下载资料'],force_private=False)
async def dlquery(session):
'''