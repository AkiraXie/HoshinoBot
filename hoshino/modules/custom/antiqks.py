import aiohttp
from hoshino import R, Service

sv = Service('antiqks')

qks_url = ["granbluefantasy.jp"]
qksimg = R.img('qksimg.jpg').cqcode


@sv.on_keyword(qks_url, normalize=True, event='group')
async def qks_keyword(bot, ctx):
    msg = f'?¿\n{qksimg}'
    await bot.send(ctx, msg, at_sender=True)


@sv.on_rex(r'[a-z0-9A-Z\.]{4,12}\/[a-zA-Z0-9]+', normalize=False, event='group')
async def qks_rex(bot, ctx, match):
    msg = f'?¿?¿?¿\n{qksimg}'
    res = 'http://'+match.group(0)
    async with aiohttp.TCPConnector(verify_ssl=False) as connector:
        async with aiohttp.request(
            'GET',
            url=res,
            allow_redirects=False,
            connector=connector
        ) as resp:
            h = resp.headers
            s = resp.status
    if s == 301 or s == 302:
        if 'granbluefantasy.jp' in h['Location']:
            await bot.send(ctx, msg, at_sender=True)
