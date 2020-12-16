from hoshino import sucmd,aiorequests
import json
@sucmd('restart',aliases=('重启go','重启gocq'),force_private=False)
async def gorestart(session):
    access_token=session.bot.config.ACCESS_TOKEN
    go_port=session.bot.config.GO_CQHTTP_WEBPORT
    try:
        res=await aiorequests.post(f'http://127.0.0.1:{go_port}/admin/do_process_restart?access_token={access_token}')
        if res.status_code !=200:
            resj=await res.json()
            session.finish(f'重启go-cqhttp失败,请前往服务器查看,出错如下:\n{json.dumps(resj)}')
    except Exception as e:
        session.finish(f'重启go-cqhttp失败,请前往服务器查看,出错如下:\n{e}')