
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




def proximoArribo(env,media,normal):
    t = max(60, np.random.normal(media, normal)) 
    yield env.timeout(t)
    print(f'nuevo arribo a las {env.now:.0f}')

print('Comenzando la simulacion del Help Desk')

env = simpy.Environment()

    #VER SI SACAR ESTO
for i in range(1,6):
    proximoArribo(env,500, 150) #0 a 8 hs
    helpDesk = HelpDesk(env, f"Ticket_{i}")
    env.process(helpDesk.pasoPorNiveles()) #Arranco los arribos de tickets
env.run(until=TIEMPO_SIMULACION)

while True:
    #ver para cuando sea despues de las 8hs que numero poner!!!
    if(env.now >= 28800 and env.now < 39600 ):  proximoArribo(270, 100)  # 8 a 11hs
    elif(env.now >= 39600 and env.now < 54000 ):  proximoArribo(245, 90) # 11 a 15hs
    elif(env.now >= 54000 and env.now < 64800 ): proximoArribo(320, 100)# 15 a 18 hs
    elif(env.now >= 64800 and env.now < 75600 ):  proximoArribo(410, 190) #18 a 21 hs
    elif(env.now >= 75600): proximoArribo(445, 180) #21 a 24 hs
    i+=1
    env.process(HelpDesk(env, f"Ticket_{i}")) #hago nacer otro ticket






#print('Tickets atendidos:', ticketsAtendidos)

