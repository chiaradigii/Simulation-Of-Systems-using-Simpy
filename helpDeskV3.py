
import random
import simpy
import numpy as np


EMPLEADOS_NIVEL_1 = 15
EMPLEADOS_NIVEL_APPS = 10
EMPLEADOS_NIVEL_HARDWARE = 9
EMPLEADOS_NIVEL_OTROS = 8
EMPLEADOS_NIVEL_PRODUCT_OWNER = 4

MEDIA_NIVEL_UNO = 7000

MEDIA_NIVEL_APPS = 10000
DESVIO_NIVEL_APPS = 25000

MEDIA_NIVEL_HARDWARE = 10000
DESVIO_NIVEL_HARDWARE = 25000

MEDIA_NIVEL_OTROS = 10000
DESVIO_NIVEL_OTROS = 15000

MEDIA_NIVEL_PRODUCT_OWNER = 6000
DESVIO_NIVEL_PRODUCT_OWNER = 2000

#TIEMPO_ARRIBO = 120
TIEMPO_SIMULACION = 86400

ticketsAtendidos = 0

#tiempo entre arribos de tickets , segun horarios
t1 = max(60, np.random.normal(500, 150)) #usamos distribución normal
t2 = max(60, np.random.normal(270, 100))
t3 = max(60, np.random.normal(245, 90))
t4 = max(60, np.random.normal(320, 100))
t5 = max(60, np.random.normal(410, 190))
t6 = max(60, np.random.normal(445, 180))


class NivelUno:

    def __init__ (self, env):
        self.env = env
        self.staff = simpy.Resource(env,EMPLEADOS_NIVEL_1)#storage que atiende de a 15 por vez
        self.tiempoAtencion = max(60, np.random.exponential(MEDIA_NIVEL_UNO))

    def atender(self,ticket):
        yield self.env.process(self.env.timeout(self.tiempoAtencion))
        print(f'Nivel 1 finalizado para el ticket {ticket} a las {self.env.now:.0f}')


class Nivel:

    def __init__ (self, env, cant_empleados, media, desvio):
        self.env = env
        self.staff = simpy.Resource(env, cant_empleados)#storage que atiende de a 10 por vez
        self.tiempoAtencion = max(60, np.random.uniform(media, desvio))

    def atender(self,ticket):
        yield self.env.process(self.env.timeout(self.tiempoAtencion))
        print(f'Nivel finalizado para el ticket {ticket} a las {self.env.now:.0f}')

class HelpDesk:
    
    global ticketsAtendidos

    def __init__ (self, env, ticket):
        self.env = env
        self.ticket = ticket
        self.nivel = NivelUno(env) 

    def pasoPorNiveles(self):
        #self.nivel.atender(self.ticket) #ejecuto la atencion del primer nivel
        with self.nivel.staff.request() as request:
           yield request 
           yield self.env.process(self.nivel.atender(self.ticket)) #ejecuto el metodo atencion y le paso quien esta siendo atendido
           print(f'ticket {self.ticket} atendido en nivel actual a las {self.env.now:.0f}')


        siguiente = random.choices(population=["apps","hardware","otros","productOwner","end"], weights=[0.25, 0.35, 0.25, 0.05, 0.1])[0]

        #basandonos en los pesos de probabilidad veo cual es el siguiente nivel
        if siguiente == "apps":
            print(f'ticket {self.ticket} asignado al equipo de Apps a las {self.env.now:.0f}')
            self.nivel = Nivel(env,EMPLEADOS_NIVEL_APPS, MEDIA_NIVEL_APPS, DESVIO_NIVEL_APPS)
            self.atender()
            siguiente = random.choices(population=["productOwner","end"], weights=[0.40, 0.60])

            if siguiente == "productOwner":
                print(f'ticket {self.ticket} asignado a grupo Mejora-Product Owner a las {self.env.now:.0f}')
                self.nivel = Nivel(env,EMPLEADOS_NIVEL_PRODUCT_OWNER, MEDIA_NIVEL_PRODUCT_OWNER, DESVIO_NIVEL_PRODUCT_OWNER)
                self.atender()
            elif siguiente == "end":
                print(f'ticket {self.ticket} ha sido resuelto a las {self.env.now:.0f}')
                ticketsAtendidos += 1

        elif siguiente == "hardware":
            print(f'ticket {self.ticket} asignado al equipo de Hardware a las {self.env.now:.0f}')
            self.nivel = Nivel(env,EMPLEADOS_NIVEL_HARDWARE, MEDIA_NIVEL_HARDWARE, DESVIO_NIVEL_HARDWARE)
            self.atender()
        elif siguiente == "otros":
            print(f'ticket {self.ticket} asignado al equipo de Otros a las {self.env.now:.0f}')
            self.nivel = Nivel(env,EMPLEADOS_NIVEL_OTROS, MEDIA_NIVEL_OTROS, DESVIO_NIVEL_OTROS)
            self.atender()
        elif siguiente == "productOwner":
            print(f'ticket {self.ticket} asignado a grupo Mejora-Product Owner a las {self.env.now:.0f}')
            self.nivel = Nivel(env,EMPLEADOS_NIVEL_PRODUCT_OWNER, MEDIA_NIVEL_PRODUCT_OWNER, DESVIO_NIVEL_PRODUCT_OWNER)
            self.atender()
        elif siguiente == "end":
            print(f'ticket {self.ticket} ha sido resuelto a las {self.env.now:.0f}')
            ticketsAtendidos += 1
   
    def atender(self):
        with self.nivel.staff.request() as request:
           yield request 
           yield self.env.process(self.nivel.atender(self.ticket)) #ejecuto el metodo atencion y le paso quien esta siendo atendido


def ticket(env,nombre, empleado):
    tArribo = env.now
    print(f'Ticket {nombre} llegó a las {tArribo:.2f}')

    with empleado.request() as req: 
        yield req
        print(f'Ticket {nombre} tomado por el empleado a las {env.now:.2f}')
        yield env.timeout(empleado.tiempoAtencion)
        print(f'empleado terrmino de atender el ticket {ticket} a las {env.now:.2f}')


def sistema(env, empleado):
    for i in range(10): 
        proxTicket = ticket(env, i, empleado) 
        env.process(proxTicket) #luego de crearlo lo ejecuto en el proceso y genero la transaccion
        tProx = proximoArribo(proximoArribo(500, 150))
        yield env.timeout(tProx)
        print(f'nuevo arribo a las {env.now:.0f}')
   
        
def proximoArribo(media,normal):
    return max(60, np.random.normal(media, normal)) 

    

def HelpDesk(env):

    emp_level1 = simpy.Resource(env,EMPLEADOS_NIVEL_1)
    env.process()
    
    


    #self.nivel.atender(self.ticket) #ejecuto la atencion del primer nivel
    with self.nivel.staff.request() as request:
        yield request 
        yield self.env.process(self.nivel.atender(self.ticket)) #ejecuto el metodo atencion y le paso quien esta siendo atendido
        print(f'ticket {self.ticket} atendido en nivel actual a las {self.env.now:.0f}')


    siguiente = random.choices(population=["apps","hardware","otros","productOwner","end"], weights=[0.25, 0.35, 0.25, 0.05, 0.1])[0]

    #basandonos en los pesos de probabilidad veo cual es el siguiente nivel
    if siguiente == "apps":
        print(f'ticket {self.ticket} asignado al equipo de Apps a las {self.env.now:.0f}')
        self.nivel = Nivel(env,EMPLEADOS_NIVEL_APPS, MEDIA_NIVEL_APPS, DESVIO_NIVEL_APPS)
        self.atender()
        siguiente = random.choices(population=["productOwner","end"], weights=[0.40, 0.60])

        if siguiente == "productOwner":
            print(f'ticket {self.ticket} asignado a grupo Mejora-Product Owner a las {self.env.now:.0f}')
            self.nivel = Nivel(env,EMPLEADOS_NIVEL_PRODUCT_OWNER, MEDIA_NIVEL_PRODUCT_OWNER, DESVIO_NIVEL_PRODUCT_OWNER)
            self.atender()
        elif siguiente == "end":
            print(f'ticket {self.ticket} ha sido resuelto a las {self.env.now:.0f}')
            ticketsAtendidos += 1

    elif siguiente == "hardware":
        print(f'ticket {self.ticket} asignado al equipo de Hardware a las {self.env.now:.0f}')
        self.nivel = Nivel(env,EMPLEADOS_NIVEL_HARDWARE, MEDIA_NIVEL_HARDWARE, DESVIO_NIVEL_HARDWARE)
        self.atender()
    elif siguiente == "otros":
        print(f'ticket {self.ticket} asignado al equipo de Otros a las {self.env.now:.0f}')
        self.nivel = Nivel(env,EMPLEADOS_NIVEL_OTROS, MEDIA_NIVEL_OTROS, DESVIO_NIVEL_OTROS)
        self.atender()
    elif siguiente == "productOwner":
        print(f'ticket {self.ticket} asignado a grupo Mejora-Product Owner a las {self.env.now:.0f}')
        self.nivel = Nivel(env,EMPLEADOS_NIVEL_PRODUCT_OWNER, MEDIA_NIVEL_PRODUCT_OWNER, DESVIO_NIVEL_PRODUCT_OWNER)
        self.atender()
    elif siguiente == "end":
        print(f'ticket {self.ticket} ha sido resuelto a las {self.env.now:.0f}')
        ticketsAtendidos += 1







def setup(env):
  t_arribos = t1 #0 a 8 hs

#VER SI SACAR ESTO
  for i in range(1,6):
    proxTicket = ticket(env,proximoArribo(500, 150))
    env.process(HelpDesk(env, f"Ticket_{i}").pasoPorNiveles()) #Arranco los arribos de tickets

  while True:
      #ver para cuando sea despues de las 8hs que numero poner!!!
      if(env.now >= 28800 and env.now < 39600 ):  t_arribos = t2 # 8 a 11hs
      elif(env.now >= 39600 and env.now < 54000 ): t_arribos = t3 # 11 a 15hs
      elif(env.now >= 54000 and env.now < 64800 ): t_arribos = t4# 15 a 18 hs
      elif(env.now >= 64800 and env.now < 75600 ): t_arribos = t5 #18 a 21 hs
      elif(env.now >= 75600): t_arribos = t6 #21 a 24 hs

      yield env.timeout(t_arribos)#Me detengo hasta que atiendan el ticket
      i+=1
      env.process(HelpDesk(env, f"Ticket_{i}")) #hago nacer otro ticket



print('Comenzando la simulacion del Help Desk')
env = simpy.Environment()
env.process(setup(env))#ejecuto un proceso (transaccion), que es la ejecución de setup
env.run(until=TIEMPO_SIMULACION)

print('Tickets atendidos:', ticketsAtendidos)