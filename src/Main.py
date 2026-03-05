import matplotlib.pyplot as plt
from Simulacion import Tiago_simulation

def main():
    plt.style.use('ggplot') 

    # Las diferentes cantidades de procesos 
    cantidades_procesos = [25, 50, 100, 150, 200]
    # Generará 3 gráficas distintas, una por cada intervalo
    intervalos = [10, 5, 1] 

    # Aquí configuramos las cantidades de la Tarea 3 y 4
    estrategias = [
        {"nombre": "Base (RAM=100, 1 CPU, Vel=3)", "ram": 100, "vel": 3, "cpus": 1},
        {"nombre": "Estrategia A (RAM=200)", "ram": 200, "vel": 3, "cpus": 1},
        {"nombre": "Estrategia B (CPU Vel=6)", "ram": 100, "vel": 6, "cpus": 1},
        {"nombre": "Estrategia C (2 CPUs)", "ram": 100, "vel": 3, "cpus": 2}
    ]

    print(f"{'Intervalo':<10} | {'Estrategia':<30} | {'Procesos':<10} | {'Promedio':<10} | {'Desviación Est.'}")
    print("-" * 85)

    # Ciclo que cambia los intervalos (10, 5, 1)
    for intervalo in intervalos:
        # Crea un lienzo nuevo para la gráfica con buen tamaño
        plt.figure(figsize=(10, 6))

        # Ciclo que cambia la configuración de la computadora (prueba las 4 estrategias)
        for est in estrategias:
            promedios_estrategia = []
            
            # Ciclo que cambia la cantidad de procesos (de 25 hasta 200)
            for cantidad in cantidades_procesos:
                
                # Llama al motor de simulación con los datos de la estrategia actual
                simulador = Tiago_simulation(
                    num_procesos=cantidad,
                    intervalo_llegada=intervalo,
                    ram_total=est["ram"],
                    instrucciones_por_ciclos=est["vel"],
                    num_cpus=est["cpus"]
                )
                
                # Ejecuta la simulación y extrae solo el promedio de tiempo
                promedio, desviacion = simulador.ejecutar()

                # Imprime los resultados (promedio y desviación) directamente en la consola
                print(f"{intervalo:<10} | {est['nombre']:<30} | {cantidad:<10} | {promedio:<10.2f} | {desviacion:.2f}")

                # Guarda el resultado para graficarlo después
                promedios_estrategia.append(promedio)

            plt.plot(cantidades_procesos, promedios_estrategia, marker='D', markersize=7, linewidth=2.5, label=est["nombre"])

        plt.title(f"Tiempo Promedio vs Procesos (Llegada cada {intervalo} seg)", fontsize=14, fontweight='bold')
        plt.xlabel("Cantidad de Procesos", fontsize=12)
        plt.ylabel("Tiempo Promedio en el Sistema", fontsize=12)
        plt.legend(loc="best", shadow=True, fancybox=True) 
        plt.xticks(cantidades_procesos) 

        # Aviso en la consola para saber en qué parte del proceso va el código
        print("-" * 85)
        print(f"Mostrando gráfica para intervalo {intervalo}. Cierra la ventana para continuar con la siguiente.")
        print("-" * 85)
        
        # Muestra la ventana en pantalla con la gráfica terminada
        plt.show()

if __name__ == "__main__":
    main()