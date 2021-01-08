from hoshino import  Service,Privilege as Priv
sv=Service('anti_group_recall',visible=False,enable_on_default=False,manage_priv=Priv.SUPERUSER)
@sv.on_notice('group_recall')
async def _(session):
    gid=session.event.group_id
    uid=session.event.user_id
    oid=session.event.operator_id
    msgid=session.event.message_id
    msgdic=await session.bot.get_msg(message_id=msgid)
    msg=msgdic['raw_message']
    user_dic = await session.bot.get_group_member_info(group_id=session.event.group_id, user_id=session.event.user_id,
                                               no_cache=True)
    user_card = user_dic['card'] if user_dic['card'] else user_dic['nickname']
    if oid==uid:
        await session.bot.send_group_msg(message=f'{user_card}({uid})撤回消息:\n{msg}',group_id=gid)
    else:
        await session.bot.send_group_msg(message=f'管理员撤回了{user_card}({uid})的消息:\n{msg}',group_id=gid)