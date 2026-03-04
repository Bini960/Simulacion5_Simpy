#Hola  tiago este es el codigo de simulación ( ❛︡ ‿‿ ❛︠ )
import simpy
import random
import statistics


class Tiago_simulation:

    def __init__(self,
                 num_procesos,
                 intervalo_llegada=10,
                 ram_total=100,
                 instrucciones_por_ciclos=3,
                 num_cpus=1,
                 random_seed=33): #semilla para los numeros

        self.num_procesos = num_procesos
        self.intervalo_llegada = intervalo_llegada
        self.ram_total = ram_total
        self.instrucciones_por_quantum = instrucciones_por_ciclos
        self.num_cpus = num_cpus
        self.random_seed = random_seed

        random.seed(self.random_seed)

        self.env = simpy.Environment() # esta cosa crea el entorno de simulación 
        self.RAM = simpy.Container(self.env, init=self.ram_total, capacity=self.ram_total)
        self.CPU = simpy.Resource(self.env, capacity=self.num_cpus)

        self.tiempos_en_sistema = []

    def proceso(self, nombre):

        tiempo_llegada = self.env.now

        memoria_necesaria = random.randint(1, 10)
        instrucciones_restantes = random.randint(1, 10)

        yield self.RAM.get(memoria_necesaria)

        while instrucciones_restantes > 0:

            with self.CPU.request() as req:
                yield req

                instrucciones_ejecutadas = min(
                    self.instrucciones_por_ciclos,
                    instrucciones_restantes
                )

                yield self.env.timeout(1)

                instrucciones_restantes -= instrucciones_ejecutadas

            if instrucciones_restantes <= 0:
                break

            decision = random.randint(1, 21)

            if decision == 1:
                yield self.env.timeout(1)
            elif decision == 2:
                pass

        yield self.RAM.put(memoria_necesaria)

        tiempo_salida = self.env.now
        self.tiempos_en_sistema.append(tiempo_salida - tiempo_llegada)

    def generador_procesos(self):

        for i in range(self.num_procesos):

            self.env.process(self.proceso(f"Proceso {i+1}"))

            tiempo_entre_llegadas = random.expovariate(
                1.0 / self.intervalo_llegada
            )

            yield self.env.timeout(tiempo_entre_llegadas)

    def ejecutar(self):

        self.env.process(self.generador_procesos())
        self.env.run()

        promedio = statistics.mean(self.tiempos_en_sistema)
        desviacion = statistics.stdev(self.tiempos_en_sistema) if len(self.tiempos_en_sistema) > 1 else 0 #len=cuantos elementos

        return promedio, desviacion
