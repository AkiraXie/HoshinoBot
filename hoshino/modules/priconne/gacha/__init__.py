import os
from collections import defaultdict
try:
    import ujson as json
except:
    import json

from hoshino import util
from hoshino import MessageSegment, Service, Privilege as Priv, aiorequests
from hoshino.util import silence, concat_pic, pic2b64, DailyNumberLimiter

from .gacha import Gacha
from ..chara import Chara

sv = Service('gacha')
jewel_limit = DailyNumberLimiter(7500)
tenjo_limit = DailyNumberLimiter(1)


JEWEL_EXCEED_NOTICE = f'您今天已经抽过{jewel_limit.max}钻了，欢迎明早5点后再来！'
TENJO_EXCEED_NOTICE = f'您今天已经抽过{tenjo_limit.max}张天井券了，欢迎明早5点后再来！'
POOL = ('MIX', 'JP', 'TW', 'BL')
DEFAULT_POOL = POOL[0]

_pool_config_file = os.path.expanduser('~/.hoshino/group_pool_config.json')
_group_pool = {}
try:
    with open(_pool_config_file, encoding='utf8') as f:
        _group_pool = json.load(f)
except FileNotFoundError as e:
    sv.logger.warning(
        'group_pool_config.json not found, will create when needed.')
_group_pool = defaultdict(lambda: DEFAULT_POOL, _group_pool)


def dump_pool_config():
    with open(_pool_config_file, 'w', encoding='utf8') as f:
        json.dump(_group_pool, f, ensure_ascii=False)


gacha_10_aliases = ('抽十连', '十连', '十连！', '十连抽', '来个十连', '来发十连', '来次十连', '抽个十连', '抽发十连', '抽次十连', '十连扭蛋', '扭蛋十连',
                    '10连', '10连！', '10连抽', '来个10连', '来发10连', '来次10连', '抽个10连', '抽发10连', '抽次10连', '10连扭蛋', '扭蛋10连',
                    '十連', '十連！', '十連抽', '來個十連', '來發十連', '來次十連', '抽個十連', '抽發十連', '抽次十連', '十連轉蛋', '轉蛋十連',
                    '10連', '10連！', '10連抽', '來個10連', '來發10連', '來次10連', '抽個10連', '抽發10連', '抽次10連', '10連轉蛋', '轉蛋10連')
gacha_1_aliases = ('单抽', '单抽！', '来发单抽', '来个单抽', '来次单抽', '扭蛋单抽', '单抽扭蛋',
                   '單抽', '單抽！', '來發單抽', '來個單抽', '來次單抽', '轉蛋單抽', '單抽轉蛋')
gacha_300_aliases = ('抽一井', '来一井', '来发井', '抽发井', '天井扭蛋',
                     '扭蛋天井', '天井轉蛋', '轉蛋天井', '抽井')


_collection_path = os.path.expanduser('~/.hoshino/collections')
if not os.path.exists(_collection_path):
    os.mkdir(_collection_path)


def load_user_collection(uid: str):
    collectionfile = os.path.join(_collection_path, f'{uid}.json')
    try:
        with open(collectionfile, encoding='utf8') as fp:
            ucollection = json.load(fp)
            return ucollection
    except:
        f = open(collectionfile, 'w', encoding='utf8')
        ucollection = {}
        ucollection[uid] = []
        json.dump(ucollection, f, ensure_ascii=False)
        f.close()
        return ucollection


def dump_user_collection(uid: str, ucollection):
    with open(os.path.join(_collection_path, f'{uid}.json'), 'w', encoding='utf8') as f:
        json.dump(ucollection, f, ensure_ascii=False)
        f.close()


@sv.on_command('卡池资讯', aliases=('查看卡池', '看看卡池', '康康卡池', '卡池資訊', '看看up', 'kkup','看看UP'), only_to_me=False,can_private=1)
async def gacha_info(session):
    gid = session.ctx.get('group_id',0)
    gacha = Gacha(_group_pool[str(gid)]) if gid!=0 else Gacha('MIX')
    up_chara = gacha.up
    if sv.bot.config.IS_CQPRO:
        up_chara = map(lambda x: str(
            Chara.fromname(x).icon.cqcode) + x, up_chara)
    up_chara = '\n'.join(up_chara)
    await session.send(f"本期卡池主打的角色：\n{up_chara}\nUP角色合计={(gacha.up_prob/10):.1f}% 3★出率={(gacha.s3_prob)/10:.1f}%")


POOL_NAME_TIP = '请选择以下卡池\n> 选择卡池 jp\n> 选择卡池 tw\n> 选择卡池 bilibili\n> 选择卡池 mix'
@sv.on_command('切换卡池', aliases=('选择卡池', '切換卡池', '選擇卡池'), only_to_me=False, perm=Priv.ADMIN)
async def set_pool(session):
    name = util.normalize_str(session.current_arg_text)
    if not name:
        session.finish(POOL_NAME_TIP, at_sender=True)
    elif name in ('b', 'b服', 'bl', 'bilibili', '国', '国服', 'cn'):
        name = 'BL'
    elif name in ('台', '台服', 'tw', 'sonet'):
        name = 'TW'
    elif name in ('日', '日服', 'jp', 'cy', 'cygames'):
        name = 'JP'
    elif name in ('混', '混合', 'mix'):
        name = 'MIX'
    else:
        session.finish(f'未知服务器地区 {POOL_NAME_TIP}', at_sender=True)
    gid = str(session.ctx['group_id'])
    _group_pool[gid] = name
    dump_pool_config()
    await session.send(f'卡池已切换为{name}池', at_sender=True)
    await gacha_info(session)


async def check_jewel_num(session):
    uid = session.ctx['user_id']
    if not jewel_limit.check(uid):
        await session.finish(JEWEL_EXCEED_NOTICE, at_sender=True)


async def check_tenjo_num(session):
    uid = session.ctx['user_id']
    if not tenjo_limit.check(uid):
        await session.finish(TENJO_EXCEED_NOTICE, at_sender=True)


@sv.on_command('仓库',  aliases=('看看仓库', '我的仓库'),can_private=1)
async def show_collection(session):
    uid = str(session.ctx['user_id'])
    ucollection = load_user_collection(uid)
    uset = set(ucollection[uid])
    uset.discard("未知角色")
    uset = list(uset)
    length = len(uset)
    if length <= 0:
        session.finish('您的仓库为空,请多多抽卡哦~', at_sender=True)
    else:
        result = list(map(lambda x: Chara.fromname(x), uset))
        step = 6
        pics = []
        for i in range(0, length, step):
            j = min(length, i + step)
            pics.append(Chara.gen_team_pic(
                result[i:j], star_slot_verbose=False))
        res = concat_pic(pics)
        res = pic2b64(res)
        res = MessageSegment.image(res)
    msg = [
        f'仅展示三星角色~',
        f'{res}',
        f'您共有{length}个三星角色~'
    ]
    ucollection[uid] = list(uset)
    dump_user_collection(uid, ucollection)
    await session.send('\n'.join(msg), at_sender=True)


@sv.on_command('gacha_1', aliases=gacha_1_aliases, only_to_me=False,can_private=1)
async def gacha_1(session):
    await check_jewel_num(session)
    uid = session.ctx['user_id']
    jewel_limit.increase(uid, 150)
    uid = str(session.ctx['user_id'])
    ucollection = load_user_collection(uid)
    uset = set(ucollection[uid])
    gid = session.ctx.get('group_id',0)
    gacha = Gacha(_group_pool[str(gid)]) if gid!=0 else Gacha('MIX')
    chara, hiishi = gacha.gacha_one(
        gacha.up_prob, gacha.s3_prob, gacha.s2_prob)
    silence_time = hiishi * 60
    if chara.star == 3:
        uset.add(chara.name)
    ucollection[uid] = list(uset)
    res = f'{chara.name} {"★"*chara.star}'
    if sv.bot.config.IS_CQPRO:
        res = f'{chara.icon.cqcode} {res}'
    dump_user_collection(uid, ucollection)
    if gid!=0:
        await silence(session.ctx, silence_time)
    await session.send(f'素敵な仲間が増えますよ！\n{res}', at_sender=True)


@sv.on_command('gacha_10', aliases=gacha_10_aliases, only_to_me=False,can_private=1)
async def gacha_10(session):
    SUPER_LUCKY_LINE = 170
    await check_jewel_num(session)
    uid = session.ctx['user_id']
    jewel_limit.increase(uid, 1500)
    uid = str(session.ctx['user_id'])
    ucollection = load_user_collection(uid)
    uset = set(ucollection[uid])
    gid = session.ctx.get('group_id',0)
    gacha = Gacha(_group_pool[str(gid)]) if gid!=0 else Gacha('MIX')
    result, hiishi = gacha.gacha_ten()
    silence_time = hiishi * 6 if hiishi < SUPER_LUCKY_LINE else hiishi * 60
    for c in result:
        if 3 == c.star:
            uset.add(c.name)
    ucollection[uid] = list(uset)
    if sv.bot.config.IS_CQPRO:
        res1 = Chara.gen_team_pic(result[:5], star_slot_verbose=False)
        res2 = Chara.gen_team_pic(result[5:], star_slot_verbose=False)
        res = concat_pic([res1, res2])
        res = pic2b64(res)
        res = MessageSegment.image(res)
        result = [f'{c.name}{"★"*c.star}' for c in result]
        res1 = ' '.join(result[0:5])
        res2 = ' '.join(result[5:])
        res = f'{res}\n{res1}\n{res2}'
    else:
        result = [f'{c.name}{"★"*c.star}' for c in result]
        res1 = ' '.join(result[0:5])
        res2 = ' '.join(result[5:])
        res = f'{res1}\n{res2}'
    dump_user_collection(uid, ucollection)
    if hiishi >= SUPER_LUCKY_LINE:
        await session.send('恭喜海豹！おめでとうございます！')
    await session.send(f'素敵な仲間が増えますよ！\n{res}', at_sender=True)
    if gid!=0:
        await silence(session.ctx, silence_time)


@sv.on_command('gacha_300',  aliases=gacha_300_aliases, only_to_me=False,can_private=1)
async def gacha_300(session):
    await check_tenjo_num(session)
    uid = session.ctx['user_id']
    tenjo_limit.increase(uid)
    uid = str(session.ctx['user_id'])
    ucollection = load_user_collection(uid)
    uset = set(ucollection[uid])
    gid = session.ctx.get('group_id',0)
    gacha = Gacha(_group_pool[str(gid)]) if gid!=0 else Gacha('MIX')
    result,up = gacha.gacha_tenjou()
    s3 = len(result['s3'])
    s2 = len(result['s2'])
    s1 = len(result['s1'])
    res = result['s3']
    for c in res:
        uset.add(c.name)
    ucollection[uid] = list(uset)
    dump_user_collection(uid, ucollection)
    lenth = len(res)
    if lenth <= 0:
        res = "竟...竟然没有3★？！"
    else:
        step = 4
        pics = []
        for i in range(0, lenth, step):
            j = min(lenth, i + step)
            pics.append(Chara.gen_team_pic(res[i:j], star_slot_verbose=False))
        res = concat_pic(pics)
        res = pic2b64(res)
        res = MessageSegment.image(res)

    msg = [
        f"\n素敵な仲間が増えますよ！ {res}",
        f"★★★×{s3} ★★×{s2} ★×{s1}",
        f"获得{up}个up角色与女神秘石×{50*(s3) + 10*s2 + s1}！\n第{result['first_up_pos']}抽首次获得up角色" if up else f"获得女神秘石{50*(up+s3) + 10*s2 + s1}个！"
    ]

    if up == 0 and s3 == 0:
        msg.append("太惨了，咱们还是退款删游吧...")
    elif up == 0 and s3 > 7:
        msg.append("up呢？我的up呢？")
    elif up == 0 and s3 <= 3:
        msg.append("这位酋长，大月卡考虑一下？")
    elif up == 0:
        msg.append("据说天井的概率只有12.16%")
    elif up <= 2:
        if result['first_up_pos'] < 50:
            msg.append("你的喜悦我收到了，滚去喂鲨鱼吧！")
        elif result['first_up_pos'] < 100:
            msg.append("已经可以了，您已经很欧了")
        elif result['first_up_pos'] > 290:
            msg.append("标 准 结 局")
        elif result['first_up_pos'] > 250:
            msg.append("补井还是不补井，这是一个问题...")
        else:
            msg.append("期望之内，亚洲水平")
    elif up == 3:
        msg.append("抽井母五一气呵成！您就是欧洲人？")
    elif up >= 4:
        msg.append("记忆碎片一大堆！您是托吧？")
    await session.send('\n'.join(msg), at_sender=True)
    silence_time = (100*up+50*s3 + 10*s2 + s1) * 1
    if gid!=0:
        await silence(session.ctx, silence_time)


@sv.on_rex(r'^氪金$', normalize=False)
async def kakin(bot, ctx, match):
    if ctx['user_id'] not in bot.config.SUPERUSERS:
        return
    count = 0
    for m in ctx['message']:
        if m.type == 'at' and m.data['qq'] != 'all':
            uid = int(m.data['qq'])
            jewel_limit.reset(uid)
            tenjo_limit.reset(uid)
            count += 1
    if count:
        await bot.send(ctx, f"已为{count}位用户充值完毕！谢谢惠顾～")
