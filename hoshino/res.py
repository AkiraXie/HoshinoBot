import os
from PIL import Image
from urllib.request import pathname2url
from urllib.parse import urljoin

from nonebot import get_bot
from nonebot import MessageSegment

from hoshino.util import pic2b64
from hoshino import logger

class R:

    @staticmethod
    def get(path, *paths):
        return ResObj(os.path.join(path, *paths))

    @staticmethod
    def img(path, *paths):
        return ResImg(os.path.join('img', path, *paths))



class ResObj:

    def __init__(self, res_path):
        res_dir = os.path.expanduser(get_bot().config.RESOURCE_DIR)
        self.fullpath = os.path.abspath(os.path.join(res_dir, res_path))
        if not self.fullpath.startswith(os.path.abspath(res_dir)):
            raise ValueError('Cannot access outside RESOUCE_DIR')
        


    @property
    def url(self):
        """
        @return: 资源文件的url，供cqhttp使用
        """
        return urljoin(get_bot().config.RESOURCE_URL, pathname2url(self.__path))


    @property
    def path(self):
        """
        @return: 资源文件的绝对路径，供bot内部使用
        """
        return os.path.normpath(self.fullpath)


    @property
    def exist(self):
        return os.path.exists(self.path)


class ResImg(ResObj):
    @property
    def cqcode(self) -> MessageSegment:
        if get_bot().config.RESOURCE_URL:
            return MessageSegment.image(self.url)
        else:
            try:
                return MessageSegment.image('file:///'+self.path)
            except Exception as e:
                logger.exception(e)
                return MessageSegment.text('[图片]')
    def open(self) -> Image:
        return Image.open(self.path)