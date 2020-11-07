from hoshino import R, CommandSession, util, Service
sv = Service('query')
p1 = R.img('priconne/quick/tqian.png').cqcode
p2 = R.img('priconne/quick/tzhong.png').cqcode
p3 = R.img('priconne/quick/thou.png').cqcode
p4 = R.img('priconne/quick/bqian.png').cqcode
p5 = R.img('priconne/quick/bzhong.png').cqcode
p6 = R.img('priconne/quick/bhou.png').cqcode
p7 = R.img('priconne/quick/rqian.png').cqcode
p8 = R.img('priconne/quick/rzhong.png').cqcode
p9 = R.img('priconne/quick/rhou.png').cqcode
@sv.on_rex(r'^([台国b日])服?([前中后])rank表?', normalize=True, event='group')
async def rank_sheet(bot, ctx, match):
    is_tw = match.group(1) == '台'
    is_b = match.group(1) == 'b' or match.group(1) == '国'
    is_jp =match.group(1) == '日'
    is_qian = match.group(2) == '前'
    is_zhong = match.group(2) == '中'
    is_hou = match.group(2) == '后'
    await bot.send(ctx, '图片较大，请稍等片刻')
    if is_tw:
        if is_qian:
            await bot.send(ctx, f'台服前卫rank表：\n{p1}', at_sender=True)
            await util.silence(ctx, 60)
        if is_zhong:
            await bot.send(ctx, f'台服中卫rank表：\n{p2}', at_sender=True)
            await util.silence(ctx, 60)
        if is_hou:
            await bot.send(ctx, f'台服后卫rank表：\n{p3}', at_sender=True)
            await util.silence(ctx, 60)
    if is_b:
        if is_qian:
            await bot.send(ctx, f'b服前卫rank表：\n{p4}', at_sender=True)
            await util.silence(ctx, 60)
        if is_zhong:
            await bot.send(ctx, f'b服中卫rank表：\n{p5}', at_sender=True)
            await util.silence(ctx, 60)
        if is_hou:
            await bot.send(ctx, f'b服后卫rank表：\n{p6}', at_sender=True)
            await util.silence(ctx, 60)
    if is_jp:
        if is_qian:
            await bot.send(ctx, f'日服前卫rank表：\n{p7}', at_sender=True)
            await util.silence(ctx, 60)
        if is_zhong:
            await bot.send(ctx, f'日服中卫rank表：\n{p8}', at_sender=True)
            await util.silence(ctx, 60)
        if is_hou:
            await bot.send(ctx, f'日服后卫rank表：\n{p9}', at_sender=True)
            await util.silence(ctx, 60)

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

byk=R.img('priconne/quick/banyuekan.jpg').cqcode
@sv.on_command('半月刊',aliases=('活动半月刊','b服半月刊','国服半月刊'))
async def banyuekan(session):
    await session.send('图片较大，请稍等片刻')
    await session.send(f'{byk}', at_sender=True)
    await util.silence(session.ctx, 60)