import numpy as np
from utils import colors
import pygame
import random
import time
import math

class Player:
	def __init__(self, position, color, player_type, GAME_WIDTH, GAME_HEIGHT, architecture, GAME_AREA = False, drawNN = False):
		self.position = position
		self.shape = []
		self.dimSurface = [25, 150] # O player é desenhado em uma superfície de 25x100px
		self.surface = False		# A superfície no qual o desenho da bola será armazenada
		self.playerColor = color
		self.GAME_AREA = GAME_AREA
		self.GAME_WIDTH = GAME_WIDTH
		self.GAME_HEIGHT = GAME_HEIGHT		
		self.velocidade = 2

		self.score = 0

		self.drawNN = False
		if drawNN is not False:
			self.drawNN = drawNN		

		self.architecture = architecture
		self.INPUT_NEURON = 2
		self.HIDDEN_NEURON1 = 6
		self.OUTPUT_NEURON = 2

		self.player_type = player_type
		self.iniciaForma()

		self.brain = []
		self.bolaSeed = 0		# Preciso armazenar a seed da bola aqui para que eu possa carregar um indivíduo sem ter que carregar todos os outros anteriores
		self.seed = time.time()
		random.seed(self.seed)
		self.redeNeural()

	def iniciaForma(self):

		self.shape = [(0, 0), (25, 0), (25, 150), (0, 150)]	# Desenho do player dentro da superfície de tamanho especificada em self.dimSurface
		#self.surface = pygame.Surface((self.dimSurface, self.dimSurface), pygame.SRCALPHA)
		self.surface = pygame.Surface((self.dimSurface[0], self.dimSurface[1]))
		self.surface.fill((0,255,0))
		self.surface.set_colorkey((0,255,0)) # Like a Chroma Key, but instead green, is black 

		pygame.draw.polygon(self.surface, self.playerColor, self.shape)

	def desenha(self):
		self.drawNN.draw()
		self.GAME_AREA.blit(self.surface, [self.position[0], self.position[1]])

	def movePlayerBaixo(self):

		if self.position[1] + self.dimSurface[1] < self.GAME_HEIGHT:
			self.position[1] += self.velocidade
			self.score += 1

	def movePlayerCima(self):

		if self.position[1] > 0:
			self.position[1] -= self.velocidade
			self.score += 1
	
	def inicializarRedeNeural(self):
		"""
			Entre 2 layers há uma matriz de pesos. Esta função constói esta matriz de pesos
		"""
		l = []
		camadas = []
		bias = []
		#print(self.architecture)
		for i in range(len(self.architecture)-1):
			qtd_neuronios_camada_anterior = self.architecture[i]
			qtd_neuronios_camada_posterior = self.architecture[i+1]

			# Init layer l1
			for i in range(qtd_neuronios_camada_anterior):
			#for (i = 0 ; i < input_neuron ; i++){
				l.append([])
				for j in range(qtd_neuronios_camada_posterior):
				#for (j = 0 ; j < hidden_neuron ; j++){
					l[i].append(random.uniform(-1,1))

			b = random.uniform(-1,1)

			camadas.append(l)
			bias.append(b)

			l = []

		#print(camadas)
		#print(bias)
		#exit()
		return [camadas, bias]
		
	def redeNeural(self):

		# Initialize brains with random values
		#for i in range(individuals):
		#for (var i = 0 ; i < individuals ; i++){
		l1 = []
		l2 = []

		camadas, bias = self.inicializarRedeNeural()
		#self.initialize_neural_network(l1, l2)

		#b1 = random.uniform(-1,1)
		#b2 = random.uniform(-1,1)

		self.brain = []
		self.brain.extend(camadas)
		self.brain.extend(bias)

		#self.brain.append(l1)
		#self.brain.append(l2)

		#self.brain.append(b1)
		#self.brain.append(b2)		


	def relu(self, mat, bias):

		result = []	
		sum = 0
		for i in range(len(mat)):
		#for(i ; i < mat.length ; i++){
			result.append(np.amax([0, mat[i] + bias ] ))
		
		return result

	def sigmoid(self, mat, bias):

		result = []	
		for i in range(len(mat)):
			try:
				oi = 1 / (1 + math.exp(-mat[i] + bias))
			except Exception as e: 
				print("Exceção no sigmoid")
				print(mat)
				print(bias)
				print(e)
				time.sleep(1000)
			#print(oi)
			result.append(oi)
		
		return result		

	def inferenciaRedeNeural(self, input):


		output = input
		for i in range(len(self.architecture)-1):
			input = output

			if self.drawNN is not False:
				self.drawNN.layerOutput[i] = input

			biasIndex = int(len(self.architecture)-1 + i)

			output = np.matmul(input, self.brain[i])	

			# If last layer, than activation function is sigmoid, otherwise, relu
			if i+1 == len(self.architecture)-1:
				output = self.sigmoid(output, self.brain[biasIndex])
			else:
				output = self.relu(output, self.brain[biasIndex])

		if self.drawNN is not False:
			self.drawNN.layerOutput[i+1] = output

		# Draw only if we have the pygame initialized. Work aroud detecdetd
		# TODO Pass this config to draw()
		#if self.drawNN is not None:
		#	self.drawNN.setInput(input)
		#	self.drawNN.setOutput(output)
			#self.drawNN.setLayer2(layer2)
			#self.drawNN.setOutput(output)	


		#output = np.matmul(layer1, self.brain[1])
		#output = self.sigmoid(output, self.brain[3])
			
		# Draw only if we have the pygame initialized. Work aroud detecdetd
		# TODO Pass this config to draw()
		#if self.drawNN is not None:
		#	self.drawNN.setInput(input)
		#	self.drawNN.setLayer1(layer1)
		#	self.drawNN.setLayer2(layer2)
		#	self.drawNN.setOutput(output)	

		return output


	def update(self, Bola):
		if self.player_type == "human":				# Este player é controlado pelas teclas do teclado, então não faz nada aqui
			pass	
		elif self.player_type == "bot_ball_follow":	# Este player segue a bola no eixo y, então vamos desenrolar os bang aqui
			
			if Bola.posicao[1] > self.position[1]:
				self.movePlayerBaixo()

			if Bola.posicao[1] < self.position[1]:
				self.movePlayerCima()

		elif self.player_type == "artificial_neural_network":
			sensores = []

			sensor1 = abs(Bola.posicao[0] - self.position[0])
			sensor2 = abs(Bola.posicao[1] - self.position[1])

			if sensor1 > 0:
				sensor1 = sensor1 / self.GAME_WIDTH
			else:
				sensor1 = 0

			if sensor2 > 0:
				sensor2 = sensor2 / self.GAME_HEIGHT
			else:
				sensor2 = 0			
			
			sensores.append(sensor1)
			sensores.append(sensor2)

			output = self.inferenciaRedeNeural(sensores)

			if output[0] > 0.5:
				self.movePlayerCima()
			else:
			#if output[1] > 0.5:
				self.movePlayerBaixo()
