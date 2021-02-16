import numpy as np
import pygame
from utils import colors
import os
from classes.Player import Player
from classes.Bola import Bola
import sys
import time
import multiprocessing
import random
import copy
from print_nn import DrawNN

# Vamos importar a classe Ambiente lá da pasta do pacote
sys.path.append("/media/davi/dados/Projetos/Ensinando-Maquinas/pymenta/pymenta")
from environment import Environment as AmbienteClass

# Ajusta onde a janela inicial va aparecer
#os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (1690,0)
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0,0)
pygame.font.init() # you have to call this at the start, 
# Importa pygame.locals para acessar as teclas do teclado
from pygame.locals import (
	K_UP,
	K_DOWN,
	K_LEFT,
	K_RIGHT,
	K_w,
	K_s,
	K_o,
	K_l,
	K_ESCAPE,
	K_SPACE,
	KEYDOWN,
	QUIT,
	)

# globais
pygame.init()
SCREEN = 0
BG = 0
ROBO = 0
GAME_AREA = 0
METADATA = 0
METADATA_SPACE = 200

WIDTH = 1280
HEIGHT = 720

ARCHITECTURE = [2, 1]
NUM_INDIVIDUOS = 16
MUTATION_PROBABILITY = 10
NUM_PARTIDAS_POR_INDIVIDUO = 20

GAME_AREA_HEIGHT = HEIGHT - METADATA_SPACE

def iniciarTela():
	global SCREEN, BG, GAME_AREA, METADATA, ROBO
	SCREEN = pygame.display.set_mode([WIDTH, HEIGHT])#, pygame.FULLSCREEN)
	BG = pygame.image.load("images/background.jpeg")
	ROBO = pygame.image.load("images/robo.png")
	GAME_AREA = pygame.Surface((WIDTH, GAME_AREA_HEIGHT))
	GAME_AREA.blit(BG, (METADATA_SPACE, 0))
	GAME_AREA.blit(ROBO, (0, 0))
	#GAME_AREA.fill((0, 255, 0))
	#GAME_AREA.set_colorkey((0, 255, 0))	# Chroma Key, deleta todas as cores VERDES nesta camada

	SCREEN.blit(GAME_AREA, (0, METADATA_SPACE))


	#SCREEN.blit(BG, (METADATA_SPACE, 0))
	pygame.display.flip()

	# Menu superior dos pontos
	METADATA = pygame.Surface((WIDTH, METADATA_SPACE))
	METADATA.fill((255, 255, 255))
	SCREEN.blit(METADATA, (0,0))

def readKeys():

	# As teclas pressionadas são armazenadas em uma pilha no módulo Pygame
	for event in pygame.event.get():
		# O usuário clicou em fechar a janela? Enão para o looping.
		if event.type == QUIT:
			return False	

	keys = pygame.key.get_pressed()
	key_pressed = []

	if keys[pygame.K_q]:
		print("Botão de saída pressianado. Falô brow.")
		return False

	if keys[pygame.K_w]:
		key_pressed.append("W")

	if keys[pygame.K_s]:
		key_pressed.append("S")						

	if keys[pygame.K_o]:
		key_pressed.append("O")

	if keys[pygame.K_l]:
		key_pressed.append("L")						

	if keys[pygame.K_SPACE]:
		key_pressed.append("SPACE")		

	return key_pressed

def desenhaDisplaySuperior(player1, player2):
	global SCREEN
	# if you want to use this module.
	myfont = pygame.font.SysFont('Comic Sans MS', 100)
	textsurface = myfont.render(str(player1.score/100), False, (0, 0, 0))
	SCREEN.blit(textsurface, (300,20))

	textsurface = myfont.render(str(player2.score/100), False, (0, 0, 0))
	SCREEN.blit(textsurface, (900,20))	

def iniciarConjuntoPlayers(numIndividuos, lado, interface, drawNeuralNetwork = False):

	# Estamos trabalhando com interface gráfica?
	if interface == True:
		game_area_ = GAME_AREA
	else:
		game_area_ = False

	playerSet = []
	for i in range(numIndividuos):
		
		if lado == "direita":
			player = Player([WIDTH-150, 100], colors.BLACK, player_type, WIDTH, GAME_AREA_HEIGHT, ARCHITECTURE, game_area_, drawNeuralNetwork)
		elif lado == "esquerda":
			player = Player([150,100], colors.RED, "bot_ball_follow", WIDTH, GAME_AREA_HEIGHT, ARCHITECTURE, game_area_, drawNeuralNetwork)
		else:
			print("Qual lado você quer que o player fique? Corrija esta informação")
			exit()

		playerSet.append(player)
	return playerSet


def calcularScore(pontos, player1, player2):
	player1.score += pontos[0]*10
	player2.score += pontos[1]*10


def preparaPlayersParaSalvar(conjuntoPlayers1, conjuntoPlayers2):
	
	for i in range(len(conjuntoPlayers1)):
		conjuntoPlayers1[i].surface = False
		conjuntoPlayers2[i].surface = False

def prepararPlayersParaCarregar(conjuntoPlayers1, conjuntoPlayers2, drawNeuralNetwork):
	for i in range(len(conjuntoPlayers1)):
		conjuntoPlayers1[i].iniciaForma()
		conjuntoPlayers1[i].GAME_AREA = GAME_AREA
		conjuntoPlayers1[i].score = 0
		conjuntoPlayers1[i].drawNN = drawNeuralNetwork

		conjuntoPlayers2[i].iniciaForma()
		conjuntoPlayers2[i].GAME_AREA = GAME_AREA
		conjuntoPlayers2[i].score = 0
		conjuntoPlayers2[i].drawNN = drawNeuralNetwork



def salvaGeracao(currentGeneration, conjuntoPlayers1, conjuntoPlayers2):
	"""
		Para que eu possa dar um replay em um jogo salvo, preciso apenas das instâncias dos 
		jogadores da geração e da semente (seed) da bola no início da geração, para que ela 
		apareça nos lugares corretpos
	"""

	# O numpy não deixa savar objetos do tipo 'pygame.Surface' (que é o formato dos players), então simplesmente
	# vamos excluir as surfaces e depois, na hora de carregar novamente, reconstruimos as superfícies
	preparaPlayersParaSalvar(conjuntoPlayers1, conjuntoPlayers2)
	np.save("checkpoints/"+str(currentGeneration)+"_conjunto1.npy", np.asarray(conjuntoPlayers1))
	np.save("checkpoints/"+str(currentGeneration)+"_conjunto2.npy", np.asarray(conjuntoPlayers2))
	#np.save("checkpoints/"+str(currentGeneration)+"_seed", seed)

def carregarPlayers(geracao):
	conjuntoPlayers1 = np.load("checkpoints/"+str(geracao)+"_conjunto1.npy", allow_pickle=True)
	conjuntoPlayers2 = np.load("checkpoints/"+str(geracao)+"_conjunto2.npy", allow_pickle=True)
	#seed = np.load("checkpoints/"+str(geracao)+"_seed.npy", allow_pickle=True)
	#print(seed)
	return conjuntoPlayers1, conjuntoPlayers2 #, seed

def update(player1, player2, bola, pontos, keyPressed = -1):

	if keyPressed == False:
		print("Faloous")
		exit()

	# Faz o update da Bola
	ponto = bola.update(player1, player2)

	# Incrementa o placar
	if ponto >= 0:
		pontos[ponto] += 1

	# Faz o update dos players que não dependem dos comandos do usuário
	player1.update(bola) # O BOT do Player tem que ver a Bola (estímulo externo) para tomar uma ação
	player2.update(bola)	

	# Faz o update dos players, levando em consideração os comandos do usuário
	if keyPressed != -1:
		for key in keyPressed:	

			if key == "S":
				player1.movePlayerBaixo()
			if key == "W":
				player1.movePlayerCima()

			if key == "O":
				player2.movePlayerCima()
			if key == "L":
				player2.movePlayerBaixo()		


def draw(player1, player2, bola, pontos):
	player1.desenha()
	player2.desenha()

	bola.desenha()

	#desenhaDisplaySuperior(pontos)
	desenhaDisplaySuperior(player1, player2)

# A cada geração, temos que resetar o score
def resetaGeracao(conjuntoPlayers1, conjuntoPlayers2):

	for i in range(len(conjuntoPlayers1)):
		conjuntoPlayers1[i].score = 0
		conjuntoPlayers2[i].score = 0


manager = multiprocessing.Manager()
ship_ = manager.list()  # Shared Proxy to a list	
def MainLooping(args):
	player1 = args[0][0]
	player2 = args[0][1]
	bola = args[0][2] 
	individualNum = args[1]
	#ship_ = args[2]

	print("Iniciando a thread")
	print(individualNum)

	pontos = [0,0]

	clock = pygame.time.Clock()
	running = True
	# Isso vai semear todas as outras classes que usam o random()
	bolaSeed = time.time()
	player1.bolaSeed = bolaSeed
	player2.bolaSeed = bolaSeed
	random.seed(bolaSeed)
	bola.iniciaPosicaoAleatoria(0, True)
	while running:

		# UPDATE SHIPS EM PARALELO
		update(player1, player2, bola, pontos)

		if pontos[0] + pontos[1] == NUM_PARTIDAS_POR_INDIVIDUO:
			print(pontos)
			print("Acabou a melhor de "+str(NUM_PARTIDAS_POR_INDIVIDUO)+". Pontos:")
			print("Individuo num: " + str(individualNum))
			print("Score: " + str(player1.score))
			print("Score: " + str(player2.score))
			print("\n")
			ship_.append(copy.deepcopy([ [player1, player2], individualNum]))
			return

		clock.tick(10000000)


def mainParallel(interface, player_type, load, ind):
	global SCREEN, BG, GAME_AREA, MUTATION_PROBABILITY, ship_

	# Configurar os jogadores
	# Guardar as informações dos jogadores
	conjuntoPlayers1 = iniciarConjuntoPlayers(NUM_INDIVIDUOS, "esquerda", interface)
	conjuntoPlayers2 = iniciarConjuntoPlayers(NUM_INDIVIDUOS, "direita", interface)
	# Eu não posso passar um objecto 'pygame.Surface' para a função MainLooping, pq o módulo 
	# multiprocessing usa o picle para serializar os parâmetros. E o piclke não gosta do pygame
	preparaPlayersParaSalvar(conjuntoPlayers1, conjuntoPlayers2)

	contagem_individuo = 0
	player1 = conjuntoPlayers1[contagem_individuo]
	player2 = conjuntoPlayers2[contagem_individuo]

	# Inicia a bola do jogo
	bola = Bola([500,100], colors.PURPLE, time.time(), GAME_AREA, WIDTH, GAME_AREA_HEIGHT)	
	bola.surface = False # O pickle não gosta do Pygame. E o multiprocessing usa pickle para passar os parâmetros

	ambiente1 = AmbienteClass(NUM_INDIVIDUOS, conjuntoPlayers1, ARCHITECTURE, rank=5)#, selection="mutation_only")	
	ambiente2 = AmbienteClass(NUM_INDIVIDUOS, conjuntoPlayers2, ARCHITECTURE, rank=5)#, selection="mutation_only")

	running = True	
	geracao_atual = 0

	numThreads = 4
	while running:

		if interface == True:
			print("Treinamento com várias threads não pode ter interface")
			exit()

		# Here I have to generate a list so that each position is a arguments bag that each process will pick 
		argumentBag = []
		for currentIndividual in range(int(NUM_INDIVIDUOS/numThreads)):
			for i in range(numThreads):
				individualNum = i + currentIndividual*numThreads
				player1 = conjuntoPlayers1[individualNum]
				player2 = conjuntoPlayers2[individualNum]

				argumentBag.append([ [player1, player2, bola], individualNum])

		with multiprocessing.Pool(processes=numThreads) as pool:
			pool.map(MainLooping, argumentBag)
			pool.close()
			pool.join()					


		for i in range(NUM_INDIVIDUOS):
			conjuntoPlayers1[ship_[i][1]] = copy.deepcopy(ship_[i][0][0])
			conjuntoPlayers2[ship_[i][1]] = copy.deepcopy(ship_[i][0][1])

		ship_[:] = [] 
		print("REPLICATING..")	
		salvaGeracao(geracao_atual, conjuntoPlayers1, conjuntoPlayers2)

		ambiente1.replicate(MUTATION_PROBABILITY)
		ambiente2.replicate(MUTATION_PROBABILITY)

		MUTATION_PROBABILITY -= MUTATION_PROBABILITY*0.02
		print("Nova MUTATION_PROBABILITY: " + str(MUTATION_PROBABILITY))

		resetaGeracao(conjuntoPlayers1, conjuntoPlayers2)
		contagem_individuo = 0
		geracao_atual += 1



# Essa é a primeira função a ser chamada no código
def main(interface, player_type, load, ind):
	global SCREEN, MUTATION_PROBABILITY, ROBO

	# Configurar a tela no qual o jogo será exedcutado
	drawNeuralNetwork = False
	if interface == True:
		iniciarTela()
		drawNeuralNetwork = DrawNN(ARCHITECTURE, SCREEN)

	# Inicia a bola do jogo
	bolaSeed = time.time()
	bola = Bola([500,100], colors.PURPLE, bolaSeed, GAME_AREA, WIDTH, GAME_AREA_HEIGHT)	

	if load > -1:# and ind >= 0:
		#conjuntoPlayers1, conjuntoPlayers2, bolaSeed = carregarPlayers(load)
		conjuntoPlayers1, conjuntoPlayers2 = carregarPlayers(load)
		# Ao carregarmos a bola, temos que definir a mesma seed do momento do treinamento
		prepararPlayersParaCarregar(conjuntoPlayers1, conjuntoPlayers2, drawNeuralNetwork)

		contagem_individuo = ind
		player1 = conjuntoPlayers1[contagem_individuo]
		player2 = conjuntoPlayers2[contagem_individuo]

		#bola.setSeed(player1.bolaSeed)
		#bola.iniciaPosicaoAleatoria(0, True)
		random.seed(player1.bolaSeed)
		bola.iniciaPosicaoAleatoria(0, True)
	else:
		# Configurar os jogadores
		# Guardar as informações dos jogadores
		conjuntoPlayers1 = iniciarConjuntoPlayers(NUM_INDIVIDUOS, "esquerda", interface, drawNeuralNetwork)
		conjuntoPlayers2 = iniciarConjuntoPlayers(NUM_INDIVIDUOS, "direita", interface, drawNeuralNetwork)

		contagem_individuo = 0
		player1 = conjuntoPlayers1[contagem_individuo]
		player2 = conjuntoPlayers2[contagem_individuo]

		player1.bolaSeed = bolaSeed
		player2.bolaSeed = bolaSeed


	pontos = [0,0]

	# Iniciando o ambiente que será responsável por evoluir os players (tipo pokemón)
	ambiente1 = AmbienteClass(NUM_INDIVIDUOS, conjuntoPlayers1, ARCHITECTURE, selection="mutation_only")	
	ambiente2 = AmbienteClass(NUM_INDIVIDUOS, conjuntoPlayers2, ARCHITECTURE, selection="mutation_only")		

	# O jogo estará em um looping infinito. A cada iteração do looping, um quadro é processado e exibido
	# na tela. Se quisermos sair do jogo, basta mudarmos a variável "running" para false	
	running = True	
	geracao_atual = 0
	while running:

		if interface == True:
			GAME_AREA.blit(BG, (0, 0))
			SCREEN.blit(ROBO, (350, 85))

		keyPressed = readKeys()	# Verifica se o usuário pressionou alguma tecla
		if keyPressed == False:
			running = False		

		update(player1, player2, bola, pontos, keyPressed)	# Primeiro, atualiza a posição de tudo no jogo
		#SCREEN.blit(BG, (0, 0))
		if interface == True:
			draw(player1, player2, bola, pontos)					# Só depois vamos desenhar os objetos na tela
		
		# Um indivíduo jogará contra outro indivíduo por 10 partidas. Depois disso, trocaremos de indivíduo
		if pontos[0] + pontos[1] == NUM_PARTIDAS_POR_INDIVIDUO:
			print("Acabou a melhor de "+str(NUM_PARTIDAS_POR_INDIVIDUO)+". Pontos:")

			"""
			print("score 1")
			print(player1.score)
			print("score 2")
			print(player2.score)
			"""
			

			# Se estivermos dando um replay em algum indivíduo, vamos parar aqui
			if load > -1:# and ind >= 0:
				print("score 1")
				print(player1.score)
				print("score 2")
				print(player2.score)
				exit()
			# Calcula o score dos indivíduos
			#calcularScore(pontos, player1, player2)

			# Zera os pontos para a nova partida
			pontos[0] = 0
			pontos[1] = 0

			# Cria uma nova geração de indivíduos. Eles são armazenados nas listas conjuntoPlayers1 e conjuntoPlayers1 por referência
			if contagem_individuo == NUM_INDIVIDUOS-1:
				salvaGeracao(geracao_atual, conjuntoPlayers1, conjuntoPlayers2)

				ambiente1.replicate(MUTATION_PROBABILITY)
				ambiente2.replicate(MUTATION_PROBABILITY)

				MUTATION_PROBABILITY -= MUTATION_PROBABILITY*0.02

				resetaGeracao(conjuntoPlayers1, conjuntoPlayers2)
				contagem_individuo = 0
				geracao_atual += 1

				bolaSeed = time.time()
				bola.setSeed(bolaSeed)
				bola.iniciaPosicaoAleatoria(0, True)			

				player1 = conjuntoPlayers1[contagem_individuo]
				player2 = conjuntoPlayers2[contagem_individuo]

				# Salva a seed da bola para que possamos dar o replay em um indivíduo específico depois
				player1.bolaSeed = bolaSeed
				player2.bolaSeed = bolaSeed

				continue

			# O simples incremento da 'contagem_individuo' garante que os próximos indivíduos comecem a jogar
			contagem_individuo += 1

			bolaSeed = time.time()
			bola.setSeed(bolaSeed)
			bola.iniciaPosicaoAleatoria(0, True)			

			player1 = conjuntoPlayers1[contagem_individuo]
			player2 = conjuntoPlayers2[contagem_individuo]

			# Salva a seed da bola para que possamos dar o replay em um indivíduo específico depois
			player1.bolaSeed = bolaSeed
			player2.bolaSeed = bolaSeed

		if interface == True:
			SCREEN.blit(GAME_AREA, (0,METADATA_SPACE))
			GAME_AREA.fill((255, 255, 255))
			#SCREEN.blit(METADATA, (0,0))
			pygame.display.update()

			METADATA.fill((242, 251, 255))
			SCREEN.blit(METADATA, (0,0))		
	pygame.quit()

# A primeira coisa que vai ser executada é isso aqui
if __name__ == "__main__":

	#interface = False
	interface = True
	load = 4
	ind = 41

	#if load > -1 and interface == False:
	#	print("Só é possível carregar uma geração se a interface estiver ligada")
	#	exit()

	#player_type = "humano"						# O jogador 2 é controlado pelas teclas "o" e "l"
	#player_type = "bot_ball_follow"			# O jogador 2 é um bot que segue a bola no eixo y
	player_type = "artificial_neural_network"	# O jogador 2 é uma rede neural artificial
	try:
		
		main(interface, player_type, load, ind)
		#mainParallel(interface, player_type, load, ind)
	except KeyboardInterrupt:
		print("\n\n")
		print("Falo brother")
