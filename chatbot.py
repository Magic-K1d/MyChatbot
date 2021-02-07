# coding=utf8
from itchat import Core
import requests
import random
from pymongo import MongoClient
from Search import Searcha


class chatbot(object):
    def __init__(self):
        self.itchat = Core()
        self.KEY_list = ['8edce3ce905a4c1dbb965e6b35c3834d', 'eb720a8970964f3f855d863d24406576',
                         '1107d5601866433dba9599fac1bc0083', '71f28bf79c820df10d39b4074345ef8c']
        self.apiUrl = 'http://www.tuling123.com/openapi/api'
        # MongoDB
        self.client = MongoClient()  ## MongDB client
        self.db = self.client['zzx']  ## choose a db
        self.jiandan_collection = self.db['jiandan']  ##choos.e a collection in db
        self.duowan_collection = self.db['duowan_lxh']  ##choose a collection in db

        self.path_jiandan_dir = u'/ftp/jiandan/'
        
        #bdy
        self.text1_list = []
        self.a_list = []
        self.Bdyuser = []

        # bt
        self.search_q = ''
        self.text2_list = []
        self.cl_list = []
        self.xl_list = []
        self.BTuser = []
        self.inChoose = []
        self.maxNum = 10
        self.link_Num = list(map(str, list(range(self.maxNum))))
        self.link_0Num = ['0' + x for x in list(map(str, list(range(self.maxNum))))]
        # for x in range(self.maxNum):
        #    self.link_Num.append(str(x))
        #    self.link_0Num.append('0' + str(x))
        self.text_send = ''
        self.fn = 'fa'
        self.fn_list = ['fa', 'la', 'hd', 'sd']
        self.fn_doc = {'fa': '收录时间', 'la': '最后活跃', 'hd': '活跃热度', 'sd': '文件大小'}

    def get_response(self, msg):
        KEY = random.choice(self.KEY_list)
        data = {
            'key': KEY,
            'info': msg,
            'userid': 'wechat-robot',
        }
        try:
            r = requests.post(self.apiUrl, data=data).json()
            if r.get('text') == '亲爱的，当天请求次数已用完。':
                return
            else:
                return r.get('text')
        except:
            return

    def random_get_img(self, msg, kind):
        global img_path_list_t, path
        if kind == 'girl':
            img_path_list_t = self.jiandan_collection.find({}, {'img_path': 'a'})
        elif kind == 'lxh':
            img_path_list_t = self.duowan_collection.find({}, {'img_path': 'a'})
        img_path_list = []
        for img_path in img_path_list_t:
            img_path_list.append(img_path['img_path'])
        img_path = random.choice(img_path_list)
        if isinstance(img_path, list):
            img_path = random.choice(img_path)
        if kind == 'girl':
            path = u'@img@' + self.path_jiandan_dir + img_path
        elif kind == 'lxh':
            path = u'@img@' + img_path  # 冷笑话的目录写在了数据库里
        print(path)
        if img_path[-4:] == '.gif':
            self.itchat.send('It\'s GIF,please wait', toUserName=msg['FromUserName'])
        self.itchat.send(path, toUserName=msg['FromUserName'])

    def bdy(self, msg):
        if msg['Text'] == 'exit' or msg['Text'] == 'e':
            self.Bdyuser.remove(msg['FromUserName'])
            self.itchat.send('Success exit Bdy.', toUserName=msg['FromUserName'])
        else:
            try:
                self.search_q = str(msg['Text'])
                self.itchat.send('正在搜索...', toUserName=msg['FromUserName'])
                [self.text1_list, self.a_list] = Searcha.Bdy_search(self.search_q)
            except:
                self.itchat.send('网络繁忙，请稍后重试', toUserName=msg['FromUserName'])
            if len(self.text1_list) != 0:
                for x in range(min(len(self.text1_list), self.maxNum)):
                    self.text_send += str(x) + ' : ' + self.text1_list[x] + ' ' +self.a_list[x] + ' \n'
                self.itchat.send(self.text_send, toUserName=msg['FromUserName'])
                self.text_send = ''
            else:
                self.itchat.send('未搜索到结果', toUserName=msg['FromUserName'])

    def bt(self, msg):
        if msg['Text'] == 'exit' or msg['Text'] == 'e':
            # self.functionDict['FriendChat']['Text'] = reply
            self.BTuser.remove(msg['FromUserName'])
            try:
                self.inChoose.remove(msg['FromUserName'])
            except:
                pass
            self.itchat.send('Success exit BT.', toUserName=msg['FromUserName'])
        elif msg['Text'] in self.fn_list:
            self.fn = msg['Text']
            self.itchat.send('排序方式-->' + str(self.fn_doc[self.fn]), toUserName=msg['FromUserName'])
            msg['Text'] = self.search_q
            try:
                self.inChoose.remove(msg['FromUserName'])
            except:
                pass
            return self.bt(msg)
        elif msg['FromUserName'] in self.inChoose:
            if msg['Text'] == 'next' or msg['Text'] == 'jx':
                self.inChoose.remove(msg['FromUserName'])
                self.itchat.send('请继续你的表演', toUserName=msg['FromUserName'])
            elif msg['Text'] in self.link_Num:
                self.itchat.send(self.cl_list[int(msg['Text'])], toUserName=msg['FromUserName'])
            elif msg['Text'] in self.link_0Num:
                self.itchat.send(self.xl_list[int(msg['Text'])], toUserName=msg['FromUserName'])
            else:
                self.inChoose.remove(msg['FromUserName'])
                return self.bt(msg)
                # self.itchat.send('序号有误，请重新输入', toUserName=msg['FromUserName'])

        else:
            try:
                self.search_q = str(msg['Text'])
                self.itchat.send('正在搜索...', toUserName=msg['FromUserName'])
                [self.text2_list, self.cl_list, self.xl_list] = Searcha.BT_search(self.search_q, self.fn)
            except:
                self.itchat.send('网络繁忙，请稍后重试', toUserName=msg['FromUserName'])
            if len(self.text2_list) != 0:
                for x in range(min(len(self.text2_list), self.maxNum)):
                    self.text_send += str(x) + ' : ' + self.text2_list[x] + ' \n'
                self.itchat.send(self.text_send, toUserName=msg['FromUserName'])
                self.text_send = ''
                self.inChoose.append(msg['FromUserName'])

                # self.itchat.send(cl_list[x], toUserName=msg['FromUserName'])
                # self.itchat.send(xl_list[x], toUserName=msg['FromUserName'])
            else:
                self.itchat.send('未搜索到结果', toUserName=msg['FromUserName'])

    # @Core.msg_register(Core, 'Friends')
    def add_friend(self, msg):
        self.itchat.add_friend(**msg['Text'])
        self.itchat.send(u'我是MkBot！\n'
                         u'使用说明：\n'
                         u'我可以陪你聊天，查询天气wiki等。\n'
                         u'输入：\'girl\'或\'g\'有惊喜\n'
                         u'输入：\'hh\'或\'冷笑话\'会冷到你哦\n'
                         u'查询BT功能，输入\'BT\'或\'bt\'进入BT查询', msg['RecommendInfo']['UserName'])


mk = chatbot()
if __name__ == '__main__':
    pass
    # mk.run()
