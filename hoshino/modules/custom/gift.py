from hoshino import sucmd
from random import randint
@sucmd('gift',aliases=('礼物','送礼'),force_private=False)
async def gift(session):
    msg=session.ctx['message']
    for m in ctx['message']:
        if m.type == 'at' and m.data['qq'] != 'all' :
            qq = m.data['qq']
            break
    session.finish(f'[CQ:gift,qq={qq},id={randint(13)}]')