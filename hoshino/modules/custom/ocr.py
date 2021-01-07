from hoshino import  Service,Privilege as Priv
sv=Service('ocr',visible=False,enable_on_default=False,manage_priv=Priv.SUPERUSER)
@sv.on_command('ocr',aliases=('识字','文字识别'),can_private=1)
async def ooocr(session):
    msg=session.ctx['message']
    imglist=[
        s.data['file']
        for s in msg
        if s.type == 'image' and 'file' in s.data
    ]
    if not imglist:
        return
    for count,i in enumerate(imglist):
        try:
            res=await session.bot.ocr_image(image=i)
        except:
            session.finish('请求ocrAPI失败')
        reply=[f'第{count+1}张图片的ocr结果是:']
        texts=res['texts']
        for t in texts:     
            reply.append(t['text'])
        await session.send('/'.join(reply),at_sender=True)
        