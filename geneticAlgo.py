from random import randint
from copy import *
from chromosome import *
from utility import *
# import view  # Disabled currently

# initPopulationSize = 5
initPopulationSize = 3
breakPoint = 25
mutationRatio = 0.2
# mutationRatio = 0.1
generation = 5000
selectionRatioOnGeneration = 0.2
# selectionRatioOnGeneration = 0.5
Gens_Length = 8
# Gens_Length = 10

Popu = []
Gens = []

TotalSucc = 0   # Total number of successful runs
TotalSteps = 0  # Sum up all steps from each run to a total number

class geneticAlgo:
    def __init__(self, boardsize=8):
        global initPopulationSize
        global Popu
        global Gens_Length
        global breakPoint
        global Gens

        Gens_Length = boardsize
        breakPoint = int(boardsize/2)
        Gens = Chromosome()
        Popu = Population()

        # print('Before Init: ', gens, population) # Debug

        for i in range(0, Gens_Length):
            Gens.append(i)

        for i in range(0, initPopulationSize):
            new_chromosome = self.generate_random_chromosome()
            Popu.append(new_chromosome)
            # print(new_chromosome, '\n') # Debug

        # print('After Init: ', gens, population) # Debug

    def prob(self, chromosome=Chromosome()):
        return chromosome.fitness() / Popu.sumFitness()

    def mating_pool(self):
        pool = []
        fitFactor = 1 - 1/initPopulationSize
        for item in Popu:
            canBeSelect = int(self.prob(item) + fitFactor)
            # print('Parent Selection:  (prob of fitness, canBeSelect) = ', '(', self.prob(item), ',', canBeSelect, ')') # Debug
            if canBeSelect == 1:
                pool.append(copy.deepcopy(item))

        return pool

    def selection(self, pool=[]):
        parent1_I = randint(0, pool.__len__() - 1)
        parent2_I = randint(0, pool.__len__() - 1)

        return pool[parent1_I], pool[parent2_I]

    def crossover(self, chromosome1=Chromosome(), chromosome2=Chromosome()):
        ### Start of original
        # global Gens
        #
        # gens_copy = copy.deepcopy(Gens)
        # child = Chromosome(copy.deepcopy(Gens))
        # for i in range(0, breakPoint):
        #     child[i] = chromosome1[i]
        #
        # j = breakPoint
        # for i in range(breakPoint, gens_copy.__len__()):
        #     if chromosome2[i] not in child[:breakPoint]:
        #         child[j] = chromosome2[i]
        #         j = j + 1
        #
        # print('child =', child)
        #
        # gencopy = copy.deepcopy(Gens)
        # availabeGens = subList(gencopy, child[:j])
        # for i in range(j, child.__len__()):
        #     # print(i, j, child.__len__())  # Debug
        #     child[i] = availabeGens[i - j]
        #
        # return child
        ### End of original   2018.12.04 marked.


        child = Chromosome()
        for i in range(0, breakPoint):
            child.append(chromosome1[i])

        remainCnt = 0
        for i in range(breakPoint, chromosome1.__len__()):
            if chromosome2[i] not in child[:breakPoint]:
                child.append(chromosome2[i])
            else:
                remainCnt += 1

        remainGen = []

        if remainCnt != 0:  # Still remaining elements to be filled in.
            for i in range(0, breakPoint):
                if chromosome2[i] not in child[:breakPoint]:
                    remainGen.append(chromosome2[i])

            for i in range(0, remainGen.__len__()):
                child.append(remainGen[i])

        # print('child =', child)  # Debug

        return child

    def generate_random_chromosome(self):
        global Gens

        chromosome = Chromosome(copy.deepcopy(Gens))
        gens_copy = copy.deepcopy(Gens)
        for i in range(0, gens_copy.__len__()):
            randGenIndex = randint(0, gens_copy.__len__() - 1)
            randGen = gens_copy[randGenIndex]
            gens_copy.remove(randGen)
            chromosome[i] = randGen

        return chromosome

    def gaSolution(self):
        global Popu
        global mutationRatio
        global generation
        global Gens
        global TotalSucc
        global TotalSteps
        global logFile

        bests = Population()
        bests.append(Popu.bestChromosome())

        fitAnswer = 0
        generation_counter = 0
        while fitAnswer != Gens.fullScore() and generation_counter < generation:
            population_childs = Population()
            for j in range(0, initPopulationSize):
                parent1, parent2 = self.selection(self.mating_pool())
                child = self.crossover(parent1, parent2)
                population_childs.append(child)

            Popu.mutating(mutationRatio)

            Popu = Popu.NextGeneration(selectionRatioOnGeneration, population_childs)

            nextGenerationBestAnswer = Popu.bestChromosome()
            bests.append(nextGenerationBestAnswer)

            fitAnswer = nextGenerationBestAnswer.fitness()

            strLine = 'Generation ' + str(generation_counter) + ': ' + str(nextGenerationBestAnswer) + ' fitness: ' + \
                      str(nextGenerationBestAnswer.fitness())

            print(strLine)

            LogFile.write(strLine + '\n')

            generation_counter = generation_counter + 1

        TotalSteps += generation_counter
        # print('Total steps = ', TotalSteps) # Debug

        if fitAnswer == Gens.fullScore():
            TotalSucc += 1

        # for item in bests:
        answer = bests.bestChromosome()
        print('----------------------------------------------------------')
        LogFile.write('----------------------------------------------------------\n')
        print('  Best answer: ', answer, ' fitness:', answer.fitness())
        LogFile.write('  Best answer: ' + str(answer) + ' fitness:' + str(answer.fitness()) + '\n')
        if fitAnswer == Gens.fullScore():
            print('  GOAL SUCCEED!  Answer is ', answer)
            LogFile.write('  GOAL SUCCEED!  Answer is ' + str(answer) + '\n')
        else:
            print('  Still attacks. GOAL FAIL!                             ')
            LogFile.write('  Still attacks. GOAL FAIL!                             \n')
        print('----------------------------------------------------------')
        LogFile.write('----------------------------------------------------------\n')

        return answer

    def getTotalSucc(self):
        global TotalSucc

        return TotalSucc

    def getTotalNumSteps(self):
        global TotalSteps

        return TotalSteps


# init()
# main()
