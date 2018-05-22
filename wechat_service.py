import itchat
from itchat.content import *
import os
import sys
sys.path.append("amazon_rank_searcher")
from rank_spider import RankSpirder

itchat.auto_login(hotReload=True, enableCmdQR=True)

@itchat.msg_register(itchat.content.TEXT)
def text_reply(msg):
  if msg.text == "查排名":
    itchat.send("查询中,请稍候...", msg.user['UserName'])
    os.chdir('./amazon_rank_searcher')
    rank_app = RankSpirder()
    rank_app.initDe()
    rank_app.run()
    result = rank_app.printResult()
    os.chdir('..')
    return result

@itchat.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO])
def download_files(msg):
    os.chdir('./amazon_rank_searcher')
    msg.download(msg.fileName)
    os.chdir('..')
    return "上传成功"

itchat.auto_login()
itchat.run()