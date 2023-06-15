
import simpy
import random

personasQueSeFueron = 0 

def persona(env, nro):
    global personasQueSeFueron    
    print(f"Ingresó la persona {nro} a las {env.now}")
    yield env.timeout(5)
    print(f"Se fue la persona {nro} a las {env.now}")
    personasQueSeFueron+=1 

def sistema(env): 
    i=0
    while True: 
      yield env.timeout(random.randint(4, 6))
      i+=1 
      env.process(persona(env, i))

env = simpy.Environment() 
env.process(sistema(env)) 
env.run(until=60)
print(f"Se fueron del sistema {personasQueSeFueron} personas") 