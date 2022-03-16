l = [1,2,3]
a="sd"

def fun(l, a):
    l.append(100)
    a=a+"qq"
    return a

a = fun(l,a)
print(l)
print(a)
