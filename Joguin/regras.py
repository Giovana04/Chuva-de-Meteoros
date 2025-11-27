# from main import *
import random

quantidadeCometas = 1
def aleatorizar(meteoros, qntd):
    for i in range(0,len(meteoros)):
        meteoros[i] = 0
    for i in range(0 ,qntd):
        val = random.randint(0,len(meteoros)-1)
        if(meteoros[val] == 0):
            meteoros[val] = 1
        else:
            for j in range(0,len(meteoros)):
                if(meteoros[j] == 0):
                    meteoros[j] = 1
                    break
    return meteoros

def checarColisaoNave(meteoro, nave):
    if nave.posicao[0] + nave.tamMax[0] > meteoro.posicao[0] + meteoro.tamMin[0] and nave.posicao[0] + nave.tamMin[0] < meteoro.posicao[0] + meteoro.tamMax[0]:
        if nave.posicao[1] + nave.tamMax[1] > meteoro.posicao[1] + meteoro.tamMin[1] and nave.posicao[1] + nave.tamMin[1] < meteoro.posicao[1] + meteoro.tamMax[1]:
                return True
    return False
