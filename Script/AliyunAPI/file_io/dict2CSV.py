
def writeHeader(path, headers, method='w+'):
    try:
        f = open(path, method)
        text = ''
        end = headers.pop()
        for s in headers:
            text = text + s + ','
        text = text + end + '\n'
        f.write(text)
        f.close()
    except ValueError:
        pass


def writeWenCaiHeader(path, headers, method='w+'):
    try:
        f = open(path, method)
        text = ''
        end = headers.pop()
        for s in headers:
            text = text + s + ','
        text = (text + end + '\n').replace('\r', '')
        f.write(text)
        f.close()
    except ValueError:
        pass


def writeRows(path, rows):
    try:
        f = open(path, 'a+')
        for row in rows:
            text = ''
            temp = list(row.values())
            end = temp.pop()
            for s in temp:
                text = text + str(s).replace(',', '') + ','
            text = text + end + '\n'
            f.write(text)
        f.close()
    except ValueError:
        pass


def writeWenCaiRow(path, rows):
    try:
        f = open(path, 'a+')
        for row in rows:
            text = ''
            end = row.pop()
            for s in row:
                text = text + str(s).replace(',', '') + ','
            text = text + str(end) + '\n'
            f.write(text)
        f.close()
    except ValueError:
        pass
