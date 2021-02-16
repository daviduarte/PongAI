import numpy as np
from utils import colors
import pygame
import time
import math
import random

class Bola:
	def __init__(self, posicao, cor, seed, GAME_AREA, GAME_WIDTH, GAME_HEIGHT):
		self.GAME_AREA = GAME_AREA
		self.dimSurface = [40, 40]  # A bola é desenhada em uma superfíce de 50x50
		self.raio = 20				# Raio da bola
		self.vetorVelocidade = False
		self.velocidade = 4
		self.surface = False		# A superfície no qual o desenho da bola será armazenada
		self.posicao = posicao
		self.cor = cor

		self.GAME_WIDTH = GAME_WIDTH
		self.GAME_HEIGHT = GAME_HEIGHT			

		self.seed = seed
		self.setSeed(self.seed)

		self.iniciaForma()
		self.iniciaPosicaoAleatoria(0, True)

	def setSeed(self, seed):
		random.seed(seed)

	def iniciaForma(self):

		self.surface = pygame.Surface((self.dimSurface[0], self.dimSurface[1]))
		self.surface.fill((0,255,0))
		self.surface.set_colorkey((0,255,0)) # Like a Chroma Key, but instead green, is black 	
		
		centroSuperficieX = int(self.dimSurface[0]/2)
		centroSuperficieY = int(self.dimSurface[1]/2)

		pygame.draw.circle(self.surface, self.cor, [centroSuperficieX, centroSuperficieY], self.raio) # Desenha o círculo que vai ser a bola, armazena este desenho em self.surface para possamos usá-lo qunando quisermos


	"""
		Inicia um vetorVelocidade aleatório
		@param lado 0 se a bola pode ir para qualquer lado, 1 se a bola pode ir para a esquerda e 2 se a bola pode ir para a direita
	"""
	def iniciaPosicaoAleatoria(self, lado, novaPosicao = True):

		# Para evitar que a bola fique muito tempo percorrendo a tela, limita as suas possíveis 
		# trajetórias para as faixas angulares:
		# 0° -> 45°
		# 135° -> 225°
		# 220° -> 360°

		if novaPosicao == True:
			self.posicao = [600, 400]

		if lado == 0:
			anguloBola = random.choice([random.randrange(45), random.randrange(90)+135, random.randrange(45)+315])
		elif lado == 1:
			anguloBola = random.randrange(90)+135
		elif lado == 2:
			anguloBola = random.choice([random.randrange(45), random.randrange(45)+315])

		anguloBola += 1	# Evita que ângulo seja 0

		#anguloBola = random.randrange(angulo)
		self.vetorVelocidade = [math.cos(math.radians(anguloBola))*self.velocidade, math.sin(math.radians(anguloBola))*self.velocidade]

	def refleteVetor(self, vetorIncidente, normalEspelho):
		vetorIncidente = np.asarray(vetorIncidente)
		normalEspelho = np.asarray(normalEspelho)

		return vetorIncidente - (2 * vetorIncidente * normalEspelho * normalEspelho ) / np.linalg.norm(normalEspelho)

	def verificaColisaoParedes(self):

		# Verificar colisão com as bordas do jogo
		# Calcula a distância entre as bordas do jogo
		distCima = self.posicao[1] # - 0
		distEsquerda = self.posicao[0] # - 0
		distBaxo = self.GAME_HEIGHT - (self.posicao[1] + self.dimSurface[1])
		distDireita = self.GAME_WIDTH - (self.posicao[0] + self.dimSurface[0])

		if distCima <= 0:
			self.posicao[1] = 0
			# Calcula o vetor normal da borda da tela
			normalTelaBaixo = [0, 1]
			# Chama os cálculos de reflexão de vetor
			novaVelocidade = self.refleteVetor(self.vetorVelocidade, normalTelaBaixo)
			# Substitui o vetor velocidade pelo novo vetor velocidade refletido
			self.vetorVelocidade = novaVelocidade

		if distEsquerda <= 0:

			# Calcula o vetor normal da borda da tela
			normalTelaBaixo = [-1, 0]
			# Chama os cálculos de reflexão de vetor
			novaVelocidade = self.refleteVetor(self.vetorVelocidade, normalTelaBaixo)
			# Substitui o vetor velocidade pelo novo vetor velocidade refletido
			self.vetorVelocidade = novaVelocidade

		if distBaxo <= 0:

			self.posicao[1] = self.GAME_HEIGHT - self.dimSurface[1]
			# Calcula o vetor normal da borda da tela
			normalTelaBaixo = [0, -1]
			# Chama os cálculos de reflexão de vetor
			novaVelocidade = self.refleteVetor(self.vetorVelocidade, normalTelaBaixo)
			# Substitui o vetor velocidade pelo novo vetor velocidade refletido
			self.vetorVelocidade = novaVelocidade

			
		if distDireita <= 0:
			# Calcula o vetor normal da borda da tela
			normalTelaBaixo = [1, 0]
			# Chama os cálculos de reflexão de vetor
			novaVelocidade = self.refleteVetor(self.vetorVelocidade, normalTelaBaixo)
			# Substitui o vetor velocidade pelo novo vetor velocidade refletido
			self.vetorVelocidade = novaVelocidade	



		# Refletir o movimento

	def verificaColisaoPlayers(self, player1, player2):
		"""
		 Verifica se a bola enconsta no Player. Lembre-se que o formato do player é um retângulo (veja a função iniciaForma() ).
		 Portanto, devemos calcular as coordenadas atuais da "parede da frente do retângulo" do player, e verificar se a bola encosta nela
		"""

		# Verifica se a bola encostou no Player 1
		# Calcula a distância entre o Player1 e a bola
		P1 = player1.position[0] + player1.dimSurface[0]	
		dist_x = self.posicao[0] - P1
		normal_player1 = [1,0]

		if dist_x <= 0 and abs(dist_x) < player1.dimSurface[0]:
			# Verifico se a posição Y da bola está entre os 2 extremos do player 1
			if self.posicao[1]+(self.dimSurface[1]/2) <= player1.position[1]+player1.dimSurface[1]+15 and self.posicao[1]+(self.dimSurface[1]/2) >= player1.position[1]-15:

				self.vetorVelocidade = self.refleteVetor(self.vetorVelocidade, normal_player1)
				self.iniciaPosicaoAleatoria(2, False)		
				player1.score += 10000
		# Verifica se a bola encostou no Player 2
		# Calcula a distância entre o Player2 e a bola
		P2 = player2.position[0]
		dist_x = P2 - (self.posicao[0] + self.dimSurface[0])
		normal_player2 = [-1,0]				
		if dist_x <= 0 and abs(dist_x) < player2.dimSurface[0]:
			# Verifico se a posição Y da bola está entre os 2 extremos do player 1
			if self.posicao[1]+(self.dimSurface[1]/2) <= player2.position[1]+player2.dimSurface[1]+15 and self.posicao[1]+(self.dimSurface[1]/2) >= player2.position[1]-15:

				self.vetorVelocidade = self.refleteVetor(self.vetorVelocidade, normal_player2)	
				self.iniciaPosicaoAleatoria(1, False)		
				player2.score += 10000


	"""
		Se algum player deixar a bola passar, ela some, volta para o centro da tela com um vetor velocidade
		aleatório, e um ponto é atribuído para o outro player
	"""
	def verificaGol(self, player1, player2):
		# Verifica se o Player 2 fez um gol contra o Player 1
		if self.posicao[0] < player1.position[0] + player1.dimSurface[0] - 100: # Adiciona uma margem de segurança
			self.posicao = [player1.position[0]+100,500]	# Inicia a bola perto do player 1 com direção ao player 2
			self.iniciaPosicaoAleatoria(2, False)
			#player2.score += 10
			return 1

		# Verifica se o Player 1 fez um gol contra o Player 2
		if self.posicao[0]+self.dimSurface[0] > player2.position[0] + 100:	# Add uma margem de segurança
			self.posicao = [player2.position[0]-100,500]
			self.iniciaPosicaoAleatoria(1, False)
			#player1.score += 10
			return 0			
		return -1


	def update(self, player1, player2):
		self.posicao[0] += self.vetorVelocidade[0]
		self.posicao[1] += self.vetorVelocidade[1]

		self.verificaColisaoParedes()
		self.verificaColisaoPlayers(player1, player2)
		
		# Verica se alguém pontuou
		ponto = self.verificaGol(player1, player2)
		return ponto

	def desenha(self):
		self.GAME_AREA.blit(self.surface, self.posicao)

