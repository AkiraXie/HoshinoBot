from hoshino import sucmd, Service
from datetime import timedelta
@sucmd('setblock',aliases=('拉黑','屏蔽'),force_private=False)
async def setblock(session):
    ctx=session.ctx
    timelen=5 if len(session.current_arg_text)==0  else int(session.current_arg_text)
    count=0
    for m in ctx['message']:
        if m.type == 'at' and m.data['qq'] != 'all' :
            uid = int(m.data['qq'])
            Service.set_block_user(uid,timedelta(minutes=timelen))
            count+=1
    session.finish(f'已拉黑{count}人,嘿嘿嘿~')