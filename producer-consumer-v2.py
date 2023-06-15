"""In this case, there is one producer who drops objects every 1 second and two consumers who try to take it every 5 seconds. 
    Therefore, the ones who wait are the producers as the store has limited capacity.
"""

import simpy

def productor(env, store):
  for i in range(100):
    yield env.timeout(1) #PRODUCTOR ESPERA 1 SEGUNDO
    print(f'Productor dejando objeto {i} a las {env.now}')
    yield store.put(f'objeto {i}') #ESTE ES EL QUE VA A DEMORAR
    print(f'Productor dejó objeto {i} a las {env.now}')

def consumidor(obj, env, store):
  while True:
    yield env.timeout(5)#CONSUMIDOR CONSUME CADA 5!! 
    print(f'Consumidor {obj} buscando objeto a las {env.now}')
    item = yield store.get()#NUCA DEMORA PORQ SIEMPRE TIENE LUGAR PARA CONSUMIR
    print(f'Consumidor {obj} tomó {item} a las {env.now}')

env = simpy.Environment()
store = simpy.Store(env, capacity=2)#SOLO TIENE CAPACIDAD DE 2
prod = env.process(productor(env, store))
cons = [env.process(consumidor(i, env, store)) for i in range(2)]#
env.run(until=11)