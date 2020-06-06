from hoshino import R,CommandSession,Service,Privilege as Priv
import base64
from hoshino import aiorequests
sv=Service('xsetu',visible=False,enable_on_default=False,manage_priv=Priv.SUPERUSER)




async def getsetu():
    resp=await aiorequests.get('https://api.loli.com.se')
    img=base64.b64encode(await resp.content).decode()
    return f'[CQ:image,cache=0,file=base64://{img}]'


@sv.on_rex(r'^(不够[涩瑟色]|[涩瑟色]图|来一?[点份张].*[涩瑟色]|再来[点份张]|看过了|铜)', normalize=True)
async def pushsetu(bot, ctx, match):
    try:
        msg=await getsetu()
        await bot.send(ctx,msg)
    except:
        await bot.send(ctx,'它太色了，被吃掉了QAQ')
        return
