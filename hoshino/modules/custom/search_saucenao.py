from hoshino import Service,Privilege as Priv,MessageSegment
from saucenao_api import SauceNao

sv = Service('saucenao',visible=False,manage_priv=Priv.SUPERUSER,enable_on_default=False)


@sv.on_command('搜索图片',aliases=('识图','搜图'))
async def searchpic(session):
    piclist=session.current_arg_images
    if len(piclist)==0:
        session.finish('未识别到图片,请发送图片以识别',at_sender=True)
    sauce=SauceNao()
    for i in piclist:
        count=1
        reply=[]
        res=sauce.from_url(i)
        if not res:
            await session.send(f'第{count}张图识别失败,请稍后再试',at_sender=True)
            continue
        best=res[0]
        reply.append('相似度:'+str(best.similarity)+'%')
        reply.append('标题:「'+best.title+'」')
        reply.append('作者:「'+best.author+'」')
        reply.append(f'[CQ:image,cache=0,file={best.thumbnail}]')
        reply.append('图片地址:'+best.url)
        await session.send('\n'.join(reply))
        count=count+1