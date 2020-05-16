
import random
from hoshino import R, CommandSession,Service

sv1=Service('justplay')
qks_url = ["granbluefantasy.jp"]
qksimg = R.img('priconne/quick/qksimg.jpg').cqcode
nothing = R.img('priconne/quick/我什么都没有.png').cqcode
prof = R.img('priconne/quick/专业团队.png').cqcode
longtree = R.img('priconne/quick/大树.jpg').cqcode
shorttree = R.img('priconne/quick/小树.jpg').cqcode
multisp=R.img('priconne/quick/多人运动.jpg').cqcode

@sv1.on_keyword(qks_url, normalize=True, event='group')
async def qks(bot, ctx):
    msg = f'爪巴\n{qksimg}'
    await bot.send(ctx, msg, at_sender=True)


@sv1.on_keyword(('我什么都没有'))
async def havenothing(bot, ctx):
    a = random.randint(1, 100)
    if a <= 10:
        await bot.send(ctx,f'{nothing}')


@sv1.on_command('professional', aliases=('专业团队', '黑人抬棺'), only_to_me=False)
async def profe(session: CommandSession):
    await session.send(f'{prof}')


@sv1.on_command('duorenyundong', aliases=('多人运动','三人忘刀'), only_to_me=False)
async def multisport(session: CommandSession):
    await session.send(f'{multisp}')


@sv1.on_keyword(('挂树', '查树'))
async def tree(bot, ctx):
    a = random.randint(1, 1000)
    if a <= 10:
        await bot.send(ctx,f'{longtree}')
    elif a <= 110:
        await bot.send(ctx,f'{shorttree}')