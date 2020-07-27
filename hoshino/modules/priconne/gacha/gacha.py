import random

from hoshino import util
from ..chara import Chara


class Gacha(object):

    def __init__(self, pool_name:str="MIX"):
        super().__init__()
        self.load_pool(pool_name)


    def load_pool(self, pool_name:str):
        config = util.load_config(__file__)
        pool = config[pool_name]
        self.up_prob = pool["up_prob"]
        self.s3_prob = pool["s3_prob"]
        self.s2_prob = pool["s2_prob"]
        self.s1_prob = 1000 - self.s2_prob - self.s3_prob
        self.up = pool["up"]
        self.star3 = pool["star3"]
        self.star2 = pool["star2"]
        self.star1 = pool["star1"]


    def gacha_one(self, up_prob:int, s3_prob:int, s2_prob:int, s1_prob:int=None):
        '''
        sx_prob: x星概率，要求和为1000
        up_prob: UP角色概率（从3星划出）
        up_chara: UP角色名列表

        return: (单抽结果:Chara, 秘石数:int)
        ---------------------------
        |up|      |  20  |   78   |
        |   ***   |  **  |    *   |
        ---------------------------
        '''
        if s1_prob is None:
            s1_prob = 1000 - s3_prob - s2_prob
        total_ = s3_prob + s2_prob + s1_prob
        pick = random.randint(1, total_)
        if pick <= up_prob:
            return Chara.fromname(random.choice(self.up), 3), 100
        elif pick <= s3_prob:
            return Chara.fromname(random.choice(self.star3), 3), 50
        elif pick <= s2_prob + s3_prob:
            return Chara.fromname(random.choice(self.star2), 2), 10
        else:
            return Chara.fromname(random.choice(self.star1), 1), 1


    def gacha_ten(self):
        result = []
        hiishi = 0
        up = self.up_prob
        s3 = self.s3_prob
        s2 = self.s2_prob
        s1 = 1000 - s3 - s2
        for _ in range(9):    # 前9连
            c, y = self.gacha_one(up, s3, s2, s1)
            result.append(c)
            hiishi += y
        c, y = self.gacha_one(up, s3, s2 + s1, 0)    # 保底第10抽
        result.append(c)
        hiishi += y

        return result, hiishi


    def gacha_tenjou(self):
        result = {'s3': [], 's2':[], 's1':[]}
        first_up_pos = 999999
        upnum=0
        up = self.up_prob
        s3 = self.s3_prob
        s2 = self.s2_prob
        s1 = 1000 - s3 - s2
        for i in range(30): #三十个十连
            for j in range(1,10):    # 前9连
                c, y = self.gacha_one(up, s3, s2, s1)
                if 100 == y:
                    result['s3'].append(c)
                    first_up_pos = min(i*10+j,first_up_pos)
                    upnum+=1
                elif 50 == y:
                    result['s3'].append(c)
                elif 10 == y:
                    result['s2'].append(c)
                elif 1==y:
                    result['s1'].append(c)
                else:
                    pass    # should never reach here
            c, y = self.gacha_one(up, s3, s2 + s1, 0)    # 保底第10抽
            if 100 == y:
                result['s3'].append(c)
                first_up_pos = min((i+1)*10,first_up_pos)
                upnum+=1
            elif 50 == y:
                result['s3'].append(c)
            elif 10 == y:
                result['s2'].append(c)
            elif 1==y:
                result['s1'].append(c)
            else:
                pass # should never reach here
        result['first_up_pos'] = first_up_pos
        return result,upnum
