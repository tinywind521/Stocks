

def txt_write(text, path):
    """写入指定路径的文本文档"""
    try:
        f = open(path, 'w')
        f.write(text)
        f.close()
    except ValueError:
        pass


def txt_read(path):
    """打开指定路径的文本文档"""
    try:
        f = open(path, 'r')
        text = f.read()
        f.close()
       
        if text:
            return text
        else:
            return None
       
    except ValueError:
        pass

