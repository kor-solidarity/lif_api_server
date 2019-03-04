a = ['a', 's', 'd', 'f', 'g']


class yolo:
    def __init__(self, id, a):
        self.id = id
        self.a = a



yo = yolo(1, 2)
lo = yolo(2, 3)
s = yolo(3, 6)
d= yolo(4, 5)
f=yolo(6, 7)

listo = [yo, lo, s, d,  f]


for i in listo:
    if i.id == 1:
        listo.remove(i)

print(listo)