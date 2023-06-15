"""
Messages are sent over the network and processed by the receiver after a certain latency. 

"""

import simpy

TIEMPO_SIMULACION = 100

class Cable(object):
    def __init__(self, env, delay):
        self.env = env
        self.delay = delay 
        self.store = simpy.Store(env) 

    def latencia(self, nombre):
        yield self.env.timeout(self.delay) 
        self.store.put(nombre)

    def put(self, nombre):
        self.env.process(self.latencia(nombre))

    def get(self):
        return self.store.get() 


def emisor(env, cable):
    while True:
        yield env.timeout(5) 
        cable.put(f'Emisor lo envió a las {env.now}')


def receptor(env, cable):
    while True:
        msg = yield cable.get() 
        print(f'Recibido a las {env.now} mientras que el {msg}')


env = simpy.Environment()

cable = Cable(env, 10)
env.process(emisor(env, cable)) 
env.process(receptor(env, cable)) 

env.run(until=TIEMPO_SIMULACION) 