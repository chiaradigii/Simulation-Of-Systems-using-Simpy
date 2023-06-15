import random
import simpy
import numpy as np

CANT_EMPLEADOS = 2 
TIEMPO_ATENCION = 300 
TIEMPO_ARRIBO = 120
TIEMPO_SIMULACION = 7200

clientesAtendidos = 0

class CallCenter:

    def __init__ (self, env, cantEmpleados, tiempoAtencion): 
      self.env = env
      self.staff = simpy.Resource(env, cantEmpleados)
      self.tiempoAtencion = tiempoAtencion

    def atender(self, cliente):
      tiempoAtencionRandom = max(60, np.random.normal(self.tiempoAtencion, 240))
      yield self.env.timeout(tiempoAtencionRandom) 
      print(f'Atencion finalizada para el cliente {cliente} a las {self.env.now:.0f}')

def customer(env, nombre, callCenter):

  global clientesAtendidos
  print(f'Cliente {nombre} ingresa a la fila a las {env.now}')
  with callCenter.staff.request() as request: 
    yield request 
    print(f'Cliente {nombre} es atendido a las {env.now:.0f}')
    yield env.process(callCenter.atender(nombre)) 
    print(f'Cliente {nombre} termina su atención a las {env.now:.0f}')
    clientesAtendidos += 1

def setup(env, cantEmpleados, tiempoAtencion, tiempoArribo):
  callCenter = CallCenter(env, cantEmpleados, tiempoAtencion) 
  for i in range(1,6):
    env.process(customer(env, i, callCenter)) 
  while True:
    yield env.timeout(random.randint(tiempoArribo-60, tiempoArribo+60)) 
    i+=1
    env.process(customer(env, i, callCenter))

print('Comenzando la simulacion del Call Center')
env = simpy.Environment() 
env.process(setup(env, CANT_EMPLEADOS, TIEMPO_ATENCION, TIEMPO_ARRIBO))
env.run(until=TIEMPO_SIMULACION)

print('Clientes atendidos:', clientesAtendidos)