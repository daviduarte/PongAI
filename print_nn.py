import numpy as np
import pygame
import time
from utils import colors


INPUT_NEURON = 8
HIDDEN_NEURON1 = 16
HIDDEN_NEURON2 = 16
OUTPUT_NEURON = 4


class DrawNN():
	def __init__(self, archtecture, screen, weights = None):

		self.screen2 = screen

		self.archtecture = archtecture

		self.weights = weights

		self.layer1_neurons_positions = []
		self.layer2_neurons_positions = []
		self.layer3_neurons_positions = []
		self.layer4_neurons_positions = []

		self.layerOutput = [[], []]
		self.input = []
		self.layer1 = []
		self.lauer2 = []
		self.output = []

		self.lines_to_write_on_top = []

	def drawNeurons(self):

		border_left = 920
		border_top = 120
		inter_neurons_width = 45
		inter_layer_width = 80
		neuron_radius = 15
		
		# For layer 1
		offset = 0
		
		
		for i in range(self.archtecture[0]):

				
			x = border_left + 0 * inter_layer_width + 20
			y = border_top + (i * inter_neurons_width) + offset

			#myfont = pygame.font.SysFont('Comic Sans MS', 25)
			#if self.input[i] == 0:
			#	new_value = 0
			#else:
			#	new_value = round(self.input[i],1)

			#textsurface = myfont.render(str(new_value), False, (0, 0, 0))
			#self.screen2.blit(textsurface,(50,y-10))


			border_left + (i * inter_neurons_width)
			self.layer1_neurons_positions.append([x,y])

			if self.layerOutput[0][i] < 0.5:
				color = colors.RED
			else:
				color = colors.BLUE

			pygame.draw.circle(self.screen2, color, (x,y), neuron_radius)


		# For layer 2
		offset = 20
		for i in range(self.archtecture[1]):
			
			x = border_left + 1 * inter_layer_width + 20
			y = border_top + (i * inter_neurons_width) + offset

			border_left + (i * inter_neurons_width)
			self.layer2_neurons_positions.append([x,y])


			if self.layerOutput[1][i] < 0.5:
				color = colors.RED
			else:
				color = colors.BLUE

			pygame.draw.circle(self.screen2, color, (x,y), neuron_radius)

		"""
		# For layer 3
		offset = 45
		for i in range(self.archtecture[2]):
			
			x = border_width + 2 * inter_layer_width + 20
			y = border_width + (i * inter_neurons_width) + offset

			border_width + (i * inter_neurons_width)
			self.layer3_neurons_positions.append([x,y])

			if self.layer2[i] < 0.5:
				color = colors.WHITE
			else:
				color = colors.YELLOW

			pygame.draw.circle(self.screen2, color, (x,y), neuron_radius)

		# For layer 4
		offset = 185

		# Neurônios > 0.5 serão ativados
		argmax = np.argmax(self.output)
		for i in range(self.archtecture[3]):
			
			x = border_width + 3 * inter_layer_width + 20
			y = border_width + (i * inter_neurons_width) + offset

			border_width + (i * inter_neurons_width)
			self.layer4_neurons_positions.append([x,y])



			#if i == argmax:
			if self.output[i] > 0.5:
				color = colors.YELLOW
			else:
				color = colors.WHITE

			pygame.draw.circle(self.screen2, color, (x,y), neuron_radius)
		"""

	def drawLines(self):

		# Layer 1 - 2
		self.lines_to_write_on_top.append([])
		for i in range(self.archtecture[0]):
			for j in range(self.archtecture[1]):

				#if self.weights[0][i][j] > 0:
				#	color = PURPLE
				#else:
				#	color = BLUE

				if self.layerOutput[0][i] > 0.5:
					color = colors.RED
					self.lines_to_write_on_top[0].append([self.layer1_neurons_positions[i],self.layer2_neurons_positions[j]])
				else: 
					color = colors.BLUE

				pygame.draw.line(self.screen2, color, self.layer1_neurons_positions[i], self.layer2_neurons_positions[j], 1)

		"""
		# Layer 2 - 3
		self.lines_to_write_on_top.append([])
		for i in range(self.archtecture[1]):
			for j in range(self.archtecture[2]):

				#if self.weights[1][i][j] > 0:
				#	color = RED
				#else:
				#	color = BLUE

				if self.layerOutput[1][i] > 0.5:
					color = colors.RED
					self.lines_to_write_on_top[1].append([self.layer2_neurons_positions[i],self.layer3_neurons_positions[j]])
				else: 
					color = colors.BLUE				
				pygame.draw.line(self.screen2, color, self.layer2_neurons_positions[i], self.layer3_neurons_positions[j], 1)				

		
		# Layer 3 - 4
		self.lines_to_write_on_top.append([])
		for i in range(self.archtecture[2]):
			for j in range(self.archtecture[3]):		

				#if self.weights[2][i][j] > 0:
				#	color = RED
				#else:
				#	color = BLUE


				if self.layer2[i] > 0.5:
					color = colors.RED
					self.lines_to_write_on_top[2].append([self.layer3_neurons_positions[i],self.layer4_neurons_positions[j]])
				else: 
					color = colors.BLUE
				pygame.draw.line(self.screen2, color, self.layer3_neurons_positions[i], self.layer4_neurons_positions[j], 1)				
		"""

	def write_top_lines_again(self):

		for i in range(len(self.lines_to_write_on_top[0])):
			pygame.draw.line(self.screen2, colors.RED, self.lines_to_write_on_top[0][i][0], self.lines_to_write_on_top[0][i][1], 1)

		"""
		for i in range(len(self.lines_to_write_on_top[1])):
			pygame.draw.line(self.screen2, colors.RED, self.lines_to_write_on_top[1][i][0], self.lines_to_write_on_top[1][i][1], 1)

		for i in range(len(self.lines_to_write_on_top[2])):
			pygame.draw.line(self.screen2, colors.RED, self.lines_to_write_on_top[2][i][0], self.lines_to_write_on_top[2][i][1], 1)						
		"""

	# Lista das saídas dos neurônios

	def setInput(self, input_):
		self.input = input_

	def setLayer1(self, layer1):
		self.layer1 = layer1

	def setLayer2(self, layer2):
		self.layer2 = layer2

	def setOutput(self, output):
		self.output = output				

	def update(self, neurons):
		pass

	def setWeights(self, weights):
		self.weights = weights

	def draw(self):

		self.drawNeurons()
		self.drawLines()		
		self.write_top_lines_again()
		self.drawNeurons()
		self.lines_to_write_on_top = []
		