# -*- coding: utf-8 -*-
import random
from operator import itemgetter

def menu_escalonadores():
	menu = '''+------------------------------------------------------------------+
| 1 - FCFS | 2 - SJF | 3 - SRTF | 4 - Round Robin | 5 - Multinível |
+------------------------------------------------------------------+'''

	print(menu)

	texto_menu = ["FCFS", "SJF", "SRTF", "Round Robin", "Multinível"]
	escolhido = 0
	while escolhido < 1 or escolhido > 5:
		escolhido = int(input("Escolha um escalonador: "))
	
	return [escolhido, texto_menu[escolhido - 1]]


#Retorna o menu de opções para gerar os processos
def menu_opcoes():
	menu = '''\n+------------------------------------------------------+
| 1 - Manual | 2 - Automático | 3 - Iguais a (escolha) |
+------------------------------------------------------+'''
	return menu



def gerar_tabela(lista_dados, espera_media, turnaround_medio): #lista_dados = [Número processo, chegada, burst, saida, espera, turnaround]
	print('''\n\n+----------------------------------------------------------------------------------------------------------+
| 1 - Nº do processo | 2 - Tempo de chegada | 3 - Burst | 4 - Tempo de saída | 5 - Espera | 6 - Turnaround |
+----------------------------------------------------------------------------------------------------------+''')
	ordem = int(input("Escolha ordenação da tabela a ser exibida: "))

	if ordem == 1:
		lista_dados = sorted(lista_dados, key=itemgetter(0, 1, 2)) #nº processo, chegada, burst
	elif ordem == 2:
		lista_dados = sorted(lista_dados, key=itemgetter(1, 2, 0)) #Chegada, burst, nº processo
	elif ordem == 3:
		lista_dados = sorted(lista_dados, key=itemgetter(2, 0, 1)) #Burst, nº processo, chegada
	elif ordem == 4:
		lista_dados = sorted(lista_dados, key=itemgetter(3)) #Saída
	elif ordem == 5:
		lista_dados = sorted(lista_dados, key=itemgetter(4, 0, 1, 2)) #Espera, nº processo, chegada, burst
	elif ordem == 6:
		lista_dados = sorted(lista_dados, key=itemgetter(5, 0, 1, 2)) #Turnaround, nº processo, chegada, burst
	
	tabela = ""
	for dados in lista_dados:
		tabela += "\n| %s | %s | %s | %s | %s | %s |" %("P%s" %(str(dados[0]).ljust(8)), str(dados[1]).ljust(7), str(dados[2]).ljust(5), str(dados[3]).ljust(5), str(dados[4]).ljust(6), str(dados[5]).ljust(10))

	tabela += "\n+-----------+---------+-------+-------+--------+------------+"
	tabela += "\n| Espera média: %s | Turnaround médio: %s |" %(str(espera_media).ljust(5), str(turnaround_medio).ljust(17))
	return tabela


def rodar_fila_horario(fila_circular):
	if len(fila_circular) <= 1:
		return fila_circular

	tamanho = len(fila_circular)
	aux = fila_circular[0]
	for i in range(tamanho):
		fila_circular[i] = fila_circular[(i + 1) % tamanho]

	fila_circular[-1] = aux
	return fila_circular

def rodar_fila_anti_horario(fila_circular):
	if len(fila_circular) <= 1:
		return fila_circular

	tamanho = len(fila_circular)
	
	for quant in range(tamanho-1):
		aux = fila_circular[0]
		for i in range(tamanho):
			fila_circular[i] = fila_circular[(i + 1) % tamanho]

		fila_circular[-1] = aux

	return fila_circular


def fcfs(lista_chegada, lista_burst): #First-Come, First-Served
	numero_proc = [(i + 1) for i in range(len(lista_chegada))] #Gera numero dos processos

	processos = zip(numero_proc, lista_chegada, lista_burst) #(Número do processo, Tempo de Chegada, Tempo de Burst)
	processos = sorted(processos, key=itemgetter(1, 0)) #Ordenação por (Tempo de Chegada, Número do processo)

	tempo_cpu = min(lista_chegada) #tempo cpu inicial deve ser igual o menor valor de chegada
	tempo_espera = 0
	turnaround_medio = 0
	espera_media = 0
	dados = []

	for processo in processos:
		chegada = processo[1]
		burst = processo[2]
		tempo_espera = tempo_cpu - chegada
		if tempo_espera < 0:
			tempo_espera = 0
		espera_media += tempo_espera
		turnaround = tempo_espera + burst
		turnaround_medio += turnaround

		if chegada > tempo_cpu:
			tempo_cpu += chegada - tempo_cpu

		tempo_cpu += burst
		
		dados.append([processo[0], chegada, burst, tempo_cpu, tempo_espera, turnaround])  
	
	espera_media /= len(processos)
	turnaround_medio /= len(processos)

	return gerar_tabela(dados, espera_media, turnaround_medio)



def sjf(lista_chegada, lista_burst): #Shortest Job First
	numero_proc = [(i + 1) for i in range(len(lista_chegada))] #Gera numero dos processos

	processos = zip(numero_proc, lista_chegada, lista_burst) #(Número do processo, Tempo de Chegada, Tempo de Burst)
	processos = sorted(processos, key=itemgetter(1, 2, 0)) #Ordenação por (Tempo de Chegada, Tempo de Burst, Número do processo)

	tempo_cpu = min(lista_chegada) #tempo cpu inicial deve ser igual o menor valor de chegada
	tempo_espera = 0
	turnaround_medio = 0
	espera_media = 0
	dados = []

	for processo in processos:
		chegada = processo[1]
		burst = processo[2]
		tempo_espera = tempo_cpu - chegada
		if tempo_espera < 0:
			tempo_espera = 0
		espera_media += tempo_espera
		turnaround = tempo_espera + burst
		turnaround_medio += turnaround

		if chegada > tempo_cpu:
			tempo_cpu += chegada - tempo_cpu

		tempo_cpu += burst
		
		dados.append([processo[0], chegada, burst, tempo_cpu, tempo_espera, turnaround])  
	

	espera_media /= len(processos)
	turnaround_medio /= len(processos)

	return gerar_tabela(dados, espera_media, turnaround_medio)



def fila_por_cpu(processos, tempo_cpu):
	fila_circular = []
	execucao = None

	for processo in processos: #Estrutura processo - (Número do processo, Tempo de Chegada, Tempo de Burst)
		if processo[1] <= tempo_cpu:
			fila_circular.append(processo) #Monta lista com processos que chegaram até o tempo atual
			if not execucao:
				execucao = processo
			if execucao and processo[2] < execucao[2]:
				fila_circular = sorted(processos, key=itemgetter(2, 1, 0)) #Ordenação por (Tempo de Burst, Tempo de Chegada, Número do processo)
				execucao = processo

	return fila_circular # Retorna uma lista com os processos



def srtf(lista_chegada, lista_burst): #Shortest Remaining Time First
	numero_proc = [(i + 1) for i in range(len(lista_chegada))] #Gera numero dos processos
	processos = zip(numero_proc, lista_chegada, lista_burst) #(Número do processo, Tempo de Chegada, Tempo de Burst)
	processos = sorted(processos, key=itemgetter(1, 2, 0)) #Ordenação por (Tempo de Chegada, Tempo de Burst, Número do processo)
	
	dict_processos = {processo[0] : {"Chegada" : processo[1], "Burst" : processo[2], "BurstAtual" : processo[2], "Espera" : 0 } for processo in processos}  #Chave = Nome : Valor = [chegada, burst, burst atual, tempo espera]

	tempo_cpu = min(lista_chegada) #tempo cpu inicial deve ser igual o menor valor de chegada
	turnaround_medio = 0
	espera_media = 0
	dados = []

	lista_processos = [(p, dict_processos[p]["Chegada"], dict_processos[p]["BurstAtual"]) for p in dict_processos]
	processos = fila_por_cpu(lista_processos, tempo_cpu) #Monta a fila de processos que chegaram no tempo atual da CPU e ordena por burst

	while dict_processos:
		tempo_cpu += 1

		if processos:
			execucao = processos[0][0]
			dict_processos[execucao]["BurstAtual"] -= 1

			for processo in processos:
				nome = processo[0]
				if nome != execucao:
					dict_processos[nome]["Espera"] += 1 

			if dict_processos[execucao]["BurstAtual"] == 0:
				chegada = dict_processos[execucao]["Chegada"]
				burst = dict_processos[execucao]["Burst"]
				tempo_espera = dict_processos[execucao]["Espera"]

				espera_media += tempo_espera
				turnaround = tempo_espera + burst
				turnaround_medio += turnaround

				processos = rodar_fila_horario(processos)
				processos.pop()

				dados.append([execucao, chegada, burst, tempo_cpu, tempo_espera, turnaround])  
	
				del dict_processos[execucao]


		lista_processos = [(p, dict_processos[p]["Chegada"], dict_processos[p]["BurstAtual"]) for p in dict_processos]
		processos = fila_por_cpu(lista_processos, tempo_cpu)

	espera_media /= len(numero_proc)
	turnaround_medio /= len(numero_proc)

	return gerar_tabela(dados, espera_media, turnaround_medio)




def fila_por_prioridade(processos, tempo_cpu):
	fila_circular = []

	#processo = [número do processo, tempo de chegada, prioridade]
	for processo in processos:
		if processo[1] <= tempo_cpu:
			fila_circular.append(processo)
		if processo[1] == tempo_cpu and processo[2] < fila_circular[0][2]:
			fila_circular = rodar_fila_anti_horario(fila_circular)

	return fila_circular # Retorna uma lista com os processos


def rr(lista_chegada, lista_burst): #Round Robin
	lista_prioridade = gerar_prioridade(len(lista_chegada))

	quantum = int(input("\nTempo do Quantum: "))

	numero_proc = [(i + 1) for i in range(len(lista_chegada))] #Gera numero dos processos
	processos = zip(numero_proc, lista_chegada, lista_burst, lista_prioridade) #(Número do processo, Tempo de Chegada, Tempo de Burst)
	processos = sorted(processos, key=itemgetter(1, 3, 2, 0)) #Ordenação por (Tempo de Chegada, Prioridade, Tempo de Burst, Número do processo)

	#Chave = Nome : Valor = [chegada, burst, burst atual, tempo espera, prioridade]
	dict_processos = {processo[0] : {"Chegada" : processo[1], "Burst" : processo[2], "BurstAtual" : processo[2], "Espera" : 0, "Prioridade" : processo[3], } for processo in processos}

	tempo_cpu = min(lista_chegada) #tempo cpu inicial deve ser igual o menor valor de chegada
	turnaround_medio = 0
	espera_media = 0
	dados = []
	rodar = False
	ultimo_tempo_rodar = 0 #tempo para identificar quando a fila deve "rodar"


	lista_processos = [(p, dict_processos[p]["Chegada"], dict_processos[p]["Prioridade"]) for p in dict_processos]
	lista_processos = sorted(lista_processos, key=itemgetter(2, 1, 0)) #Ordenação por  (Prioridade, Tempo de chegada e número processo)
	processos = fila_por_prioridade(lista_processos, tempo_cpu) #Monta a fila de processos que chegaram no tempo atual da CPU e ordena por burst


	while dict_processos:
		tempo_cpu += 1
		
		if ultimo_tempo_rodar + quantum == tempo_cpu:
			rodar = True

		if processos:
			execucao = processos[0][0]
			dict_processos[execucao]["BurstAtual"] -= 1
			
			for processo in processos:
				nome = processo[0]
				if nome != execucao and processo[1] < tempo_cpu:
					dict_processos[nome]["Espera"] += 1 

			if dict_processos[execucao]["BurstAtual"] == 0:
				chegada = dict_processos[execucao]["Chegada"]
				burst = dict_processos[execucao]["Burst"]
				tempo_espera = dict_processos[execucao]["Espera"]

				espera_media += tempo_espera
				turnaround = tempo_espera + burst
				turnaround_medio += turnaround

				dados.append([execucao, chegada, burst, tempo_cpu, tempo_espera, turnaround])
				del dict_processos[execucao]

				processos = rodar_fila_horario(processos)
				processos.pop()
				rodar = False
				ultimo_tempo_rodar = tempo_cpu
			
			elif rodar:
				processos = rodar_fila_horario(processos)
				rodar = False
				ultimo_tempo_rodar = tempo_cpu #Guarda o tempo da última vez que a fila andou


		for p in dict_processos:
			if dict_processos[p]["Chegada"] == tempo_cpu:
				processos.append((p, dict_processos[p]["Chegada"], dict_processos[p]["Prioridade"]))

		processos = fila_por_prioridade(processos, tempo_cpu)

	espera_media /= len(numero_proc)
	turnaround_medio /= len(numero_proc)


	return gerar_tabela(dados, espera_media, turnaround_medio)



def multinivel(lista_chegada, lista_burst):
	return "multinivel"



def gerar_tc(qtd_proc):
	escolhido = 0

	while(escolhido < 1 or escolhido > 3):
		print(menu_opcoes())
		escolhido = int(input("Escolha como deseja gerar o tempo de CHEGADA: "))

	if escolhido == 1:
		lista_chegada = [int(input("Tempo chegada P%d: " %(i + 1))) for i in range(qtd_proc)]
	elif escolhido == 2:
		lista_chegada = [random.randint(0, 30) for i in range(qtd_proc)]
	else:
		num = int(input("Tempo de chegada: "))
		lista_chegada = [num for i in range(qtd_proc)]

	return lista_chegada


def gerar_burst(qtd_proc):
	escolhido = 0

	while(escolhido < 1 or escolhido > 3):
		print(menu_opcoes())
		escolhido = int(input("Escolha como deseja gerar o BURST: "))

	if escolhido == 1:
		lista_burst = [int(input("Burst P%d: " %(i + 1))) for i in range(qtd_proc)]
	elif escolhido == 2:
		lista_burst = [random.randint(1, 20) for i in range(qtd_proc)]
	else:
		num = int(input("Tamanho do burst: "))
		lista_burst = [num for i in range(qtd_proc)]

	return lista_burst


#Gerar prioridade caso seja RR
def gerar_prioridade(qtd_proc):
	escolhido = 0

	while(escolhido < 1 or escolhido > 3):
		print(menu_opcoes())
		escolhido = int(input("Escolha como deseja gerar a PRIORIDADE: "))

	if escolhido == 1:
		lista_prioridade = [int(input("Prioridade P%d: " %(i + 1))) for i in range(qtd_proc)]
	elif escolhido == 2:
		lista_prioridade = [random.randint(1, 20) for i in range(qtd_proc)]
	else:
		num = int(input("Prioridade: "))
		lista_prioridade = [num for i in range(qtd_proc)]

	return lista_prioridade



#Programa principal
def run():
	funcoes = [fcfs, sjf, srtf, rr, multinivel] #Declaração para chamada das funções
	escolhido = menu_escalonadores()
	funcao = funcoes[escolhido[0] - 1] #Recebe a função escolhida no menu
	qtd_proc = int(input("Número de processos: "))
	lista_chegada = gerar_tc(qtd_proc)
	lista_burst = gerar_burst(qtd_proc)

	tabela = "\n+-----------------------------------------------------------+"
	tabela += "\n| %s %s" %(escolhido[1].rjust(31), "|".rjust(27))
	tabela += "\n+-----------+---------+-------+-------+--------+------------+"
	tabela += "\n| Processos | Chegada | Burst | Saída | Espera | Turnaround |"
	tabela += "\n+-----------+---------+-------+-------+--------+------------+"
	tabela += funcao(lista_chegada, lista_burst)
	tabela += "\n+---------------------+-------------------------------------+"

	print(tabela)

	print("Tempos de chegada: %s" %lista_chegada)
	print("Burst: %s" %lista_burst)


run()
