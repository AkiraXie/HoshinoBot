from aiocqhttp.exceptions import Error as CQHttpError
import requests
import demjson
import random
import math
import time as _time
import os
from .arcaea_crawler import *
from hoshino import  Service,Privilege as Priv
sv=Service('arc',visible=False,enable_on_default=False,manage_priv=Priv.SUPERUSER)
dsname=os.path.join(os.path.dirname(__file__),'ds.txt')
f = open(dsname, 'r', encoding='utf-8')
dss = f.readlines()
f.close()

help_text = '''欢迎使用Arcaea Bot。支持的命令如下：
.ds <曲名/等级> 查询定数
.arc <玩家名/好友码> 查询玩家的ptt、r10/b30和最近游玩的歌曲
.best <玩家名/好友码> <n> 查询玩家ptt前n的歌曲'''


@sv.on_command('archelp', only_to_me=False)
async def helpp(session: CommandSession):
    await session.send(help_text)


@sv.on_command('arcbest', only_to_me=False)
async def lookup(session: CommandSession):
    await session.send("Looking up %s\nWarning: .best命令具有刷屏风险，请尽量私聊查询~" % session.state['id'])
    QueryThread(session.cmd, session.ctx, session.bot, session.state).start()


@lookup.args_parser
async def _(session: CommandSession):
    arr = session.current_arg_text.strip().split(' ')
    session.state['id'] = arr[0]
    try:
        session.state['num'] = int(arr[1])
    except Exception:
        session.state['num'] = 0


@sv.on_command('arcaea', aliases=['arc'], only_to_me=False)
async def arcaea(session: CommandSession):
    await session.send("Querying %s" % session.state['id'])
    QueryThread(session.cmd, session.ctx, session.bot, session.state).start()
        

@arcaea.args_parser
async def _(session: CommandSession):
    session.state['id'] = session.current_arg_text.strip()


@on_command('arcds', only_to_me=False)
async def ds(session: CommandSession):
    result_str = ""
    num = 0
    for line in dss:
        if session.state['arg'].lower() in line.lower():
            num += 1
            result_str += line.replace('\t', '  ')
    await session.send("共找到%d条结果：\n" % num + result_str[:-1])


@ds.args_parser
async def _(session: CommandSession):
    session.state['arg'] = session.current_arg_text.strip()