from hoshino import  Service,sucmd
from aiocqhttp.message import Message
@sucmd('ocr',aliases=('识字','文字识别'),force_private=False)
async def ooocr(session):
    msg=Message(session.current_arg)
    imglist=[
        s.data['file']
        for s in msg
        if s.type == 'image' and 'file' in s.data
    ]
    if not imglist:
        return
    count=1
    for i in imglist:
        res=await session.bot.call_action(action='.ocr_image',image=i)
        reply=[f'第{count}张图片的ocr结果是:']
        texts=res['texts']
        for t in texts:     
            reply.append(t['text'])
        await session.send('\n'.join(reply),at_sender=True)
        count+=1