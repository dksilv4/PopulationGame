import random

diogo = 0
dani = 0
leo = 0
kosta = 0
george = 0


for x in range(0, 1000000):
    randomInt = random.randint(0, 100)
    a = random.randint(0, 100)
    b = random.randint(0, 100)
    c = random.randint(0, 100)

    if randomInt<=20:
        diogo +=1
    if randomInt<=40 and randomInt>20:
        dani +=1
    if randomInt<=60 and randomInt>40:
        leo+=1
    if randomInt<=80 and randomInt>60:
        kosta +=1
    if randomInt<=100 and randomInt>80:
        george+= 1

print("Diogo: {} \nDani: {} \nLeo: {} \nKosta: {} \nGeorge: {}".format(diogo,dani,leo,kosta,george))