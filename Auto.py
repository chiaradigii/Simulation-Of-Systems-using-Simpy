
import simpy

def conductor(env, auto):
  yield env.timeout(3)
  auto.action.interrupt()

class Auto(object):

  def __init__(self, env):
    self.env = env
    self.action = env.process(self.arranca())

  def arranca(self):
      while True:
          print(f'Estacionando y cargando energía a las {self.env.now}')
          duracionCarga = 5

          try: 
            yield self.env.process(self.cargaBateria(duracionCarga))
          except simpy.Interrupt:
            print(f'Se interrumpió la carga a las {self.env.now}. Esperemos que alcance para el viaje...')
          
          print(f'Comienza a andar a las {self.env.now}')
          yield self.env.timeout(2)

  def cargaBateria(self, duracionCarga):
              yield self.env.timeout(duracionCarga)


env = simpy.Environment()
auto = Auto(env) 
env.process(conductor(env, auto))
env.run(until=25)