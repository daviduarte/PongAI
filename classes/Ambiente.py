import numpy as np
import copy
import random


class Environment:
	def __init__(self, numIndividuals, individuals, architecture, rank = False, selection=None):


		self.architecture = architecture

		self.MUTATION_PROBABILITY = 10
		self.INPUT_NEURON = 8
		self.HIDDEN_NEURON1 = 16
		self.HIDDEN_NEURON2 = 16
		self.OUTPUT_NEURON = 4
		self.numIndividuals = numIndividuals
		self.individuals = individuals 
		self.currentGeneration = 0
		self.rank = False			# Use just the 'rank' best fit methods for some selection method?
		if rank is not False:
			self.rank = rank

		self.selection = selection

	"""
		Given all individuals, return a table with the scores
	"""
	def getScoreSet(self):

		scoreSet = []
		for individual in self.individuals:
			scoreSet.append(individual.score)
		return scoreSet

	def saveMostApt(self, index_fittest1,score_most_fittest):
		pass

	def extractBrains(self):
		brain_set = []
		for individual in self.individuals:
			brain_set.append(individual.brain)
		return brain_set

	def updateNewBrains(self, newBrains):
		for i, brain in enumerate(newBrains):
			self.individuals[i].brain = copy.deepcopy(brain)


	"""
	Select an individuals by roullet method to replicate
	@score_set list Score of all individuals
	@return list Index of two individuals to replicate
	@score_sum float Sum of all sores of all individuals
	@excludeIndividual int Some individual to ignore in selection. 
	"""
	def roulletSelection(self, score_set, score_sum, excludeIndividual = -1):
		# Get a list with the most apts index in descending order
		index_list = [i[0] for i in sorted(enumerate(score_set), key=lambda x:x[1], reverse=True)]

		# Select 2 individuos for replication by roullet seledction		
		individual = -1
		score_ate_agora = 0
		rand = random.randrange(int(score_sum))
		for i in range(self.numIndividuals):
			score_ate_agora += score_set[index_list[i]]

			if score_ate_agora > rand or i == (self.numIndividuals-1):
				if excludeIndividual == index_list[i]:
					# Select the previous individual 
					individual = index_list[i-1]
				else:
					individual = index_list[i]
				break

		return individual

#	def kRandom(self, score_set):
#		index_list = [i[0] for i in sorted(enumerate(score_set), key=lambda x:x[1], reverse=True)]
#		interval = index_list[0:5]


	def justBestRankedIndividuals(self, score_set):
		# Get the index of most apts individuals
		#index_list = [i[0] for i in sorted(enumerate(score_set), key=lambda x:x[1], reverse=True)]

		# SORT THE LIST AND GET SELF.RANK FIRST INDIVIDUALS
		if self.rank is not False:
			score_set.sort(reverse=True)
			return score_set[0:self.rank]
			
		return score_set

		"""
		inde

		if self.rank is not False:
			print("Rank set to " + str(self.rank))
			return score_set[0:self.rank]

		return score_set
		"""

	def calculeWeightLen(self):
		# Calcule the weight number in the architecture
		numWeights = 0
		for i in range(len(self.architecture)-1):
			numWeights += self.architecture[i] + self.architecture[i+1]
		return numWeights

	def crossOverLayer(self, i, layerIndex, most_fitted_individual, most_fitted_individual2, crossoverPoint, brain_set, counter = 0):
		# Count the genes for single point crossingover. We consider the entire NN as a big single cromossomos
		#counter = 0
		for j in range(self.architecture[layerIndex]):

			for k in range(self.architecture[layerIndex+1]):
				prob = random.uniform(0, 100)

				if prob < self.MUTATION_PROBABILITY:
					brain_set[i][layerIndex][j][k] += np.random.normal(0, 1/6)
					#brain_set[i][0][j][k] = random.uniform(-1,1)


					if brain_set[i][layerIndex][j][k] > 1:
						brain_set[i][layerIndex][j][k] = 1
					if brain_set[i][layerIndex][j][k] < -1:
						brain_set[i][layerIndex][j][k] = -1						

				else:
					if counter > crossoverPoint  or self.selection == "mutation_only":
						brain_set[i][layerIndex][j][k] = copy.deepcopy(most_fitted_individual[layerIndex][j][k])
					else:
						brain_set[i][layerIndex][j][k] = copy.deepcopy(most_fitted_individual2[layerIndex][j][k])

				counter += 1

			# Crossover the bias
			biasIndex = int(len(self.architecture)-1 + layerIndex)	# The "self.brain_set" is a list where the first items are the ANN layers and the last layers are the bias.
			if counter > crossoverPoint or self.selection == "mutation_only":
				brain_set[i][biasIndex] = copy.deepcopy(most_fitted_individual[biasIndex])				
			else:
				brain_set[i][biasIndex] = copy.deepcopy(most_fitted_individual2[biasIndex])

			counter += 1		

		# Mutate the bias
		prob = random.uniform(0, 100)
		if prob < self.MUTATION_PROBABILITY:
			brain_set[i][biasIndex] += np.random.normal(0, 1/6)
			#brain_set[i][3] = random.uniform(-1,1)

			if brain_set[i][biasIndex] > 1:
				brain_set[i][biasIndex] = 1
			if brain_set[i][biasIndex] < -1:
				brain_set[i][biasIndex] = -1
		#else:
		#	brain_set[i][3] = copy.deepcopy(most_fitted_individual[3])


		return counter

	def replicate(self, MUTATION_PROBABILITY):

		self.MUTATION_PROBABILITY = MUTATION_PROBABILITY
		
		brain_set = self.extractBrains()

		# Select 5 most fittest individuals, them, make a random selection for crossing over
		most_fittest_array = []
		newIndividuals = []

		score_set = self.getScoreSet()
		score_set_copy = copy.deepcopy(score_set)

		generationMean = np.mean(score_set)
		index_fittest1 = np.argmax(score_set)

		file = open('checkpoints/scores.txt', 'a')
		score_most_fittest = score_set[index_fittest1]
		file.write(str(score_most_fittest)+'-'+str(generationMean)+'-'+str(index_fittest1)+'\n')
		file.close()


		print(score_set_copy[index_fittest1])
		score_set_copy[index_fittest1] = float('-Inf')

		index_fittest2 = np.argmax(score_set_copy)
		print(score_set_copy[index_fittest2])
		score_set_copy[index_fittest2] = float('-Inf')

		index_fittest3 = np.argmax(score_set_copy)
		print(score_set_copy[index_fittest3])
		score_set_copy[index_fittest3] = float('-Inf')

		index_fittest4 = np.argmax(score_set_copy)
		print(score_set_copy[index_fittest4])
		score_set_copy[index_fittest4] = float('-Inf')		

		"""
		most_fittest_array.append(index_fittest1)
		most_fittest_array.append(index_fittest2)
		most_fittest_array.append(index_fittest3)
		most_fittest_array.append(index_fittest4)

		most_fitted_individual = copy.deepcopy(brain_set[index_fittest1])
		most_fitted_individual2 = copy.deepcopy(brain_set[index_fittest2])
		"""

		# Clone the most apt in the new generation
		brain_set[0] = copy.deepcopy(brain_set[index_fittest1])

		# Salva o mais apto
		self.saveMostApt(index_fittest1, score_most_fittest)
		self.currentGeneration += 1

		#weightsLen = self.INPUT_NEURON*self.HIDDEN_NEURON1 + self.HIDDEN_NEURON1*self.HIDDEN_NEURON2 + self.HIDDEN_NEURON2*self.OUTPUT_NEURON + 3
		weightsLen = self.calculeWeightLen()
		#crossoverPoint = random.randrange(weightsLen)
		#crossoverPoint = int(weightsLen/2)

		# Use all the individuals in selection?
		score_set = self.justBestRankedIndividuals(score_set)

		score_sum = np.sum(score_set)
		for i in range(1, self.numIndividuals):	
			
			index1 = self.roulletSelection(score_set, score_sum)
			index2 = self.roulletSelection(score_set, score_sum, excludeIndividual=index1)
			most_fitted_individual = copy.deepcopy(brain_set[index1])
			most_fitted_individual2 = copy.deepcopy(brain_set[index2])

			print("Roleta selecionou o individuo " + str(index1) + ", socore " + str(score_set[index1]))
			print("Roleta selecionou o individuo " + str(index2) + ", socore " + str(score_set[index2]))

			crossoverPoint = random.randrange(weightsLen)

			"""			
			most_fittest_array_aux	= []
			most_fittest_array_aux = copy.deepcopy(most_fittest_array)

			index = random.randrange(4)
			most_fitted_individual = copy.deepcopy(brain_set[most_fittest_array_aux[index]])
			del most_fittest_array_aux[index]

			index2 = random.randrange(3)
			most_fitted_individual2 = copy.deepcopy(brain_set[most_fittest_array_aux[index2]])
			del most_fittest_array_aux[index2]
			"""

			counter = self.crossOverLayer(	i, 
											0, 
											most_fitted_individual, 
											most_fitted_individual2, 
											crossoverPoint,
											brain_set)
			#counter = crossOverLayer(i, i, most_fitted_individual, most_fitted_individual2, counter)


		self.updateNewBrains(brain_set)
			