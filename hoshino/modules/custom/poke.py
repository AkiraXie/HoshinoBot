from hoshino import  Service,Privilege as Priv
sv=Service('poke',visible=False,enable_on_default=False,manage_priv=Priv.SUPERUSER)
@sv.on_notice('poke')
async def poke(session):
    uid=session.event.user_id
    tid=session.event.target_id
    gid=session.event.group_id
    if tid==session.event.self_id:
        await session.bot.send_group_msg(message=f'[CQ:poke,qq={uid}]',group_id=gid)
    else:
        return 