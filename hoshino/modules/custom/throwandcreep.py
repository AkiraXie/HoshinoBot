from hoshino import Service,Privilege as Priv,aiorequests,MessageSegment,R
from hoshino.util import pic2b64
from PIL import Image, ImageDraw
import random
from io import BytesIO
import os
sv=Service('throwandcreep',enable_on_default=False,visible=False,manage_priv=Priv.SUPERUSER)
base_path=R.img(f'throwandcreep/').path
os.makedirs(os.path.join(base_path,'pa'),exist_ok=True)


def get_circle_avatar(avatar, size):
    avatar.thumbnail((size, size))
    scale = 5
    mask = Image.new('L', (size*scale, size*scale), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, size * scale, size * scale), fill=255)
    mask = mask.resize((size, size), Image.ANTIALIAS)
    ret_img = avatar.copy()
    ret_img.putalpha(mask)
    return ret_img

async def throw(qq):
    avatar_url=f'http://q1.qlogo.cn/g?b=qq&nk={qq}&s=640'
    imgres=await aiorequests.get(avatar_url)
    if not imgres:
        return -1
    img=await imgres.content
    avatar = Image.open(BytesIO(img)).convert('RGBA')
    avatar = get_circle_avatar(avatar, 139)
    randomangle=random.randrange(360)
    throw_img=Image.open(os.path.join(base_path,'throw.jpg'))
    throw_img.paste(avatar.rotate(randomangle),(17, 180),avatar.rotate(randomangle))
    throw_img=pic2b64(throw_img)
    throw_img=str(MessageSegment.image(throw_img))
    return throw_img

async def creep(qq):
    cid = random.randint(0, 53)
    avatar_url=f'http://q1.qlogo.cn/g?b=qq&nk={qq}&s=640'
    imgres=await aiorequests.get(avatar_url)
    if not imgres:
        return -1
    img=await imgres.content
    avatar = Image.open(BytesIO(img)).convert('RGBA')
    avatar = get_circle_avatar(avatar, 100)
    creep_img = Image.open(os.path.join(base_path,'pa',f'爬{cid}.jpg')).convert('RGBA')
    creep_img = creep_img.resize((500, 500), Image.ANTIALIAS)
    creep_img.paste(avatar, (0, 400, 100, 500), avatar)
    creep_img=pic2b64(creep_img)
    creep_img=str(MessageSegment.image(creep_img))
    return creep_img

@sv.on_keyword(('丟','dio'))
async def diu(bot,ctx):
    qq=''
    msg=ctx['message']
    for segment in msg:
        if segment['type'] == 'at':
            qq= segment['data']['qq']
            break
    if qq == '' or qq== 'all':
        await bot.send(ctx,'丢丢失败，请at单一群友')
        return
    reply=await throw(qq)
    if isinstance(reply,str):
        await bot.send(ctx,f'{reply}')
    else:
        await bot.send(ctx,'丢丢失败，请稍后再试')
@sv.on_keyword(('爬','爪巴'))
async def pa(bot,ctx):
    qq=''
    msg=ctx['message']
    for segment in msg:
        if segment['type'] == 'at':
            qq= segment['data']['qq']
            break
    if qq == '' or qq== 'all':
        await bot.send(ctx,'爬爬失败，请at单一群友')
        return
    reply=await creep(qq)
    if isinstance(reply,str):
        await bot.send(ctx,f'{reply}')
    else:
        await bot.send(ctx,'爬爬失败，请稍后再试')