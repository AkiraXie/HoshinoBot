from hoshino import Service,Privilege as Priv,sucmd
from nonebot.message import unescape
sv=Service('say',visible=False,manage_priv=Priv.SUPERUSER,enable_on_default=False)

@sv.on_command('say')
async def say(session):
    msg=session.current_arg
    try:
        await session.send(unescape(msg))
    except Exception as e:
        sv.logger.error(type(e))
        session.finish('调取say失败，请稍后再试')
@sucmd('echo',False)
async def echo(session):
    msg=session.current_arg
    try:
        await session.send(unescape(msg))
    except Exception as e:
        sv.logger.error(type(e))
        session.finish('调取echo失败，请稍后再试')