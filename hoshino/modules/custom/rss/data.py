import os
import re
from typing import List, Dict, Optional
from lxml import etree
import peewee as pw
from hoshino import aiorequests
BASE_URL = "https://rsshub.akiraxie.me/"

class Rss():
    def __init__(self, route: str, limit: int = 5) -> None:
        super().__init__()
        self.route = route
        self.url=BASE_URL+self.route
        self.limit = limit

    @property
    async def xml(self):
        try:
            ret = await aiorequests.get(self.url, params={'limit': self.limit})
            return etree.XML(await ret.content)
        except:
            raise

    @staticmethod
    def _get_rssdic(item) -> Dict:
        ret = {'title': item.find('.title').text.strip(),
               'link': item.find('.link').text.strip(),
               'publish': item.find('.pubDate').text.strip()}
        return ret

    async def get_new_item_info(self) -> Optional[Dict]:
        try:
            xml = await self.xml
            item = xml.xpath('/rss/channel/item')[0]
            return self._get_rssdic(item)
        except:
            return None

    async def get_all_item_info(self) -> Optional[List[Dict]]:
        try:
            ret = []
            xml = await self.xml
            items = xml.xpath('/rss/channel/item')
            for item in items:
                itemdic = self._get_rssdic(item)
                ret.append(itemdic)
            return ret
        except:
            return None

    @property
    async def last_update(self) -> Optional[str]:
        try:
            return (await self.get_new_item_info())['publish']
        except:
            return None


db = pw.SqliteDatabase(
    os.path.join(os.path.dirname(__file__), 'rss.db')
)


class Rssdata(pw.Model):
    route = pw.TextField()
    name = pw.TextField()
    date = pw.TextField()
    group = pw.IntegerField()
    class Meta:
        database = db
        primary_key = pw.CompositeKey( 'group','route')

def init():
    if not os.path.exists(os.path.join(os.path.dirname(__file__), 'rss.db')):
        db.connect()
        db.create_tables([Rssdata])
        db.close()


init()
