from Simulacion import Tiago_simulation 

def main():
    # Cantidades de procesos    
    cantidades_procesos = [25, 50, 100, 150, 200]
    
    # Intervalo de llegada de procesos
    intervalos_llegada = [10] 

    print("Iniciando Tarea 1. Copia los resultados de abajo:\n")
    print("Intervalo | Procesos | Tiempo Promedio | Desviación Est.")
    print("-" * 55)

    # Ciclo que recorre el intervalo configurado
    for intervalo in intervalos_llegada:
        
        # Ciclo que recorre las 5 cantidades de procesos
        for cantidad in cantidades_procesos:
            
            # Llama a la clase 
            simulador = Tiago_simulation(
                num_procesos=cantidad,
                intervalo_llegada=intervalo,
                ram_total=100, # Memoria base de 100
                instrucciones_por_ciclos=3, # CPU normal de 3 instrucciones por turno
                num_cpus=1 # Un solo procesador
            )
            
            # Corre la simulación y recibimos los datos matemáticos
            promedio, desviacion = simulador.ejecutar()
            
            # Imprime el resultado 
            print(f"    {intervalo:2}    |   {cantidad:3}    |      {promedio:.2f}      |      {desviacion:.2f}")

if __name__ == "__main__":
    main()