from operator import itemgetter
from collections import defaultdict
import functools

from IPython.display import SVG, display, Image
import graphviz as gv


class Sucesion():
    """
    Esta clase aplica el algoritmo de Havel-Hakimi sobre una sucessión
    de grados de vertices. Primero realiza la demolición y después la 
    reconstrucción.

    Atributos:
    sucesion: Lista de grados que se ha pasado como argumento
    numerados: Nueva lista con los vertices numerados
    descompuesto: Último paso tras aplicar la demolición
    sucesion_grafica: Guarda si es o no sucesion grafica
    demolido: Guarda si ha aplicado ya el algoritmo de demolicion
    relations: Diccionario con  la relación de grados
    """
    
    def __init__(self, lista):

        if not isinstance(lista, (list, tuple)):
            raise TypeError("debe pasar como argumento una lista")
        else:
            self.sucesion = lista
            self.numerados = [[x,i] for i,x in enumerate(self.sucesion,1)]
            self.descompuesto = []
            self.sucesion_grafica = False
            self.demolido = False

    def es_grafica(self):
        #Vemos si la suma de los vertices es divisible por 2
        #O que el grado del primero seo mayor que el número de vertices
        if sum([x[0] for x in self.numerados]) % 2 or self.numerados[0][0] > len(self.numerados):
            return False

        #Comprobamos si ya se ha demolido
        if not self.demolido:
            self.demolicion(False)

        #Si todos son 0 en la lista de demolición
        if all(v[0] == 0 for v in self.descompuesto):
            return True

        return False

    def demolicion(self, mostrar=True):

        """
        Mostrar = True hace que se muestre el proceso paso a paso
        """
        
        numerados = self.numerados
        #Creamos un diccionario que va a almacenar listas de relaciones
        relations = defaultdict(list)

        #Si queremos que se muestre el procedimiento imprimimos el
        #estado inicial
        if mostrar:
            print([x for x,y in numerados])

        #Mientras haya valores positivos
        while any([v[0] > 0 for v in numerados]):
            
            #Tomamos el primer elemento
            primer = numerados[0][0]
            #Para los siguiente n elementos
            for i in range(1,primer+1):
                #restamos 1 a su valor
                numerados[i][0] -= 1
                #Añadimos la relacion de vertices
                relations[numerados[0][1]].append(numerados[i][1])
                #Ponemos a 0 el grado del primero
                numerados[0][0] = 0
                
            #Mostramos el paso
            if mostrar:
                print([x for x,y in sorted(numerados, key=itemgetter(1))])
                #Reordenamos la lista
            numerados = sorted(numerados,reverse=True, key=itemgetter(0))

        self.descompuesto = numerados
        self.relations = relations
        self.demolido = True

        return None

    
    def reconstruccion(self):
        #Aplicamos el algoritmo de demolicion
        #En caso de que no se haya hecho
        if not self.demolido:
            self.demolicion(False)
            
        if self.es_grafica():
            self.__dibuja()
        else:
            raise Exception("No es sucesión grafica")

        return None
        

    def __dibuja(self):
        g = gv.Graph(format='svg')

        tabla = dict(self.relations)
        inicial = self.sucesion

        for relacion in tabla.items():
            g.node(str(relacion[0])  ,label= str(inicial[relacion[0]-1]))
            for pareja in relacion[1]:
                par = g.node(str(pareja), label= str(inicial[pareja-1]))
                g.edge(str(relacion[0]), str(pareja) )

        salida= g.render()
        display(SVG(salida))
        return None

    def relaciones(self):
        return self.relations
