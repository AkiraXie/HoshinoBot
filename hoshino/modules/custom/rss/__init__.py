import asyncio
import time
from datetime import datetime, timedelta
from .data import Rss, Rssdata, BASE_URL
from hoshino import Service, Privilege as Priv, CommandSession, aiohttprequest
sv = Service('rss', manage_priv=Priv.ADMIN,
             enable_on_default=False, visible=False)


def format_time(timestr: str) -> str:
    struct_time = time.strptime(timestr, '%a, %d %b %Y %H:%M:%S %Z')
    dt = datetime.fromtimestamp(time.mktime(struct_time))
    return str(dt+timedelta(hours=8))


@sv.on_command('添加订阅', aliases=('addrss', '增加订阅'))
async def addrss(session: CommandSession):
    try:
        msgs = session.current_arg_text.split()
    except:
        return
    if len(msgs) != 2:
        return
    name, route = msgs
    name = name.strip()
    route = route.strip('/')
    url = BASE_URL+route
    try:
        stats = await aiohttprequest.head(url)
    except Exception as e:
        sv.logger.exception(e)
        sv.logger.error(type(e))
        session.finish('请求路由失败,请稍后再试')
    if stats.status != 200:
        session.finish('输入路由无效')
    rss = Rss(route)
    try:
        Rssdata.replace(route=rss.route, name=name, group=session.event.group_id, date=await rss.last_update).execute()
    except Exception as e:
        sv.logger.exception(e)
        sv.logger.error(type(e))
        session.finish('添加订阅失败')
    session.finish(f'添加订阅{name}成功')


@sv.on_command('删除订阅', aliases=('delrss', '取消订阅'))
async def delrss(session: CommandSession):
    try:
        name = session.current_arg_text.strip()
    except:
        return

    try:
        Rssdata.delete().where(Rssdata.name == name, Rssdata.group ==
                               session.event.group_id).execute()
    except Exception as e:
        sv.logger.exception(e)
        sv.logger.error(type(e))
        session.finish('删除订阅失败')
    session.finish(f'删除订阅{name}成功')


@sv.scheduled_job('cron', minute='*/15', jitter=20)
async def push_rss():
    bot = sv.bot
    glist = await sv.get_enable_groups()
    for gid in glist.keys():
        res = Rssdata.select(Rssdata.route, Rssdata.name,
                             Rssdata.date).where(Rssdata.group == gid)
        for r in res:
            rss = Rss(r.route)
            if lstdate := (await rss.last_update) != r.date:
                try:
                    await asyncio.sleep(0.5)
                    newinfo = await rss.get_new_item_info()
                    msg = [f'订阅 {r.name} 更新啦！']
                    msg.append(f'标题: {newinfo["title"]}')
                    msg.append(f'链接: {newinfo["link"]}')
                    msg.append(f'时间: {format_time(newinfo["publish"])}')
                    Rssdata.update(date=lstdate).where(
                        Rssdata.group == gid, Rssdata.name == r.name)
                    bot.send_group_msg(message='\n'.join(msg), group_id=gid)
                except Exception as e:
                    sv.logger.exception(e)
                    sv.logger.error(f'{type(e)} occured when pushing rss')


@sv.on_command('订阅列表', aliases=('查看本群订阅'))
async def lookrsslist(session: CommandSession):
    try:
        res = Rssdata.select(Rssdata.route, Rssdata.name).where(Rssdata.group ==
                                                                session.event.group_id)
        msg = ['本群订阅如下:']
        for r in res:
            msg.append(f'订阅标题:{r.name}  订阅路由:{r.route}')
    except Exception as e:
        sv.logger.exception(e)
        sv.logger.error(type(e))
        session.finish('查询订阅列表失败')
    session.finish('\n'.join(msg))


@sv.on_command('看订阅', aliases=('查订阅', '查看订阅'))
async def lookrss(session: CommandSession):
    try:
        name = session.current_arg_text
    except:
        return
    try:
        res = Rssdata.select(Rssdata.route).where(Rssdata.name == name, Rssdata.group ==
                                                  session.event.group_id)
        r = res[0]
        rss = Rss(r.route)
        infolist = await rss.get_all_item_info()
    except Exception as e:
        sv.logger.exception(e)
        sv.logger.error(type(e))
        session.finish(f'查订阅{name}失败')
    msg = [f'{name}的最近记录:']
    for info in infolist:
        msg.append(f'标题: {info["title"]}')
        msg.append(f'链接: {info["link"]}')
        msg.append(f'时间: {format_time(info["publish"])}')
        msg.append('==========')
    session.finish('\n'.join(msg))
