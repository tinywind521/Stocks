from file_io import txt

path1 = 'Z:/Test/LHB.txt'
s1 = txt.txt_read(path1)
s1.rstrip()
LHB_List = s1.splitlines()
print(LHB_List)

path2 = 'Z:/Test/量子通信.txt'
s2 = txt.txt_read(path2)
s2.rstrip()
Block_List = s2.splitlines()
print(Block_List)

for s in Block_List:
    if LHB_List.count(s) >= 1:
        print(s)