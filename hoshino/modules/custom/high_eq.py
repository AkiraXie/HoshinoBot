from PIL import ImageFont, ImageDraw, Image
from hoshino import Service,R,Privilege as Priv
from hoshino.util import pic2b64
sv=Service('high_eq',visible=False,manage_priv=Priv.SUPERUSER,enable_on_default=False)
fontpath=R.img('priconne/gadget/FZY3K.TTF').path
path = R.img('high_eq_image.png').path
def draw_text(img_pil, text, offset_x):
    draw = ImageDraw.Draw(img_pil)
    font = ImageFont.truetype(fontpath, 48)
    width, height = draw.textsize(text, font)
    x = 5
    if width > 390:
        font = ImageFont.truetype(fontpath, int(390 * 48 / width))
        width, height = draw.textsize(text, font)
    else:
        x = int((400 - width) / 2)
    draw.rectangle((x + offset_x - 2, 360, x + 2 + width + offset_x, 360 + height * 1.2), fill=(0, 0, 0, 255))
    draw.text((x + offset_x, 360), text, font=font, fill=(255, 255, 255, 255))
@sv.on_rex(r'低情商(.+)高情商(.+)', normalize=True,can_private=1)
async def high_eq(bot,ctx,match):
    left = match.group(1).strip().strip(":").strip("。")
    right = match.group(2).strip().strip(":").strip("。")
    if len(left) > 15 or len(right) > 15:
        await bot.send(ctx,"为了图片质量，请不要多于15个字符")
        return
    img_p = Image.open(path)
    draw_text(img_p, left, 0)
    draw_text(img_p, right, 400)
    await bot.send(ctx,f'[CQ:image,file={pic2b64(img_p)}]')
@sv.on_rex(r'高情商(.+)低情商(.+)', normalize=True,can_private=1)
async def high_eq(bot,ctx,match):
    left = match.group(2).strip().strip(":").strip("。")
    right = match.group(1).strip().strip(":").strip("。")
    if len(left) > 15 or len(right) > 15:
        await bot.send(ctx,"为了图片质量，请不要多于15个字符")
        return
    img_p = Image.open(path)
    draw_text(img_p, left, 0)
    draw_text(img_p, right, 400)
    await bot.send(ctx,f'[CQ:image,file={pic2b64(img_p)}]')
