from hoshino import Service,Privilege as Priv,aiorequests
import json
sv=Service('wangyiyun',visible=False,manage_priv=Priv.SUPERUSER,enable_on_default=False)

@sv.on_command('上号',aliases=('网抑云',"网易云","生而为人"),can_private=1)
async def shanghao(session):
    resp=await aiorequests.get('http://api.heerdev.top/nemusic/random')
    if not resp:
        session.finish("调取api失败，请稍后再试")
    j = await resp.json()
    msg=j.get('text',"调取api失败，请稍后再试")
    await session.finish(msg,at_sender=True)