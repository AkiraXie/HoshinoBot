import random
from hoshino import Service

sv = Service('chooseone')


@sv.on_message('group')
async def chooseone(bot, ctx):
    message = ctx['raw_message']
    if message.startswith('选择卡池'):
        return
    if message.startswith('选择'):
        msg = message[2:].split('还是')
        if len(msg) == 1:
            return
        for i in msg:
            if len(i)==0:
                await bot.send(ctx, '不支持选择空字符')
                return
        choices=msg
        choices.append('"我全都要"')
        final_choice = random.choice(choices)
        reply = '您的选项是：'
        num = 1
        for i in choices[:-1]:
            reply += f'\n{num}、 {i}'
            num = num+1
        reply += f'\n最终的决定是：{final_choice}'
        await bot.send(ctx, reply, at_sender=True)
