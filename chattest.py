from itchat import Core

Core = Core()
Core.auto_login(hotReload=True, enableCmdQR=2)


@Core.msg_register('Text')
def test(msg):
    print(msg['Text'])
    if Core.functionDict['FriendChat']['Text'] == test1:
        print('xxxxxxxxxxx')


def test1(msg):
    print(msg['Text'] + '\nxxxxxx')
    if Core.functionDict['FriendChat']['Text'] == test1:
        print('xxxxxxxxxxx')
        Core.send('123', toUserName=['FromUserName'])
        print('a')


Core.functionDict['FriendChat']['Text'] = test1
#if Core.functionDict['FriendChat']['Text'] == test1:
#    print('xxxxxxxxxxx')
# while Core.alive:
#    Core.configured_reply()

Core.run()
