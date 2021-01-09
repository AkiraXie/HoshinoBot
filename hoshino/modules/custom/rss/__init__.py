import asyncio
from nonebot.argparse import ArgumentParser
from .data import Rss, Rssdata, BASE_URL
from hoshino import Service, Privilege as Priv, CommandSession, aiohttpx
sv = Service('rss', manage_priv=Priv.ADMIN,
             enable_on_default=False, visible=False)


@sv.on_command('添加订阅', aliases=('addrss', '增加订阅'), shell_like=True)
async def addrss(session: CommandSession):
    parser = ArgumentParser(session=session)
    parser.add_argument('name')
    parser.add_argument('url')
    parser.add_argument('-r', '--rsshub', action='store_true')
    args = parser.parse_args(session.argv)
    name = args.name
    url = BASE_URL+args.url if args.rsshub else args.url
    try:
        stats = await aiohttpx.head(url, timeout=5, allow_redirects=True)
    except Exception as e:
        sv.logger.exception(e)
        sv.logger.error(type(e))
        session.finish('请求路由失败,请稍后再试')
    if stats.status_code != 200:
        session.finish('请求路由失败,请检查路由状态')
    rss = Rss(url)
    if not await rss.has_entries:
        session.finish('暂不支持该RSS')
    try:
        Rssdata.replace(url=rss.url, name=name, group=session.event.group_id, date=await rss.last_update).execute()
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


@sv.scheduled_job('cron', minute='*/6', jitter=20)
async def push_rss():
    bot = sv.bot
    glist = await sv.get_enable_groups()
    for gid in glist.keys():
        res = Rssdata.select(Rssdata.url, Rssdata.name,
                             Rssdata.date).where(Rssdata.group == gid)
        for r in res:
            rss = Rss(r.url)
            if not (await rss.has_entries):
                continue
            if (lstdate := await rss.last_update) != r.date:
                try:
                    await asyncio.sleep(0.5)
                    newinfo = await rss.get_new_entry_info()
                    msg = [f'订阅 {r.name} 更新啦！']
                    for k, v in newinfo.items():
                        msg.append(f'{k}: {v}')
                    Rssdata.update(date=lstdate).where(
                        Rssdata.group == gid, Rssdata.name == r.name,Rssdata.url==r.url).execute()
                    await bot.send_group_msg(message='\n'.join(msg), group_id=gid)
                except Exception as e:
                    sv.logger.exception(e)
                    sv.logger.error(f'{type(e)} occured when pushing rss')


@sv.on_command('订阅列表', aliases=('查看本群订阅'))
async def lookrsslist(session: CommandSession):
    try:
        res = Rssdata.select(Rssdata.url, Rssdata.name).where(Rssdata.group ==
                                                              session.event.group_id)
        msg = ['本群订阅如下:']
        for r in res:
            msg.append(f'订阅标题:{r.name}  订阅路由:{r.url}')
    except Exception as e:
        sv.logger.exception(e)
        sv.logger.error(type(e))
        session.finish('查询订阅列表失败')
    session.finish('\n'.join(msg))


@sv.on_command('看订阅', aliases=('查订阅', '查看订阅'), shell_like=True)
async def lookrss(session: CommandSession):
    parser = ArgumentParser(session=session)
    parser.add_argument('name')
    parser.add_argument('-l', '--limit', default=5, type=int)
    args = parser.parse_args(session.argv)
    limit = args.limit
    name = args.name
    try:
        res = Rssdata.select(Rssdata.url).where(Rssdata.name == name, Rssdata.group ==
                                                session.event.group_id)
        r = res[0]
        rss = Rss(r.url, limit)
        infolist = await rss.get_all_entry_info()
    except Exception as e:
        sv.logger.exception(e)
        sv.logger.error(type(e))
        session.finish(f'查订阅{name}失败')
    msg = [f'{name}的最近记录:']
    for info in infolist:
        for k, v in info.items():
            msg.append(f'{k}: {v}')
        msg.append('==========')
    session.finish('\n'.join(msg))
