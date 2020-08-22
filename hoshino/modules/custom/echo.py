from hoshino import Service,Privilege as Priv,aiorequests
import json
from nonebot.message import unescape
sv=Service('echo',visible=False,manage_priv=Priv.SUPERUSER,enable_on_default=False)

@sv.on_command('echo',aliases=('say'))
async def echo(session):
    msg=session.current_arg
    try:
        await session.send(unescape(msg))
    except Exception as e:
        sv.logger.error(type(e))
        session.finish('调取echo失败，请稍后再试')
    