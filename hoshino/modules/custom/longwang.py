import json
import re
import random

from hoshino import Service,aiorequests,R

sv = Service('longwang')

@sv.on_command('迫害龙王')
async def longwang(session):
    gid = session.ctx['group_id']
    try:
        cookies = await session.bot.get_cookies(domain='qun.qq.com')
    except:
        sv.logger.warning('get cookies failed')
        session.finish('迫害失败')
    headers = {
        "cookie" : cookies['cookies']
    }
    url = f'https://qun.qq.com/interactive/honorlist?gc={gid}&type=1'
    resp=await aiorequests.post(url,headers=headers)
    text = await resp.text
    json_text = re.search('window.__INITIAL_STATE__=(.+?)</script>',text).group(1)
    data = json.loads(json_text)
    dragon_king = data['talkativeList'][0]['uin']
    if dragon_king==session.ctx['self_id']:
        longwangme=R.img('longwangme.jpg').cqcode
        session.finish(f'{longwangme}')
    n = random.randint(0, 6)
    if 0==n:
        img="龙王出来喷水"
    elif 6==n:
        img="龙王出来挨透"
    else:
        img = R.img('longwang{}.jpg'.format(n)).cqcode
    session.finish(f'[CQ:at,qq={dragon_king}]\n{img}')
