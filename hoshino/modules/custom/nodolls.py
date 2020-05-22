from hoshino import Service,Privilege as Priv


sv=Service('nodolls',visible=False,enable_on_default=False,manage_priv=Priv.SUPERUSER)


def dddolls(s: str):
    l = len(s)
    if l>=15:
        return
    for i in range(l//2, 1, -1):
        if s[:i] == s[i:i+i]:
            return ''.join([s[:i],s])
    return
@sv.on_message('group')
async def nodolls(bot, ctx):
    message = ctx['raw_message']
    res=dddolls(message)
    if res:
        await bot.send(ctx,res)
