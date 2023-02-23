from functions import structure
import datetime
import werobot
import pymongo
from werobot.replies import ArticlesReply, Article, ImageReply


# 创建图片对话
def createImageReply(msg, pic_path, robot):
    ret = robot.client.upload_media("image", open(pic_path, mode='rb'))
    pic_id = ret["media_id"]
    return ImageReply(msg, media_id=pic_id)

# 创建图文对话
def createArticleReply(msg, pic_path, description, url, title):
    ret = ArticlesReply(message=msg)
    article = Article(
        title = title,
        description = description,
        img = pic_path,
        url = url
    )
    ret.add_article(article)
    return ret


# def session(message, openid_status, func_dict):
#     openid = message.source
#     text = message.content
#     if '开始' in text:
#         if openid in openid_status and openid_status[openid] == '对话中':
#             return 'cancel'
#         else:
#             openid_status[openid] = '对话中'
#             function = text[:-2]
#             if function in func_dict:
#                 return function
#             else:
#                 openid_status[openid] = '非对话中'
#                 return 'unkown'
#     elif '结束' in text:
#         openid_status[openid] = '非对话中'
#         return 'bye'
#     elif openid in openid_status and openid_status[openid] == '对话中':
#         return 'talking'

