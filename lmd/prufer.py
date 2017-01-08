from IPython.display import SVG, display, Image
import pydot

class Prufer():
    """
    Clase que representa al código de Prüfer de un árbol.
    
    Metodos:
   
    - Construir: Cuando la clase toma una lista, representando
    el código de Prüfer de un árbol, construye el árbol
    y devuelve un svg.
    
    - Construir: Dado una relación de nodos en forma de diccionario
    devuelve el código de Prüfer del árbol correspondiente.
    """

    def __init__(self, *args):
        if len(args) == 0:
            raise Exception("No se ha pasado ningún argumento")
        else:
            self.args = args

        #Nos aseguramos de que toma los argumentos correctos
        if isinstance(self.args[0], (list, tuple)):
            self.codigo = self.args[0]
            self.numero_nodos = len(self.codigo) + 2
        elif isinstance(self.args[0], (dict)):
            self.relaciones = self.args[0]
        else:
            raise TypeError("No se ha pasado un argumento válido")

    def construir(self):
        #No podemos construir si se ha pasado un árbol ya
        if not isinstance(self.args[0], (list, tuple)):
            raise TypeError("debe pasar como argumento una lista")

        #Creamos el grafo
        graph = pydot.Dot(graph_type='graph')
        #Obtenemos una lista con los nodos
        nodos = [x for x in range(1,self.numero_nodos +3)]
        #Copiamos el código dado
        copia_codigo = list(self.codigo)

        for _ in range(len(self.codigo)):
            #Buscamos el menor del los nodos que no está en el código
            menor_no_en_codigo = min([x for x in nodos if x not in copia_codigo])
            
            #Creamos un lado que va del primer elemento en el código
            #Al menor elemento que no está en el mismo
            lado = pydot.Edge(str(copia_codigo[0]), str(menor_no_en_codigo))

            #Quitamos los nodos que ya hemos unido
            copia_codigo.pop(0)
            nodos.remove(menor_no_en_codigo)

            #Añadimos el lado al grafo(árbol)
            graph.add_edge(lado)

        #Añadimos el último lado que queda

        lado = pydot.Edge(str(nodos[0]), str(nodos[1]))
        graph.add_edge(lado)

        #Mostramos el resultado
        display(SVG(graph.create_svg()) )
        
    def codigo(self):
        if not isinstance(self.args[0], (dict)):
            raise TypeError("debe pasar como argumento un diccionario")

        #Secuencia de nodos
        sec = [];
        d = dict(self.relaciones)

        #Obtenemos todos los nodos
        nodos = set(x for lis in list(d.items()) for x in lis[1] + [lis[0]] )
        
        for i in range(len(nodos)-2):
            #Buscamos las hojas
            min_val = min( [x for i in d.values() for  x in i if x not in d.keys()] )
            #Obtenemos el nodo asociado
            nodo = [k for k, v in d.items() if min_val in v][0]
            #Añadimos el nodo a la secuencia
            sec.append(nodo)
            #Quitamos la hoja
            d[nodo].remove(min_val)

            #Si hemos acabado con un nódo lo quitamos
            if len(d[nodo]) == 0:
                d.pop(nodo)

        return sec
