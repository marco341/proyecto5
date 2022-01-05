class Biblioteca:
    
    def __init__(self):
        self.listaAristas = []

    #Modelo Gm,n de malla. Crear m*n nodos. Para el nodo ni,j crear una arista con el nodo ni+1,j
    # y otra con el nodo ni,j+1, para i<m y j<n
    def grafoMalla(self, n, m, dirigido=False):
            
        """
        Genera grafo de malla
        :param m: número de columnas (> 1)
        :param n: número de filas (> 1)
        :param dirigido: el grafo es dirigido?
        :return: grafo generado
        """
        coordenada = []
        coordenadaH = []
        coordenadaV= []
        borrar = []
        vertical = []
        horizontal = [] 
        #Genero cooredenadas de tamaño m*n
        for i in range(0, m):
            for j in range(0, n):
                coordenada.append([i, j])

        #Inido el limite derecho de la maya 
        for fin in range(n-1, len(coordenada), n):
            borrar.append((fin, fin+1))
        
        #Generamos los aristas sobre el lado derecho
        for coordenadaH in range(0, len(coordenada)):
            vertical.append((coordenadaH, coordenadaH+1))
        #eliminamos aritas que no pertenecen a la maya                   
        vetical=list(set(vertical)-set(borrar))
        #generamos la aritas verticales 
        for i in range(0, len(coordenada)):    
            coordenadaV.append((i, i+n))

        #Selecciono las aristas que seran generas para el grafo
        longitud = len(coordenadaV)-n
        s=0
        while s < len(coordenadaV):
            if s == longitud:
                s = len(coordenadaV)
            else:
                horizontal.append(coordenadaV[s])
                s+=1
        self.listaAristas = horizontal + vetical
        
            
    #Modelo Gn,m de Erdös y Rényi. Crear n nodos y elegir uniformemente al azar m distintos pares de distintos vértices.
    def grafoErdosRenyi(self, n, m, dirigido=False, auto=False):
        import random as rd
        """
        Genera grafo aleatorio con el modelo Erdos-Renyi
        :param n: número de nodos (> 0)
        :param m: número de aristas (>= n-1)
        :param dirigido: el grafo es dirigido?
        :param auto: permitir auto-ciclos?
        :return: grafo generado
        """
        aristarepe = []
        s=0
        
        while s < m: #proporciono el la cantidad de aritrias que se puede generar 
            #Selecciono dos nodos al azar 
            u=rd.randint(1, n) 
            v=rd.randint(1, n)
            #Si estan repetidos realizo otro intento
            if u == v:
                s-=1
            elif u != v:
                nod2= u,v
            if nod2 in aristarepe:
                s-=1
            else:
                aristarepe.append((nod2))
            s+=1
        self.listaAristas = aristarepe
        
    #Modelo Gn,p de Gilbert. Crear n nodos y poner una arista entre cada par independiente y uniformemente con probabilidad p.
    def grafoGilbert(self, n, p, dirigido=False, auto=False):
        import random as rd
        """
        Genera grafo aleatorio con el modelo Gilbert
        :param n: número de nodos (> 0)
        :param p: probabilidad de crear una arista (0, 1)
        :param dirigido: el grafo es dirigido?
        :param auto: permitir auto-ciclos?
        :return: grafo generado"""
    
        l=list(range(n)) #se genera una lista de nodos

        #Se lee el los nodos y se realiza un cilco for
        l = ([(l,j) 
            for l in range(n)   
                for j in range(l)   
                    if rd.random() < p]) #toma la decisicon mediante un promedio si se realiza union o no mediate un true o False
        
        self.listaAristas = l

    #Modelo Gn,r geográfico simple. Colocar n nodos en un rectángulo unitario con coordenadas 
    #uniformes (o normales) y colocar una arista entre cada par que queda en distancia r o menor.
    def grafoGeografico(self, n, r, x, y, dirigido=False, auto=False):
        import random as rd
        """
        Genera grafo aleatorio con el modelo geográfico simple
        :param n: número de nodos (> 0)
        :param r: distancia máxima para crear un nodo (0, 1)
        :param dirigido: el grafo es dirigido?
        :param auto: permitir auto-ciclos?
        :return: grafo generado
        """
        coor = []
        numNodoCoor = []
        for i in range(x):
            for j in range(y):
                coor.append((i, j))

        # Genera el numero numero del nodos y su cooredenada 
        for i in range(0, len(coor)-1): 
            j = i, coor[i]
            numNodoCoor.append(j)

        nodoGPS = [] # coordenadas en el cuadrado (m*m)-1
        listaNodo =[]
        #Genero lista de nodos posibles 
        for i in range(n-1):
            listaNodo.append(i)

        #genero al azar nodos dentro del limiete de mis coordenadas 
        totalNodos =rd.randint(1, n-1)
        s=0
        while s < totalNodos: #selecciono al azar el nodo
                
            nodo = rd.choice(listaNodo)
            tomoNodo = listaNodo.index(nodo)
            nodoGPS.append(nodo)

            del listaNodo[tomoNodo] #elimino para no tener repetidos 

            s+=1

        listaNodoRadio =[]

        #Asigno el nodos seleccionado con su coordenada
        for i in range(0, len(nodoGPS)):
            j=numNodoCoor[nodoGPS[i]]
            listaNodoRadio.append(j)

        s=0
        nodoOrigen = []
        nodoMapa = []
        while s < totalNodos:
            
            #tomo un nodo de listaNodoRadio y lo agrego a nodoOtogen
            nodoOrigen.append(listaNodoRadio[0])
            #Elimino el nodo listaNodoRadio que tome
            del listaNodoRadio[0]
            #se utilizara el metodo de puntos dnetro de un circulo donde nodoOrigen es el nodo del centro 
            # y listaNodoRadio son los nodos cercanos a ese nodo

            for i in range(0, len(listaNodoRadio)):
                rN = ((listaNodoRadio[i][1][0]-nodoOrigen[s][1][0])**2) + ((listaNodoRadio[i][1][1]-nodoOrigen[s][1][1])**2)
                if rN <= r:
                    nodoMapa.append((nodoOrigen[s][0], listaNodoRadio[i][0]))         
            s+=1

        self.listaAristas = nodoMapa

    #Variante del modelo Gn,d Barabási-Albert. Colocar n nodos uno por uno, asignando a cada uno d aristas a vértices distintos de tal manera
    # que la probabilidad de que el vértice nuevo se conecte a un vértice existente v es proporcional a la cantidad de aristas que v tiene 
    # actualmente - los primeros d vértices se conecta todos a todos.
    def grafoBarabasiAlbert(self, n, d, dirigido=False, auto=False):
        import random as rd
        """
        Genera grafo aleatorio con el modelo Barabasi-Albert
        :param n: número de nodos (> 0)
        :param d: grado máximo esperado por cada nodo (> 1)
        :param dirigido: el grafo es dirigido?
        :param auto: permitir auto-ciclos?
        :return: grafo generado
        """
        l= n
        m=range(n)

        listaNodos = []
        for i in range(0, len(m)):
            listaNodos.append(i)

        nodoUtiles = []
        listaTemporal = []
        nodoAceptado = []
        nodoRevicion = []
        nodoSeleccionados = []
        s=0
        x=0
        #contrullo tomo cada nodo de la lista
        while s < l: 
            s1 = 0
            for i in listaNodos:
                nodoUtiles.append(i)
            del nodoUtiles[0]

            while s1 < d:

                if s != 0 and s1 == 0:
                    for i  in range(0, len(listaTemporal)):
                        j = listaTemporal[i][1]
                        if j == s:
                            s1+=1
                    
                #reglas de promedio para nueva arista
                if s1 != 0:
                    p = 1-(s1/d)
                else:
                    p = 1
                    c = 0

                # Creo la primera aista
                # Proporciono una probavilidad para unirlos al siguiente nodo o no
                if rd.random() < p: # Si es True lo gurdo
                    if s != nodoUtiles[c]:
                        nodoCandidato = s, nodoUtiles[c] #genero una arista
                        listaTemporal.append(nodoCandidato) #la cargo a una pila
                        nodoSeleccionados.append(s)
                        nodoSeleccionados.append(nodoUtiles[c])
                        del nodoUtiles[c] #elimino 
                    
                else:
                    s1-=1
                    c+=1

                # pregunnro si ya lei todos los nodos del grafo
                if c == len(nodoUtiles):
                    c = 0

                s1+=1
            nodoUtiles = [ ]
            print
            s+=1
        
        self.listaAristas = listaTemporal

    #Modelo Gn Dorogovtsev-Mendes. Crear 3 nodos y 3 aristas formando un triángulo. Después, para cada nodo adicional,
    # se selecciona una arista al azar y se crean aristas entre el nodo nuevo y los extremos de la arista seleccionada. 
    def grafoDorogovtsevMendes(self, n, dirigido=False):
        import random as rd
        """
        Genera grafo aleatorio con el modelo Barabasi-Albert
        :param n: número de nodos (≥ 3)
        :param dirigido: el grafo es dirigido?
        :return: grafo generado
        """
        
        listaNodo = []
        candidatosNodo = []
        trinagulo = []

        for i in range(n):
            listaNodo.append(i)
        
        # Genero un base para conectrar los otros triagulos 
        s = 0
        while s < 3:
        
            nodo = rd.choice(listaNodo) #selecciono un nodo al hazar
            tomoNodo = listaNodo.index(nodo)
            candidatosNodo.append(nodo) #lista candidato

            del listaNodo[tomoNodo] #Elimino el nodo tomado

            s+=1
        # Construyo el primer triangulos
        trinagulo.append((candidatosNodo[0], candidatosNodo[1]))
        trinagulo.append((candidatosNodo[1], candidatosNodo[2]))
        trinagulo.append((candidatosNodo[0], candidatosNodo[2]))
        #Se lecciono un nodo de los disponibles y lo uno con dos nodos de mi lista de candidatos
        # se elmina el nodo tomado y se continua asta finalizar todos los nodos
        s1 = 0
        while s1 < len(trinagulo):
            if len(listaNodo) == 0:
                s1 = len(trinagulo) #Rompe el ciclo
            else:

                nodoB = rd.choice(listaNodo) #elijo un nodo
                nodoT = listaNodo.index(nodoB) #lo convierto en index para eliminar
                
                arista_Azar = rd.choice(trinagulo)
                
                    
                trinagulo.append((nodoB, arista_Azar[0]))
                trinagulo.append((nodoB, arista_Azar[1]))

                del listaNodo[nodoT]            
        
        self.listaAristas = trinagulo
        print(self.listaAristas)


class Coordenada:    
    def __init__(self, i):
        self.idd=i #es la id de los datos
        self.coords =[] #genera la listas coordenadas de cada nodo

    def agregarCoordenadas(self, x, y): # Agregar nodod coordenadas
        self.coords.append(x)
        self.coords.append(y)

class Display:
    def __init__(self):
        self.coordenadas_dic = {}
        
    def agregaVerticeCoordenada(self, id):
        if id not in self.coordenadas_dic:
            self.coordenadas_dic[id]= Coordenada(id)

    def agregarCoordnada(self, n, x, y):        
        self.coordenadas_dic[n].agregarCoordenadas(x, y)  

class Display_coor:

    def display_coor(self, n, tam_X, tam_Y):
        import random as rd

        d = Display()

        self.coordenada_unica = []

        s = 0
        while s < n:
            eje_X = rd.randint(0, tam_X)
            eje_Y = rd.randint(0, tam_Y)

            ejes = (eje_X, eje_Y)

            if ejes not in self.coordenada_unica:
                d.agregaVerticeCoordenada(s)
                d.agregarCoordnada(s, eje_X, eje_Y)
                s+=1
            else:
                s = s
        return d.coordenadas_dic
 
#-------------------------------------------------------------------------------
#// generamos lista de nodos con vecinos 
class Vertice:

    #se generan los vertices y los vecinos  donde v es un veciono y p es el peso 
    def __init__(self, i):
        self.id=i #es la id de los datos
        self.vecinos =[]
    def agregarVecino(self, v): # nos inica v el nodo y p el peso del nodo
        if not v in self.vecinos:
            self.vecinos.append(v)

class Grafica:
    def __init__(self):
        self.vertices ={}

    def agregaVertice(self, id):
        if id not in self.vertices:
            self.vertices[id]= Vertice(id)
    
    def agregarAristas(self, a, b): #contrulle la arista y les proporciona el peso p
        if a in self.vertices and b in self.vertices:
            
            self.vertices[a].agregarVecino(b)   

#///////////////----- Clase PyGame para mostrar grafo -----------//////////////
class PyGame:
    def __init__(self):
        self.g = Grafica()
        self.d = Display()
        self.dc = Display_coor()
        
    def crearGrafos(self, listas, no_nodos):
                
        tam_X = 1028
        tam_Y = 600

        for i in range(no_nodos):
            self.g.agregaVertice(i)

        for i in range(0,no_nodos):
            self.d.agregaVerticeCoordenada(i)
        listasLimpia = []
        for i in listas:
            for j in i:
                listasLimpia.append(j)

        for i in range(0, len(listasLimpia)-1, 3):
            self.g.agregarAristas(listasLimpia[i], listasLimpia[i+1])

        diccionario_Coor = self.dc.display_coor(no_nodos, tam_X, tam_Y)
        
        self.pygame(diccionario_Coor, self.g.vertices, tam_X, tam_Y)
    
    def algortimoSpring(self, diccionario_Coor, vertices, tam_X, tam_Y):
        import math

        c1 = 2
        c2 = 1
        c3 = 1
        c4 = 0.1
        minimo = 50

        for i in vertices:
            vecinos = vertices[i].vecinos
            fx=0
            fy=0

            for n in vertices:
                
                if n in vecinos:
                    
                    x1 = diccionario_Coor[i].coords[0]
                    y1 = diccionario_Coor[i].coords[1]

                    x2 = diccionario_Coor[n].coords[0]
                    y2 = diccionario_Coor[n].coords[1]

                    d = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
                
                    if d<minimo: 
                        continue

                    force= c1*math.log(d/c2)
                    radians = math.atan2(y2 - y1, x2 - x1)
                    fx+= force*math.cos(radians)
                    fy+=force*math.sin(radians)
                else:
                    
                    x1 = diccionario_Coor[i].coords[0]
                    y1 = diccionario_Coor[i].coords[1]

                    x2 = diccionario_Coor[n].coords[0]
                    y2 = diccionario_Coor[n].coords[1]

                    d = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
                    if d==0:
                        continue
                    force= c3/math.sqrt(d)
                    radians = math.atan2(y2 - y1, x2 - x1)
                    fx-= force*math.cos(radians)
                    fy-=force*math.sin(radians)

            diccionario_Coor[i].coords[0]+=c4*fx
            diccionario_Coor[i].coords[1]+=c4*fy
        return diccionario_Coor
    
    def pian(self, ventana,  diccionario_Coor, vertices, tam_X, tam_Y):
        import  pygame, sys
        BLACK   = (  0,   0,   0)
        ventana.fill(BLACK)
        self.dibujar(ventana, diccionario_Coor, vertices)
        pygame.display.update()
        diccionario_Coor = self.algortimoSpring(diccionario_Coor, vertices, tam_X, tam_Y)
        return (diccionario_Coor)


    def dibujar(self, ventana, diccionario_Coor, vertices):

        import  pygame, sys


        BLACK   = (  0,   0,   0)
        WHITE   = (255, 255, 255)
        GREEN   = (  0, 255,   0)
        RED     = (255,   0,   0)
        BLUE    = (  0,   0, 255)


        for i in range(0, len(vertices)):
            
            veci = vertices[i].vecinos
            aro1 = i
            x1 = int(diccionario_Coor[aro1].coords[0])
            y1 = int(diccionario_Coor[aro1].coords[1])

            for n in range(0, len(veci)):
                aro2 = veci[n]

                x2 = int(diccionario_Coor[aro2].coords[0])
                y2 = int(diccionario_Coor[aro2].coords[1])

                pygame.draw.aaline(ventana, WHITE,(x1, y1),(x2, y2),3)

                pygame.draw.circle(ventana, BLUE,(x1, y1),4)
                pygame.draw.circle(ventana, BLUE,(x2, y2),4)

                

    def pygame(self, diccionario_Coor, vertices, tam_X, tam_Y):

        import  pygame, sys

        pygame.init()
        ventana = pygame.display.set_mode((tam_X, tam_X))
        pygame.display.set_caption("Proyecto 5 ")

        
        clock = pygame.time.Clock()

        s = 0
        while True:
            clock.tick(80)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
           
            newDiccionario_Coor = self.pian(ventana, diccionario_Coor, vertices, tam_X, tam_X)
            diccionario_Coor = newDiccionario_Coor

class NodosAristas:
    def __init__(self):
        self.b = Biblioteca()
        self.g = Grafica()    
        self.p = PyGame()  
          
    def nodoID(self, n, listaAristas):
        import random as rd

        listaLipia = [] #Elimino los parentecis de la lista 
        
        self.grafo_Peso = []
        self.peso = []

        for i in listaAristas:
            for j in i:
                listaLipia.append(j)

        for i in range(0, len(listaLipia)-1, 2): #Recorro la lista de dos en dos y agrego un nuevo valor que sera el peso 
            p = rd.randint(20, 30)
            self.peso.append((listaLipia[i], listaLipia[i+1], p))

        print('Grafo', '\n', self.peso)

        self.p.crearGrafos(self.peso, n)
#__________________________Menu_______________________________________   

class Menu:
    def __init__(self): 
        import random as rd
        self.b = Biblioteca()
        self.g = Grafica()
        self.nod = NodosAristas()   

    def opcionesMenu(self, opcion): 
        import random as rd
        #////////////////////////////////////////////////////////////////////////7  
        #se obteiene n nodos al azar
        self.n = 10 #rd.randint(0, 5) ########## se indica los nodos al azzar
        while opcion != 0:
            if opcion == 1:
                m=10 #rd.randint(0, 6) #### se indica los nodos m para la malla
                n = self.n*m
                print('Graficar la malla')
                self.b.grafoMalla(self.n, m) 
                self.nod.nodoID(n, self.b.listaAristas)
                
            elif opcion == 2:
                m=rd.randint(400, self.n) #### indica el número de aristas para Erdos Renyi 
                print('Graficar la Erdos Renyi')
                self.b.grafoErdosRenyi(self.n, m)
                self.nod.nodoID(self.n, self.b.listaAristas)

            elif opcion == 3:
                print('Graficar la Gilbert')
                #Se proporciona un promedio 
                p = 0.25
                self.b.grafoGilbert(self.n, p)
                self.nod.nodoID(self.n, self.b.listaAristas)
             
            elif opcion == 4:
                print('Graficar la Geografico')
                r = int(input("Indique un radio "))
                x = int(input("Indique una longitud x"))
                y = int(input("Indique una altura y"))
                self.b.grafoGeografico(self.n, r, x, y) # es importante generar un cuadrado x y y confome al tamaño de n
                print(self.b.listaAristas)
                self.nod.nodoID(self.n, self.b.listaAristas)
                               
            elif opcion == 5:
                print('Graficar la BarabasiAlbert')
                d = rd.randint(40, self.n-1)
                self.b.grafoBarabasiAlbert(self.n, d)
                self.nod.nodoID(self.n, self.b.listaAristas)
                               
            elif opcion == 6:
                print('Graficar la Dorogovtsev Mendes')
                self.b.grafoDorogovtsevMendes(self.n)   
                self.nod.nodoID(self.n, self.b.listaAristas)
                                
            elif opcion == 0:
                print('Gracias')
            else:
                print('esa opcion no esta en el menú')
            
            
            opcion = int(input("Menú Principal: \n 1. Graficar la malla \n 2. Graficar la Erdos Renyi \n 3. Graficar la Gilbert \n 4. Graficar la Geografico \n 5. Graficar la BarabasiAlbert \n 6. Graficar la Dorogovtsev Mendes \n 0. Salir \n"))
                        
class Main:
    me = Menu()
    
    opcion = int(input("Menú Principal: \n 1. Graficar la malla \n 2. Graficar la Erdos Renyi \n 3. Graficar la Gilbert \n 4. Graficar la Geografico \n 5. Graficar la BarabasiAlbert \n 6. Graficar la Dorogovtsev Mendes \n 0. Salir \n"))
    if opcion == 0:
        print('Gracias')
    me.opcionesMenu(opcion)
    
