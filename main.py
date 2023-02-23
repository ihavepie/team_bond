import werobot
import tools
import pymongo
import time
from functions import weather
from functions import structure

robot = werobot.WeRoBot()
class RobotConfig(object):
    HOST = '10.0.8.13'
    PORT = 80
    TOKEN = 'maple'
    APP_ID = "wx3768aa80f1b99e95"
    APP_SECRET = "a941a4cf18a3763f1be98bd18fd50543"
robot.config.from_object(RobotConfig)
client = robot.client

mongo = pymongo.MongoClient("mongodb://root:password@101.42.53.204:27017/database")
db = mongo["database"]
col = db["session_log"]

func_dict = {
    'structure': structure.structure_quire,
    'weather': weather.weather_quire,
    'fiction': 'test',
    'daily': 'test',
}

func_reply = "1.天气功能:   weather开始\n" \
             "2.今日日报:   daily开始\n" \
             "3.结构查询:   structure开始\n" \
             "et al...."

def session(message, funcs):
    openid = message.source
    text = message.content
    # 因为result不是动态的，所以每次操作都需要重复此步骤
    result = col.find_one({'openid':openid, 'status':'talking'})
    if '开始' in text:
        # 如果能找到当前对话用户的session， 则返回‘cancel’
        if result:
            return 'cancel'
        # 如果不能找到当前对话用户的session，则在数据中新建一个session
        else:
            # 创建一个session
            col.insert_one({'openid': openid, 'status': 'talking', 'num':0})
            # 对result更新
            result = col.find_one({'openid':openid, 'status':'talking'})
            # 包含一些创建时间等信息
            start = int(time.time())
            col.update_one(result, {"$set":{'start':start}})
            # 截取功能
            function = text[:-2]
            # 如果功能函数在列表内, 则返回名称
            if function in funcs:
                col.update_one(result, {"$set":{'function':function}})
                return function
            # 如果创建的是未知功能对话, 则返回未知
            else:
                col.update_one(result, {"$set":{'status':'untalk'}})
                return 'unknown'
    # 如果发送包含'结束'的语句, 则更新字段, 返回该session的信息
    elif '结束' in text:
        result = col.find_one({'openid': openid, 'status': 'talking'})
        start = result['start']
        end = int(time.time())
        col.update_one(result, {"$set": {'end': end}})
        col.update_one(result, {"$set": {'during': end-start}})
        # 对话结束后，返回关于对话的信息
        result = col.find_one({'openid': openid, 'status': 'talking'})
        replies = f"用时{result['during']}s\n" \
                  f"共{result['num']}句话\n" \
                  f"使用功能为{result['function']}"
        col.update_one(result, {"$set": {'status': 'untalk'}})
        # 此处应该返回一个对象
        return replies
    # 如果发送语句不包含开始和结束, 则返回对话中
    else:
        # 可以在此处放置一些关于对话的信息，num et al
        result = col.find_one({'openid': openid, 'status': 'talking'})
        num = result['num']
        num += 1
        col.update_one(result, {"$set": {'num': num}})
        return 'talking'
    
def judgement(message, status):
    openid = message.source
    text = message.content
    if status == 'cancel':
        return '请先退出当前对话~'
    elif status == 'unknown':
        return '未知功能,请查看功能列表~'
    else:
        result = col.find_one({'openid': openid, 'status': 'talking'})
        if result:
            if result['num'] == 0:
                return status+'功能开始'
            else:
                func = result['function']
                if func == 'structure':
                    return func_dict[func](text)
                elif func == 'weather':
                    return func_dict[func](text)
        else:
            return status

@robot.text
def reply(message):
    if '功能' in message.content:
        return func_reply
    status = session(message, func_dict)
    return judgement(message, status)


# 让服务器监听在 0.0.0.0:80
robot.run()