# 本文实例讲述了Python去除列表中重复元素的方法。分享给大家供大家参考。
# 具体如下：
#
# 比较容易记忆的是用内置的set
l1 = ['b', 'c', 'd', 'b', 'c', 'a', 'a']
l2 = list(set(l1))
print(l2)

# 还有一种据说速度更快的，没测试过两者的速度差别
l1 = ['b', 'c', 'd', 'b', 'c', 'a', 'a']
l2 = list({}.fromkeys(l1).keys())
print(l2)

# 这两种都有个缺点，祛除重复元素后排序变了：
# ['a', 'c', 'b', 'd']

# 如果想要保持他们原来的排序：

# 用list类的sort方法
l1 = ['b', 'c', 'd', 'b', 'c', 'a', 'a']
l2 = list(set(l1))
l2.sort(key=l1.index)
print(l2)

# 也可以这样写
l1 = ['b', 'c', 'd', 'b', 'c', 'a', 'a']
l2 = sorted(set(l1), key=l1.index)
print(l2)

# 也可以用遍历
l1 = ['b', 'c', 'd', 'b', 'c', 'a', 'a']
l2 = []
for i in l1:
    if not (i in l2):
        l2.append(i)
print(l2)

# 上面的代码也可以这样写
l1 = ['b', 'c', 'd', 'b', 'c', 'a', 'a']
l2 = []
[l2.append(i) for i in l1 if not (i in l2)]
print(l2)
# 这样就可以保证排序不变了：
