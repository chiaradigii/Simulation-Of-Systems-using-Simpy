"""Simulate a generic producer/consumer. The producer leaves something in the Store
(which has a certain capacity) and the consumer takes them.
In this case, there is a producer who leaves objects every 2 seconds and two consumers who try to take it every second. 
Therefore, the ones who have to wait are the consumers"""

import simpy

def productor(env, store):
  for i in range(100): 
    yield env.timeout(2)
    print(f'Productor dejando objeto {i} a las {env.now}')
    yield store.put(f'objeto {i}')
    print(f'Productor dejó objeto {i} a las {env.now}')

def consumidor(obj, env, store):
  while True:
    yield env.timeout(1)
    print(f'Consumidor {obj} buscando objeto a las {env.now}')
    item = yield store.get()
    print(f'Consumidor {obj} tomó {item} a las {env.now}')

env = simpy.Environment()
store = simpy.Store(env, capacity=2) 
prod = env.process(productor(env, store))
cons = [env.process(consumidor(i, env, store)) for i in range(2)]
env.run(until=8)
