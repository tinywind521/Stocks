import json
import os


# 写入JSON数据
def Write(path, data):
    if os.path.isdir(os.path.split(path)[0]):
        pass
    else:
        os.makedirs(os.path.split(path)[0])
    if data:
        with open(path, 'w+') as f:
            json.dump(data, f)
    else:
        pass


# 读取JSON数据
def Read(path):
    if path:
        with open(path, 'r') as f:
            data = json.load(f)
        return data
    else:
        return None
