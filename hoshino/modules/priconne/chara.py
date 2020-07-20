import os
import base64
import importlib
from io import BytesIO
from PIL import Image
import requests
import zhconv

from . import priconne_data
from hoshino import scheduled_job,aiorequests,sucmd,logger,R, ResImg


try:
    gadget_equip = R.img('priconne/gadget/equip.png').open()
    gadget_star = R.img('priconne/gadget/star.png').open()
    gadget_star_dis = R.img('priconne/gadget/star_disabled.png').open()
    gadget_star_pink = R.img('priconne/gadget/star_pink.png').open()
    unknown_chara_icon = R.img('priconne/unit/icon_unit_100031.png').open()
except Exception as e:
    logger.exception(e)


NAME2ID = {}
pcrdatapath=os.path.join(os.path.dirname(__file__),'priconne_data.py')
jsonpath=os.path.join(os.path.dirname(__file__),'gacha','config.json')

async def reload_pcrdata():
    try:
        dataget=await aiorequests.get('http://api.h-loli.cc/pcr/priconne_data.py',timeout=10)
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
        dataget=await aiorequests.get('http://api.h-loli.cc/pcr/config.json',timeout=10)
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

def download_chara_icon(id_, star):
    url = f'https://redive.estertion.win/icon/unit/{id_}{star}1.webp'
    save_path = R.img(f'priconne/unit/icon_unit_{id_}{star}1.png').path
    logger.info(f'Downloading chara icon from {url}')
    try:
        rsp = requests.get(url, stream=True, timeout=5)
    except Exception as e:
        logger.error(f'Failed to download {url}. {type(e)}')
        logger.exception(e)
    if 200 == rsp.status_code:
        img = Image.open(BytesIO(rsp.content))
        img.save(save_path)
        logger.info(f'Saved to {save_path}')
    else:
        logger.error(f'Failed to download {url}. HTTP {rsp.status_code}')


def download_card(id_, star):
    url = f'https://redive.estertion.win/card/full/{id_}{star}1.webp'
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
    if 200 == rsp.status_code:
        img = Image.open(BytesIO(rsp.content))
        img.save(save_path)
        logger.info(f'Saved to {save_path}')
    else:
        logger.error(f'Failed to download {url}. HTTP {rsp.status_code}')
    
@scheduled_job('cron',hour='01,13',minute='45',jitter=25)
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
    def gen_team_pic(team, size=64, star_slot_verbose=True):
        num = len(team)
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