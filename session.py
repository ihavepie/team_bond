class Session:
    def __init__(self, message, openid_status, func_dict):
        self.openid_status = openid_status
        self.func_dict = func_dict
        self.text = message.content
        self.status = ''

    def status(self):
        if '开始' in text:
            if openid in openid_status and openid_status[openid] == '对话中':
                self.status = 'cancel'
            else:
                openid_status[openid] = '对话中'
                function = text[:-2]
                if function in func_dict:
                    self.status = function
                else:
                    openid_status[openid] = '非对话中'
                    self.status = 'unkown'
        elif '结束' in text:
            openid_status[openid] = '非对话中'
            self.status = 'bye'
        elif openid in openid_status and openid_status[openid] == '对话中':
            self.status = 'talking'