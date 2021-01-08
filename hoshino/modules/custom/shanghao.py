import string
import random
from hoshino import Service,Privilege as Priv, aiorequests
sv=Service('wangyiyun',visible=False,manage_priv=Priv.SUPERUSER,enable_on_default=False)
@sv.on_command('上号',aliases=('网抑云',"网易云","生而为人"),can_private=1)
async def shanghao(session):
    format_string=''.join(random.sample(string.ascii_letters + string.digits, 16))
    try:
        resp=await aiorequests.post(f'https://nd.2890.ltd/api/?format={format_string}')
        j =await resp.json()
    except Exception as e:
        sv.logger.exception(e)
        sv.logger.error(type(e))
        session.finish("调取api失败，请稍后再试")
    try:    
        if j['status'] !=1:
            session.finish("请求api失败")
        content=j['data']['content']['content']
    except Exception as e:
        sv.logger.exception(e)
        sv.logger.error(type(e))
        session.finish('调取api失败')
    await session.finish(content,at_sender=True)