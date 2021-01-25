from typing import Iterable
from lxml import etree
import json
import os
from asyncio import sleep
from nonebot import CommandSession
from hoshino import service, aiorequests
from hoshino.util import load_config

sv = service.Service("steam", enable_on_default=False,visible=False)

subscribe_file = os.path.join(os.path.dirname(__file__), 'subscribes.json')
with open(subscribe_file, mode="r") as f:
    f = f.read()
    sub = json.loads(f)
cfg = load_config(__file__)
playing_state = {}
async def format_id(id:str)->str:
    if id.startswith('76561198') and len(id)==17:
        return id
    else:
        resp= await aiorequests.get(f'https://steamcommunity.com/id/{id}?xml=1')
        xml=etree.XML(await resp.content)
        return xml.xpath('/profile/steamID64')[0].text

@sv.on_command("添加steam订阅")
async def steam(session: CommandSession):
    account = session.current_arg_text.strip()
    try:
        rsp = await get_account_status(account)
        if rsp["personaname"] == "":
            await session.send("查询失败！")
        elif rsp["gameextrainfo"] == "":
            await session.send(f"%s 没在玩游戏！" % rsp["personaname"])
        else:
            await session.send(f"%s 正在玩 %s ！" % (rsp["personaname"], rsp["gameextrainfo"]))
        await update_steam_ids(account, session.event["group_id"])
        await session.send("订阅成功")
    except:
        await session.send("订阅失败")


@sv.on_command("取消steam订阅")
async def steam(session: CommandSession):
    account = session.current_arg_text.strip()
    try:
        await del_steam_ids(account, session.event["group_id"])
        await session.send("订阅成功")
    except:
        await session.send("订阅失败")


@sv.on_command("steam订阅列表",aliases=('查看本群steam','本群steam订阅'))
async def steam(session: CommandSession):
    group_id = session.event["group_id"]
    msg = '======steam======\n'
    await update_game_status()
    for key, val in playing_state.items():
        if group_id in sub["subscribes"][str(key)]:
            if val["gameextrainfo"] == "":
                msg += "%s 没在玩游戏\n" % val["personaname"]
            else:
                msg += "%s 正在游玩 %s\n" % (val["personaname"],
                                         val["gameextrainfo"])
    await session.send(msg)


@sv.on_command("查询steam账号",aliases=('查看steam','查看steam订阅','steam'))
async def steam(session: CommandSession):
    account = session.current_arg_text.strip()
    rsp = await get_account_status(account)
    if rsp["personaname"] == "":
        await session.send("查询失败！")
    elif rsp["gameextrainfo"] == "":
        await session.send(f"%s 没在玩游戏！" % rsp["personaname"])
    else:
        await session.send(f"%s 正在玩 %s ！" % (rsp["personaname"], rsp["gameextrainfo"]))


async def get_account_status(id) -> dict:
    id=await format_id(id)
    params = {
        "key": cfg["key"],
        "format": "json",
        "steamids": id
    }
    resp = await aiorequests.get("https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/", params=params)
    rsp = await resp.json()
    friend = rsp["response"]["players"][0]
    return {
        "personaname": friend["personaname"] if "personaname" in friend else "",
        "gameextrainfo": friend["gameextrainfo"] if "gameextrainfo" in friend else ""
    }


async def update_game_status() -> None:
    params = {
        "key": cfg["key"],
        "format": "json",
        "steamids": ",".join(sub["subscribes"].keys())
    }
    resp = await aiorequests.get("https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/", params=params)
    rsp = await resp.json()
    for friend in rsp["response"]["players"]:
        playing_state[friend["steamid"]] = {
            "personaname": friend["personaname"],
            "gameextrainfo": friend["gameextrainfo"] if "gameextrainfo" in friend else ""
        }
    

async def update_steam_ids(steam_id, group):
    steam_id=await format_id(steam_id)
    if steam_id not in sub["subscribes"]:
        sub["subscribes"][str(steam_id)] = []
    if group not in sub["subscribes"][str(steam_id)]:
        sub["subscribes"][str(steam_id)].append(group)
    with open(subscribe_file, mode="w") as fil:
        json.dump(sub, fil, indent=4, ensure_ascii=False)
    await update_game_status()


async def del_steam_ids(steam_id, group):
    steam_id=await format_id(steam_id)
    if group in sub["subscribes"][str(steam_id)]:
        sub["subscribes"][str(steam_id)].remove(group)
    with open(subscribe_file, mode="w") as fil:
        json.dump(sub, fil, indent=4, ensure_ascii=False)
    await update_game_status()


@sv.scheduled_job('cron', minute='*/2')
async def check_steam_status():
    old_state = playing_state.copy()
    await update_game_status()
    for key, val in playing_state.items():
        if val["gameextrainfo"] != old_state[key]["gameextrainfo"]:
            glist=set(sub["subscribes"][key])&set((await sv.get_enable_groups()).keys())
            if val["gameextrainfo"] == "":
                await broadcast(glist,
                                "%s 不玩 %s 了！" % (val["personaname"], old_state[key]["gameextrainfo"]))
            else:
                await broadcast(glist,
                                "%s 开始游玩 %s ！" % (val["personaname"], val["gameextrainfo"]))


async def broadcast(group_list: Iterable, msg):
    for group in group_list:
        await sv.bot.send_group_msg(group_id=group, message=msg)
        await sleep(0.5)
