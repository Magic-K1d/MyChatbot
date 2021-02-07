# coding=utf8
from chatbot import mk

mk.itchat.auto_login(hotReload=True, enableCmdQR=2)


@mk.itchat.msg_register('Text')
def main_reply(msg):
    if msg['FromUserName'] in mk.BTuser:
        mk.bt(msg)
    elif msg['FromUserName'] in mk.Bdyuser:
        mk.bdy(msg)

    elif msg['Text'] == 'girl' or msg['Text'] == 'g' or msg['Text'] == '美女':
        mk.random_get_img(msg, 'girl')
    elif msg['Text'] == '笑话' or msg['Text'] == 'hh' or msg['Text'] == '冷笑话':
        mk.random_get_img(msg, 'lxh')
    elif msg['Text'] == 'BT' or msg['Text'] == 'bt':
        # mk.itchat.functionDict['FriendChat']['Text'] = mk.bt
        mk.itchat.send('Success into BT.', toUserName=msg['FromUserName'])
        mk.itchat.send('BT种子搜索功能：\n'
                       '输入查询的内容，默认返回10个结果，格式为\n'
                       '序号 ：文件名  大小\n\n'
                       '输入\'序号\'获取磁力链接\n'
                       '输入\'0+序号\'获取迅雷链接\n'
                       '可重复获取链接\n输入\'next\'或\'jx\'重新搜索\n\n'
                       '输入代号更改排序方式,默认fa\n'
                       'fa : 收录时间   la : 最后活跃\n'
                       'hd : 活跃热度   sd : 文件大小\n\n'
                       '查询结束输入\'e\'或者\'exit\'退出搜索功能\n退出前无法使用其他功能', toUserName=msg['FromUserName'])
        mk.BTuser.append(msg['FromUserName'])
    elif msg['Text'] == 'bd' or msg['Text'] == 'BD' or msg['Text'] == 'bdy' or msg['Text'] == 'Bdy' or msg['Text'] == 'Bd':
        # mk.itchat.functionDict['FriendChat']['Text'] = mk.bt
        mk.itchat.send('Success into Bdy.', toUserName=msg['FromUserName'])
        mk.itchat.send('百度网盘搜索功能：\n'
                       '输入查询的内容，默认返回10个结果，格式为\n'
                       '序号 ：文件名  链接\n\n'
                       '查询结束输入\'e\'或者\'exit\'退出搜索功能\n退出前无法使用其他功能', toUserName=msg['FromUserName'])
        mk.Bdyuser.append(msg['FromUserName'])
    else:
        defaultReply = 'I received: ' + msg['Text']
        reply = mk.get_response(msg['Text'])
        return reply or defaultReply


# 开启自动添加好友
mk.itchat.functionDict['FriendChat']['Friends'] = mk.add_friend

mk.itchat.run()
