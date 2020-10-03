import nonebot
bot= nonebot.get_bot()

#@bot.on_meta_event("heartbeat")
async def heartnotice(ev):
   await bot.send_private_msg( user_id=bot.config.SUPERUSERS[0], message='心跳包~')
   
@bot.on_meta_event('lifecycle.connect')
async def onlinenotice(ev):
   await bot.send_private_msg( user_id=bot.config.SUPERUSERS[0], message='生命周期上线~')
   
