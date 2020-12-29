import json
import re
import random
import os

from hoshino import Service,aiorequests,R

sv = Service('longwang',enable_on_default=False,visible=False)

@sv.on_command('迫害龙王')
async def longwang(session):
    gid = session.ctx['group_id']
    dragon_king=await session.bot.get_group_honor_info(group_id=gid,type='talkative')
    dragon_king=dragon_king['current_talkative']['user_id']
    longwanglist=list()
    longwangmelist=list()
    for lw in os.listdir(R.img('longwang/').path):
        if lw.startswith('longwangme'):
            longwangmelist.append(lw)
        else:
            longwanglist.append(lw)
    longwangme=R.img('longwang/',random.choice(longwangmelist)).cqcode
    longwangs=[R.img('longwang/',x).cqcode for x in longwanglist]
    longwangs.extend(['龙王出来挨透','龙王出来喷水'])
    if dragon_king==session.ctx['self_id']:
        session.finish(f'{longwangme}')
    reply=random.choice(longwangs)
    session.finish(f'[CQ:at,qq={dragon_king}]\n{reply}')
