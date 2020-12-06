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
        choices=list(filter(lambda x:len(x)!=0,msg))
        if not choices:
            await bot.send(ctx,'选项不能全为空！',at_sender=True)
            return 
        msgs=['您的选项是:']
        idchoices=list(f'{i}. {choice}' for i,choice in enumerate(choices))
        msgs.extend(idchoices)
        if random.randrange(1000)<=76:
            msgs.append('建议您选择: “我全都要”')
        else:
            final=random.choice(choices)
            msgs.append(f'建议您选择: {final}')
        await bot.send(ctx,'\n'.join(msgs),at_sender=True)