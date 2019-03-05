txt = open("z:/1.txt",mode='w+')

for i in range(1114111):
    try:
        txt.write(chr(i))
    except:
        pass

txt.close()
