import simpy

def auto(env, nombre, puestoBaterias, tiempoConduccion, tiempoCarga):
  
  print(f'El auto {nombre} comienza a conducir a las {env.now}')
  yield env.timeout(tiempoConduccion)
  print(f'El auto {nombre} frena en el puesto de baterias a las {env.now}')

  with puestoBaterias.request() as req: 
    yield req 
    print (f'El auto {nombre} comienza a cargar bateria a las {env.now}')
    yield env.timeout(tiempoCarga)
    print (f'El auto {nombre} finalizó su carga bateria a las {env.now}')

env = simpy.Environment()
puestoBaterias = simpy.Resource(env, capacity=2) 

for i in range(5):
  env.process(auto(env, i, puestoBaterias, 2, 5))
env.run(until=25)