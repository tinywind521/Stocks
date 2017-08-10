import json


# 写入JSON数据
def jsonWrite(path, data):
    if data:
        with open(path, 'w+') as f:
            json.dump(data, f)
    else:
        pass


# 读取JSON数据
def jsonRead(path):
    if path:
        with open(path, 'r') as f:
            data = json.load(f)
        return data
    else:
        return None
