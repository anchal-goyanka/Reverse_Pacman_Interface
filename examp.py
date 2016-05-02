import copy
for i in range(1,4):
    print i
l = [1,3,4]
b = copy.deepcopy(l)
for i in l:
    if i > 1:
        b.remove(i)
        print b,i
print b,l    
