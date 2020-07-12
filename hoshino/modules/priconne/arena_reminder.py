from hoshino.service import Service

sv = Service('pcr-arena-reminder')
svjp = Service('pcr-arena-reminder-jp', enable_on_default=False)
msg = '骑士君~准备好背刺了吗？'

@sv.scheduled_job('cron', hour='14', minute='45')
async def pcr_reminder():
    await sv.broadcast(msg, 'pcr-reminder', 0.2)

@svjp.scheduled_job('cron', hour='13', minute='45')
async def pcr_reminder_jp():
    await svjp.broadcast(msg, 'pcr-reminder-jp', 0.2)
