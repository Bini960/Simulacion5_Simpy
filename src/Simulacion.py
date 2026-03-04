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
        
        # Utiliza una semilla para que se genere siempre la misma secuencia
        random.seed(self.random_seed)

        self.env = simpy.Environment() # crea el entorno de simulación 
        # Se usa un recurso tipo Container para simular la memoria RAM, con una cantidad inicial y capacidad total igual a ram_total.
        self.RAM = simpy.Container(self.env, init=self.ram_total, capacity=self.ram_total)
        # El CPU es modelado con una cola tipo Resource, con una capacidad igual al número de CPUs disponibles.
        self.CPU = simpy.Resource(self.env, capacity=self.num_cpus)

        self.tiempos_en_sistema = []

    def proceso(self, nombre):

        tiempo_llegada = self.env.now
        # Solicita una cantidad de memoria
        memoria_necesaria = random.randint(1, 10)
        # Cantidad de instrucciones totales a realizar
        instrucciones_restantes = random.randint(1, 10)

        yield self.RAM.get(memoria_necesaria)

        while instrucciones_restantes > 0:

            # Esperar que lo atienda el CPU
            with self.CPU.request() as req:
                yield req

                # Si el proceso tiene menos de tres instrucciones que le hace falta procesar, libera el CPU anticipadamente
                instrucciones_ejecutadas = min(
                    self.instrucciones_por_quantum,
                    instrucciones_restantes
                )
                # Atiende un proceso en una 1 unidad de tiempo
                yield self.env.timeout(1)

                instrucciones_restantes -= instrucciones_ejecutadas
            # Si el proceso ya no tiene instrucciones por realizar entonces pasa al estado "terminated"
            if instrucciones_restantes <= 0:
                break
            # Se genera un número entero al azar entre 1 y 21
            decision = random.randint(1, 21)

            if decision == 1:
                # Pasa a la cola de Waiting para hacer operaciones de I/O
                yield self.env.timeout(1)
            elif decision == 2:
                # Se dirige nuevamente a la cola de "ready"
                pass

        yield self.RAM.put(memoria_necesaria)

        tiempo_salida = self.env.now
        self.tiempos_en_sistema.append(tiempo_salida - tiempo_llegada)

    def generador_procesos(self):

        for i in range(self.num_procesos):

            self.env.process(self.proceso(f"Proceso {i+1}"))

            # Simular la llegada de procesos con una distribución exponencial
            tiempo_entre_llegadas = random.expovariate(
                1.0 / self.intervalo_llegada
            )

            yield self.env.timeout(tiempo_entre_llegadas)

    def ejecutar(self):
        # Inicia el generador que irá creando los procesos con sus tiempos de llegada
        self.env.process(self.generador_procesos())
        # Arranca el reloj de SimPy y corre la simulación hasta terminar todos los eventos
        self.env.run()

        promedio = statistics.mean(self.tiempos_en_sistema) # Calcula el promedio de tiempo que los procesos estuvieron en la computadora
        desviacion = statistics.stdev(self.tiempos_en_sistema) if len(self.tiempos_en_sistema) > 1 else 0 # Calcula la desviación estándar de los tiempos (solo si hay más de 1 dato para evitar errores)

        return promedio, desviacion
