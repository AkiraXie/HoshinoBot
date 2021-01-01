import re
import time
from collections import defaultdict

from nonebot import CommandSession, MessageSegment, get_bot
from hoshino.util import silence, concat_pic, pic2b64, FreqLimiter
from hoshino.service import Service, Privilege as Priv

sv = Service('pcr-arena', manage_priv=Priv.SUPERUSER)

from ..chara import Chara
from . import arena

DISABLE_NOTICE = '本群竞技场查询功能已禁用\n如欲开启，请与维护组联系'

lmt = FreqLimiter(5)

aliases = ('怎么拆', '怎么解', '怎么打', '如何拆', '如何解', '如何打', '怎麼拆', '怎麼解', '怎麼打', 'jjc查询', 'jjc查詢')
aliases_b = tuple('b' + a for a in aliases) + tuple('B' + a for a in aliases)+tuple('国' + a for a in aliases)
aliases_tw = tuple('台' + a for a in aliases)
aliases_jp = tuple('日' + a for a in aliases)

@sv.on_command('竞技场查询', aliases=aliases, deny_tip=DISABLE_NOTICE, only_to_me=False,can_private=1)
async def arena_query(session:CommandSession):
    await _arena_query(session, region=1)

@sv.on_command('b竞技场查询', aliases=aliases_b, deny_tip=DISABLE_NOTICE, only_to_me=False,can_private=1)
async def arena_query_b(session:CommandSession):
    await _arena_query(session, region=2)

@sv.on_command('台竞技场查询', aliases=aliases_tw, deny_tip=DISABLE_NOTICE, only_to_me=False,can_private=1)
async def arena_query_tw(session:CommandSession):
    await _arena_query(session, region=3)

@sv.on_command('日竞技场查询', aliases=aliases_jp, deny_tip=DISABLE_NOTICE, only_to_me=False,can_private=1)
async def arena_query_jp(session:CommandSession):
    await _arena_query(session, region=4)


async def _arena_query(session:CommandSession, region:int):

    arena.refresh_quick_key_dic()
    uid = session.ctx['user_id']

    if not lmt.check(uid):
        session.finish('您查询得过于频繁，请稍等片刻', at_sender=True)
    lmt.start_cd(uid)

    # 处理输入数据
    argv = session.current_arg_text.strip()
    argv = re.sub(r'[?？，,_]', ' ', argv)
    argv = argv.split()
    if 0 >= len(argv):
        session.finish('请输入防守方角色，用空格隔开', at_sender=True)
    if 5 < len(argv):
        session.finish('编队不能多于5名角色', at_sender=True)
    defen = [ Chara.name2id(name) for name in argv ]
    if len(defen) <5:
        session.finish('由于pcrdfans.com的限制，编队必须为5个角色', at_sender=True)
    for i, id_ in enumerate(defen):
        if Chara.UNKNOWN == id_:
            session.finish(f'编队中含未知角色"{argv[i]}"', at_sender=True)
    if len(defen) != len(set(defen)):
        await session.finish('编队中出现重复角色', at_sender=True)
    if 1004 in defen:
        await session.send('\n⚠️您正在查询普通版炸弹人\n※万圣版可用万圣炸弹人/瓜炸等别称', at_sender=True)
    # 执行查询
    sv.logger.info('Doing query...')
    try:
        res = await arena.do_query(defen, uid, region)
    except TypeError:
        session.finish('查询出错，请再次查询\n如果多次查询失败，请先移步pcrdfans.com进行查询，并可联系维护组', at_sender=True)
    sv.logger.info('Got response!')

    # 处理查询结果
    if res == 117 :
        session.finish('高峰期bot限流，请移步pcrdfans.com查询。',at_sender=True)
    if res is None:
        session.finish('查询出错，请再次查询\n如果多次查询失败，请先移步pcrdfans.com进行查询，并可联系维护组', at_sender=True)
    if not len(res):
        session.finish('抱歉没有查询到解法\n※没有作业说明随便拆 发挥你的想象力～★\n作业上传请前往pcrdfans.com', at_sender=True)
    res = res[:min(6, len(res))]    # 限制显示数量，截断结果

    # 发送回复
    if get_bot().config.IS_CQPRO:
        sv.logger.info('Arena generating picture...')
        atk_team = [ Chara.gen_team_pic(team=entry['atk'],text="\n".join([
      f"{entry['qkey']}",
      f"赞 {entry['up']}",
      f"踩 {entry['down']}",
  ])) for entry in res ]
        atk_team = concat_pic(atk_team)
        atk_team = pic2b64(atk_team)
        atk_team = str(MessageSegment.image(atk_team))
        sv.logger.info('Arena picture ready!')
    else:
        atk_team = '\n'.join(map(lambda entry: ' '.join(map(lambda x: f"{x.name}{x.star if x.star else ''}{'专' if x.equip else ''}" , entry['atk'])) , res))


    defen = [ Chara.fromid(x).name for x in defen ]
    defen = f"防守方【{' '.join(defen)}】"
    at = str(MessageSegment.at(session.ctx["user_id"]))

    msg = [
        defen,
        str(atk_team),
    ]
    msg.append('Support by pcrdfans_com')
    sv.logger.debug('Arena sending result...')
    await session.send('\n'.join(msg),at_sender=1)
    sv.logger.debug('Arena result sent!')


