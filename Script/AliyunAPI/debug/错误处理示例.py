"""python中try/except/else/finally语句的完整格式如下所示："""
try:
    """Normal execution block"""
except TypeError:
    "Exception A handle"
except ValueError:
    "Exception B handle"
except:
    "Other exception handle"
else:
    "if no exception,get here"
finally:
    """print("finally")"""
# 继续下面的流程
