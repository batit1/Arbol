import heapq

class EstadoSemestre:
    def __init__(self, semanas, asignaturas, estres, camino):
        self.semanas = semanas
        self.asignaturas = asignaturas
        self.estres = estres
        self.camino = camino

    def calcular_suspensos(self):
        return sum(1 for nivel in self.asignaturas.values() if nivel < 2)

    def calcular_cota(self):
        mejoras_necesarias = sum(2 - nivel for nivel in self.asignaturas.values())
        mejoras_posibles = self.semanas * 2
        
        if self.asignaturas['EDA II'] < 2 and self.semanas < (2 - self.asignaturas['EDA II']):
            return 99
            
        inevitables = max(0, (mejoras_necesarias - mejoras_posibles) // 2)
        return self.calcular_suspensos() + inevitables

    def __lt__(self, otro):
        if self.calcular_cota() != otro.calcular_cota():
            return self.calcular_cota() < otro.calcular_cota()
        return self.estres < otro.estres

def resolver_semestre():
    estado_inicial = {'EDA II': 1, 'Ecuaciones': 1, 'Calculo': 1, 'Geometria': 1}
    raiz = EstadoSemestre(3, estado_inicial, 0, [])
    
    heap = [raiz]
    mejor_solucion = None
    min_suspensos_global = 5
    
    while heap:
        actual = heapq.heappop(heap)
        
        if actual.calcular_cota() > min_suspensos_global:
            continue
            
        if actual.semanas == 0:
            suspensos = actual.calcular_suspensos()
            if suspensos < min_suspensos_global:
                min_suspensos_global = suspensos
                mejor_solucion = actual
            continue

        opciones = [
            ("Estudiar Fuerte", 0),
            ("Estudiar Normal", 0),
            ("LoL", 1),
            ("Fiesta", 0)
        ]

        for nombre_acc, extra_estres in opciones:
            nuevas_asig = actual.asignaturas.copy()
            
            if nombre_acc == "Estudiar Fuerte":
                nuevas_asig['EDA II'] = min(2, nuevas_asig['EDA II'] + 1)
                for k in nuevas_asig:
                    if k != 'EDA II' and nuevas_asig[k] < 2:
                        nuevas_asig[k] += 1
                        break
            elif nombre_acc == "Estudiar Normal":
                for k in nuevas_asig:
                    if nuevas_asig[k] < 2:
                        nuevas_asig[k] += 1
                        break
            elif nombre_acc == "Fiesta":
                for k in reversed(list(nuevas_asig.keys())):
                    if nuevas_asig[k] > 0:
                        nuevas_asig[k] -= 1
                        break

            nuevo_nodo = EstadoSemestre(
                actual.semanas - 1, 
                nuevas_asig, 
                actual.estres + extra_estres,
                actual.camino + [nombre_acc]
            )
            heapq.heappush(heap, nuevo_nodo)

    return mejor_solucion

solucion = resolver_semestre()
print(f"Mejor estrategia: {solucion.camino}")
print(f"Suspensos finales: {solucion.calcular_suspensos()}")
print(f"Estado final: {solucion.asignaturas}")