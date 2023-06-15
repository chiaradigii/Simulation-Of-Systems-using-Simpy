
"""Customers are served by an employee who can serve one customer at a time. 
Customers are impatient and leave if they are not served after a certain amount of time.
Customers arrive every with negative exponential distribution """


import random
import simpy

SEMILLA = 42 
CANT_CLIENTES = 10  
INTERVALO_CLIENTES = 10 
MIN_PACIENCIA = 1  
MAX_PACIENCIA = 3  

def sistema(env, cantidad, intervalo, empleado): 
    for i in range(cantidad): 
        proxCliente = cliente(env, i, empleado, tiempoAtencion=12) 
        env.process(proxCliente)
        tProxCliente = random.expovariate(1.0 / intervalo)#
        yield env.timeout(tProxCliente)


def cliente(env, nombre, empleado, tiempoAtencion):
    tArribo = env.now 
    print(f'Cliente {nombre} llegó a las {tArribo:.2f}')

    with empleado.request() as req: 
        tPaciencia = random.uniform(MIN_PACIENCIA, MAX_PACIENCIA)
        resultado = yield req | env.timeout(tPaciencia)

        tEspera = env.now - tArribo

        if req in resultado: 
            print(f'Cliente {nombre} fue atendido a las {env.now:.2f} y esperó {tEspera:.2f}')
            tAtencion = random.expovariate(1.0 / tiempoAtencion)
            yield env.timeout(tAtencion)
            print(f'Cliente {nombre} terminó de ser antendido a las {env.now:.2f}')

        else: 
            print(f'Cliente {nombre} se fue por impaciencia a las {env.now:.2f} luego de esperar {tEspera:.2f}')


random.seed(SEMILLA) 
env = simpy.Environment()

empleado = simpy.Resource(env, capacity=1)
env.process(sistema(env, CANT_CLIENTES, INTERVALO_CLIENTES, empleado))
env.run()