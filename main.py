'''
Aluno: Marcelo Araújo dos Santos
Matrícula: 16/0035481
'''

from dijkstar import Graph, find_path
from consts import *
from seq_alig import get_correct
import tkinter as tk
import math

canvas_height=310
canvas_width=810
raio = 5
rowInterac = 3
cidades = {}
rodovias = {}

graph = Graph()

master = tk.Tk()
master.title('mapa')
master.geometry('1100x700')

w = tk.Canvas(master, width=canvas_width, height=canvas_height)

class Edge:
    def __init__(self, nome, x, y):
        self.nome = nome
        self.x = x
        self.y = y

'''
pesos:
    sp = situacaoPista (0 a 10), 10 não há como passar, 0 pista tá perfeita
    pp = precoPedagios
    tv = tempoDeViagem (distancia / velocidadeMax)
    p = perigo (0 a 10), 0 = sem perigo

vão de 0 a 5
'''

def create_circle(x, y, r, color, canvasName): #center coordinates, radius
    x0 = x - r
    y0 = y - r
    x1 = x + r
    y1 = y + r
    return canvasName.create_oval(x0, y0, x1, y1, fill=color)

def pintarMapa(cidades, rodovias, master, w, result=None):
    
    for r in rodovias:
        #print(r)
        c1, c2 = r.split(',')
        w.create_line(cidades[c1].x, cidades[c1].y, cidades[c2].x, cidades[c2].y )
        
    for c in cidades:
        create_circle(cidades[c].x, cidades[c].y, raio, "blue", w)
        w.create_text(cidades[c].x,cidades[c].y-10,fill="darkblue",
                        text=cidades[c].nome)
        #w.Label(master, text=cidades[c].nome, width=cidades[c].x, height=cidades[c].y+5)
    if result != None:
        length = len(result) 
        tam = 0
        for i in range(length-1): 
            c1, c2 = result[i], result[i+1]
            #==
            '''print(c1.nome)
            str = "{},{}".format(c1.nome, c2.nome)
            print(rodovias[str])'''

            '''p = x.replace('\n', '').split(', ')
            ei = cidades[p[START_CITY]]
            ef = cidades[p[END_CITY]]
            dist = math.sqrt( (ef.x-ei.x)**2 + (ef.y-ei.y)**2 )
            tempoDeViagem = dist / int(p[5])
            infoEdge = {
                'situacaoPista':int(p[2]),
                'precoPedagios':float(p[3]),
                'perigo':int(p[4]),
                'tempoDeViagem':tempoDeViagem
                }
            rodovias["{},{}".format(p[START_CITY], p[END_CITY])] = infoEdge'''

            w.create_line(cidades[c1].x, cidades[c1].y, cidades[c2].x, cidades[c2].y, fill="red")
    return 0

def get_weights():
    return {'sp': 3, 'pp': 3, 'tv': 3, 'p': 3}

def execButton(graph, cost_func, inicio, fim, textRes, cities):
    n_inicio = get_correct(inicio.get(), cities)
    n_fim = get_correct(fim.get(), cities)
    if(inicio.get() == "" or fim.get() == ""):
        textRes.config(text="preencha os dois campos de cidade inicio e fim")
    else:
        try:
            pesos = get_weights()
            cost_func = lambda u, v, e, prev_e: e['distancia']# + e['situacaoPista'] + e['precoPedagios']+ e['perigo'] + e['tempoDeViagem']
            print(n_inicio)
            
            path = find_path(graph,n_inicio, n_fim, cost_func=cost_func)
            #print("veja: ",path)
            caminho = path.nodes
            
            texto = "de '{}' ate '{}' o menor caminho eh {} com custo de {}km".format(caminho[0], caminho[-1], caminho, int(path.total_cost*100)/100)
            
            print(texto)
            textRes.config(text=texto)
            pintarMapa(cidades, rodovias, master, w, path.nodes)
        except:
            textRes.config(text="nao foi possivel achar caminho de '{}' ate '{}'".format(n_inicio, n_fim))


def calc_info_edge(edges):
    return -1

def main():
    w.grid(row=0,column=0)

    texti = tk.Label(master, text='inicio')
    texti.grid(row=1, column=0, sticky=tk.E)#, columnspan=1, rowspan=1) # 0, 0
    textf = tk.Label(master, text='fim')
    textf.grid(row=2, column=0, sticky=tk.E)#, columnspan=1, rowspan=2) # 0, 1

    textRes = tk.Label(master, text='----')
    textRes.grid(row=rowInterac, column=1)

    inicio = tk.Entry(master)
    inicio.grid(row=1, column=1, sticky=tk.W)#, columnspan=2, rowspan=1) # 1, 0
    fim = tk.Entry(master)
    fim.grid(row=2, column=1, sticky=tk.W)#, columnspan=2, rowspan=2) # 1, 1

    cost_func = -1
    

    fc = open("cidades.txt","r")
    fr = open("rodovias.txt","r")
    cities = []

    # lendo as cidades (nodes) e guardando
    fl =fc.readlines()
    for x in fl:
        c = x.replace('\n', '').split(', ')
        # print(c[CITY_NAME][1])
        cities.append(c[CITY_NAME])
        cidades[c[CITY_NAME]] = Edge(c[CITY_NAME], 2*int(c[COORD_X]), int(c[COORD_Y]))
    fc.close

    # lendo as rodovias (edges) e guardando no grafo
    fl =fr.readlines()
    for x in fl:
        p = x.replace('\n', '').split(', ')
        ei = cidades[p[START_CITY]]
        # print(p[END_CITY])
        ef = cidades[p[END_CITY]]
        dist = math.sqrt( (ef.x-ei.x)**2 + (ef.y-ei.y)**2 )
        tempoDeViagem = dist / int(p[VELOCITY])
        infoEdge = {
            'situacaoPista':int(p[CONDITION]),
            'precoPedagios':float(p[PRICE]),
            'perigo':int(p[DANGER]),
            'tempoDeViagem':tempoDeViagem,
            'distancia':dist
            }
        rodovias["{},{}".format(p[START_CITY], p[END_CITY])] = infoEdge
        

        graph.add_edge(p[START_CITY], p[END_CITY], infoEdge)
        graph.add_edge(p[END_CITY], p[START_CITY], infoEdge)
        
    
    button = tk.Button(master, text='calcular caminho', width=25,
         command=lambda: execButton(graph, cost_func, inicio, fim, textRes, cities))
    button.grid(row=rowInterac,column=0)
    
    fr.close()

    pesos = get_weights()
    

    #cost_func = lambda u, v, e, prev_e: e['distancia'] + e['situacaoPista'] + e['precoPedagios']+ e['perigo'] + e['tempoDeViagem']
    #path = find_path(graph, 'a', 'z', cost_func=cost_func)
    #print(path.nodes)
    
    pintarMapa(cidades, rodovias, master, w)
    master.mainloop() 


if __name__== "__main__":
  main()

