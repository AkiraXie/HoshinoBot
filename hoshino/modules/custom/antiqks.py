import aiohttp
from hoshino import R, Service,Privilege as Priv,aiorequests

sv = Service('antiqks',visible=False,manage_priv=Priv.SUPERUSER,enable_on_default=True)

qks_url = ["granbluefantasy.jp"]
qksimg = R.img('qksimg.jpg').cqcode


@sv.on_keyword(qks_url, normalize=True, event='group')
async def qks_keyword(bot, ctx):
    msg = f'?¿\n{qksimg}'
    await bot.send(ctx, msg, at_sender=True)
async def check_gbf(url):
    resp=await aiorequests.head(url,allow_redirects=False)
    h = resp.headers
    s = resp.status_code
    if s == 301 or s == 302:
        if 'granbluefantasy.jp' in h['Location']:
            return True,h['Location']
    return False,h['Location']

#潜在的安全风险和概率影响性能，故antiqks请谨慎开启
@sv.on_rex(r'https?://[a-z0-9A-Z\.]{4,11}\/[a-zA-Z0-9]+', normalize=False, event='group')
async def qks_rex(bot, ctx, match):
    msg = f'?¿?¿?¿\n{qksimg}'
    res = match.group(0)
    a=await check_gbf(res)
    if a[0] or (await check_gbf(a[1]))[0] :
       await bot.send(ctx, msg, at_sender=True) 
    
                 
