import os
import os.path

rootdir = input('Please input direction path:')
# 指明被遍历的文件夹

for parent, dirnames, filenames in os.walk(rootdir):
    # 三个参数分别返回
    # 1. parent: 父目录
    # 2. dirnames: 所有文件夹名字（不含路径）
    # 3. filenames: 所有文件名字
    for dirName in dirnames:
        # 输出文件夹信息
        print('以下枚举文件夹信息')
        print("父目录 is " + parent)
        print("文件夹目录 is " + dirName)

    for fileName in filenames:
        # 输出文件信息
        print('\n以下枚举文件信息')
        print("父目录 is " + parent)
        print("文件名 is " + fileName)
        print("完整文件路径 is " + os.path.join(parent, fileName))
        # 输出文件路径信息

    # 这个filenames就是文件夹下的文件名列表
    print(filenames)
