import os
import base64
import importlib
from io import BytesIO
from PIL import Image,ImageDraw,ImageFont
import requests
import zhconv

from . import priconne_data,pcrdatapath,jsonpath
from hoshino import scheduled_job,aiorequests,sucmd,logger,R, ResImg


try:
    gadget_equip = R.img('priconne/gadget/equip.png').open()
    gadget_star = R.img('priconne/gadget/star.png').open()
    gadget_star_dis = R.img('priconne/gadget/star_disabled.png').open()
    gadget_star_pink = R.img('priconne/gadget/star_pink.png').open()
    unknown_chara_icon = R.img('priconne/unit/icon_unit_100031.png').open()
except Exception as e:
    logger.exception(e)
os.makedirs(R.img(f'priconne/gadget/').path,exist_ok=True)
os.makedirs(R.img(f'priconne/card/').path,exist_ok=True)
os.makedirs(R.img(f'priconne/unit/').path,exist_ok=True)
NAME2ID = {}

#更新数据
async def reload_pcrdata():
    try:
        dataget=await aiorequests.get('http://api.akiraxie.me/pcr/priconne_data.py',timeout=5)
        datacon=await dataget.content
    except Exception as e:
        logger.error(f'连接服务器失败. {type(e)}')
        logger.exception(e)
        return 1
    if 200!=dataget.status_code:
        logger.warning('连接服务器失败')
        return 1
    with open(pcrdatapath, 'wb') as f:
        f.write(datacon)
        f.close()
    reload_data()
    logger.info('更新角色数据成功')
    return 0
def reload_data():
    importlib.reload(priconne_data)
    gen_name2id()
    logger.info('重载角色数据成功')

async def reload_config():
    try:
        dataget=await aiorequests.get('http://api.akiraxie.me/pcr/config.json',timeout=5)
        datacon=await dataget.content
    except Exception as e:
        logger.error(f'连接服务器失败. {type(e)}')
        logger.exception(e)
        return 1
    if 200!=dataget.status_code:
        logger.warning('连接服务器失败')
        return 1
    with open(jsonpath, 'wb') as f:
        f.write(datacon)
        f.close()
    importlib.reload(priconne_data)
    gen_name2id()
    logger.info('更新卡池配置成功')
    return 0

def download_chara_icon(id_, star,rurl='https://redive.estertion.win/icon/unit/'):
    url = rurl+f'{id_}{star}1.webp'
    save_path = R.img(f'priconne/unit/icon_unit_{id_}{star}1.png').path
    logger.info(f'Downloading chara icon from {url}')
    try:
        rsp = requests.get(url, stream=True, timeout=5)
    except Exception as e:
        logger.error(f'Failed to download {url}. {type(e)}')
        logger.exception(e)
        return 1,star
    if 200 == rsp.status_code:
        img = Image.open(BytesIO(rsp.content))
        img.save(save_path)
        logger.info(f'Saved to {save_path}')
        return 0,star
    else:
        logger.error(f'Failed to download {url}. HTTP {rsp.status_code}')
        return 1,star


def download_card(id_, star,rurl='https://redive.estertion.win/card/full/'):
    url = rurl+f'{id_}{star}1.webp'
    save_path = R.img(f'priconne/card/{id_}{star}1.png').path
    if star==1:
        url = f'https://redive.estertion.win/card/profile/{id_}11.webp'
        save_path = R.img(f'priconne/card/{id_}11.png').path
    logger.info(f'Downloading card from {url}')
    try:
        rsp = requests.get(url, stream=True, timeout=5)
    except Exception as e:
        logger.error(f'Failed to download {url}. {type(e)}')
        logger.exception(e)
        return 1,star
    if 200 == rsp.status_code:
        img = Image.open(BytesIO(rsp.content))
        img.save(save_path)
        logger.info(f'Saved to {save_path}')
        return 0,star
    else:
        logger.error(f'Failed to download {url}. HTTP {rsp.status_code}')
        return 1,star

@scheduled_job('cron',hour='0,12',minute='40',jitter=20)
async def updatedata():
    await reload_pcrdata()
    await reload_config()

def gen_name2id():
    NAME2ID.clear()
    for k, v in priconne_data._PriconneData.CHARA.items():
        for s in v:
            if s not in NAME2ID:
                NAME2ID[normname(s)] = k
            else:
                logger.warning(f'Chara.__gen_name2id: 出现重名{s}于id{k}与id{NAME2ID[s]}')


def normname(name:str) -> str:
    name = name.lower().replace('（', '(').replace('）', ')')
    name = zhconv.convert(name, 'zh-hans')
    return name

class Chara:

    UNKNOWN = 1000

    def __init__(self, id_, star=3, equip=0):
        self.id = id_
        self.star = star
        self.equip = equip


    @staticmethod
    def fromid(id_, star=3, equip=0):
        '''Create Chara from her id. The same as Chara()'''
        return Chara(id_, star, equip)


    @staticmethod
    def fromname(name, star=3, equip=0):
        '''Create Chara from her name.'''
        id_ = Chara.name2id(name)
        return Chara(id_, star, equip)


    @property
    def name(self):
        return priconne_data._PriconneData.CHARA[self.id][0] if self.id in priconne_data._PriconneData.CHARA else priconne_data._PriconneData.CHARA[Chara.UNKNOWN][0]


    @property
    def icon(self) -> ResImg:
        if self.star==0 or self.star==6:
            star='6'
        elif 3<=self.star<=5:
            star='3'
        else :
            star="1"
        res = R.img(f'priconne/unit/icon_unit_{self.id}{star}1.png')
        if not res.exist:
            res = R.img(f'priconne/unit/icon_unit_{self.id}31.png')
        if not res.exist:
            res = R.img(f'priconne/unit/icon_unit_{self.id}11.png')
        if not res.exist:
            download_chara_icon(self.id, 6)
            download_chara_icon(self.id, 3)
            download_chara_icon(self.id, 1)
            res = R.img(f'priconne/unit/icon_unit_{self.id}{star}1.png')
        if not res.exist:
            res = R.img(f'priconne/unit/icon_unit_{self.id}31.png')
        if not res.exist:
            res = R.img(f'priconne/unit/icon_unit_{self.id}11.png')
        if not res.exist:#should never reach here
            res = R.img(f'priconne/unit/icon_unit_{UNKNOWN}31.png')
        return res


    @property
    def card(self):
        if self.star==0 or self.star==6:
            star='6'
        elif 3<=self.star<=5:
            star='3'
        else :
            star="1"
        tip=f"{self.name}{star}星卡面：\n"
        res = R.img(f'priconne/card/{self.id}{star}1.png')
        if not res.exist:
            if self.star==6:
                tip=f"{self.name}没有6星卡面，将展示3星卡面：\n"
            else:
                tip=f"{self.name}3星卡面：\n"
            res = R.img(f'priconne/card/{self.id}31.png')
        if not res.exist:
            tip=f"{self.name}1星卡面：\n"
            res = R.img(f'priconne/card/{self.id}11.png')
        if not res.exist:
            download_card(self.id, 6)
            download_card(self.id, 3)
            download_card(self.id, 1)
            tip=f"{self.name}{star}星卡面：\n"
            res = R.img(f'priconne/card/{self.id}{star}1.png')
        if not res.exist:
            if self.star==6:
                tip=f"{self.name}没有6星卡面，将展示3星卡面：\n"
            else:
                tip=f"{self.name}3星卡面：\n"
            res = R.img(f'priconne/card/{self.id}31.png')
        if not res.exist:
            tip=f"{self.name}1星卡面：\n"
            res = R.img(f'priconne/card/{self.id}11.png')
        if not res.exist:#should never reach here
            tip=""
            res = R.img(f'priconne/unit/icon_unit_{UNKNOWN}31.png')
        return tip+f'{res.cqcode}'

    def gen_icon_img(self, size, star_slot_verbose=True) -> Image:
        try:
            pic = self.icon.open().convert('RGBA').resize((size, size), Image.LANCZOS)
        except FileNotFoundError:
            logger.error(f'File not found: {self.icon.path}')
            pic = unknown_chara_icon.convert('RGBA').resize((size, size), Image.LANCZOS)

        l = size // 6
        star_lap = round(l * 0.15)
        margin_x = ( size - 6*l ) // 2
        margin_y = round(size * 0.05)
        if self.star:
            for i in range(5 if star_slot_verbose else min(self.star, 5)):
                a = i*(l-star_lap) + margin_x
                b = size - l - margin_y
                s = gadget_star if self.star > i else gadget_star_dis
                s = s.resize((l, l), Image.LANCZOS)
                pic.paste(s, (a, b, a+l, b+l), s)
            if 6 == self.star:
                a = 5*(l-star_lap) + margin_x
                b = size - l - margin_y
                s = gadget_star_pink
                s = s.resize((l, l), Image.LANCZOS)
                pic.paste(s, (a, b, a+l, b+l), s)
        if self.equip:
            l = round(l * 1.5)
            a = margin_x
            b = margin_x
            s = gadget_equip.resize((l, l), Image.LANCZOS)
            pic.paste(s, (a, b, a+l, b+l), s)
        return pic


    @staticmethod
    def gen_team_pic(team, size=64, star_slot_verbose=True,text=None):
        num = len(team)
        if isinstance(text,str):
            des = Image.new('RGBA', (num*size+77, size), (255, 255, 255, 255))
            tfont = ImageFont.truetype(R.img('priconne/gadget/FZY3K.TTF').path,16)
            timg = Image.new('RGBA', (72, 64) ,(255, 255, 255, 255))
            dra = ImageDraw.Draw(timg)
            dra = dra.text((3,3), text, font=tfont,fill="#000000")
            img = Image.new('RGBA', (20, 40), (255, 255, 255, 255))
            like = Image.open(R.img('priconne/gadget/like.png').path)
            dislike = Image.open(R.img('priconne/gadget/dislike.png').path)
            dislike.thumbnail((20, 20))
            like.thumbnail((20, 20))
            img.paste(like, (0, 0), like)
            img.paste(dislike, (0, 20), dislike)
            des.paste(timg, (num * size, 0), timg)
            des.paste(img, (num * size, 24), img)
        else:
            des = Image.new('RGBA', (num*size, size), (255, 255, 255, 255))
        for i, chara in enumerate(team):
            src = chara.gen_icon_img(size, star_slot_verbose)
            des.paste(src, (i * size, 0), src)
        return des
    
    @staticmethod
    def name2id(name):
        name = normname(name)
        if not NAME2ID:
            gen_name2id()
        return NAME2ID[name] if name in NAME2ID else Chara.UNKNOWN
gen_name2id()
@sucmd('更新卡池',aliases=('更新数据'),force_private=False)
async def forceupdate(session):
    code_1=await reload_config()
    code_2=await reload_pcrdata()
    if code_1==0 and code_2==0:
        session.finish('更新卡池和数据成功')
    else:
        session.finish('更新卡池和数据失败，请前往后台查看')
@sucmd('重载角色数据',aliases=('重载花名册'),force_private=False)
async def forcereload(session):
    reload_data()
    session.finish('重载数据成功')
STARS=[1,3,6]
@sucmd('downloadicon',aliases=('下载头像',"下载icon"),force_private=False)
async def iconcmd(session):
    msgs=session.current_arg_text.split()
    charas=list(map(lambda x:Chara.fromid(int(x)) if x.isdigit() else Chara.fromname(x),msgs))
    replys=["本次下载头像情况:"]
    for c in charas:
        for star in STARS:
            code,s=download_chara_icon(c.id,star)
            status='成功' if code==0 else '失败'
            replys.append(f'name:{c.name},id:{c.id},star:{s},下载头像{status}')
    session.finish('\n'.join(replys))
@sucmd('downloadcard',aliases=('下载卡面','下载card','下载立绘'),force_private=False)
async def cardcmd(session):
    msgs=session.current_arg_text.split()
    charas=list(map(lambda x:Chara.fromid(int(x)) if x.isdigit() else Chara.fromname(x),msgs))
    replys=["本次下载卡面情况:"]
    for c in charas:
        for star in STARS:
            code,s=download_card(c.id,star)
            status='成功' if code==0 else '失败'
            replys.append(f'name:{c.name},id:{c.id},star:{s},下载卡面{status}')
    session.finish('\n'.join(replys))
@sucmd('downloadticon',aliases=('下载t头像',"下载ticon"),force_private=False)
async def ticoncmd(session):
    msgs=session.current_arg_text.split()
    charas=list(map(lambda x:Chara.fromid(int(x)) if x.isdigit() else Chara.fromname(x),msgs))
    replys=["本次下载头像情况:"]
    for c in charas:
        for star in STARS:
            code,s=download_chara_icon(c.id,star,'https://api.redive.lolikon.icu/icon/icon_unit_')
            status='成功' if code==0 else '失败'
            replys.append(f'name:{c.name},id:{c.id},star:{s},下载头像{status}')
    session.finish('\n'.join(replys))
@sucmd('downloadtcard',aliases=('下载t卡面','下载tcard','下载t立绘'),force_private=False)
async def tcardcmd(session):
    msgs=session.current_arg_text.split()
    charas=list(map(lambda x:Chara.fromid(int(x)) if x.isdigit() else Chara.fromname(x),msgs))
    replys=["本次下载卡面情况:"]
    for c in charas:
        for star in STARS[1:]:
            code,s=download_card(c.id,star,'https://api.redive.lolikon.icu/bg_still/bg_still_')
            status='成功' if code==0 else '失败'
            replys.append(f'name:{c.name},id:{c.id},star:{s},下载卡面{status}')
    session.finish('\n'.join(replys))