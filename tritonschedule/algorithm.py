import itertools

from random import uniform
from random import randint
from classtime import ClassTime

class AlgorithmError(Exception):
    pass

class Algorithm:
    def __init__(self, schedule):
        """
        Constructor for the Algorithm class. The constructor turns the Schedule
        output into chromosomes for individuals.
        """
        self.chromosomes = {}
        self.schedule = schedule

        # Get all the possible alleles, which would be a specific lecture and
        # section(s) for a course.
        for code, courseList in schedule.items():
            # Treat each course as a chromosome.
            self.chromosomes[code] = []

            # Find all the genes for the "chromosome".
            for index in range(len(courseList)):
                course = courseList[index]
                indices = {}

                # Find set of all sections for the lecture.
                for meetingType, meeting in course.items():
                    if meetingType == "LE" or meetingType == "FI":
                        continue

                    indices[meetingType] = [i for i in range(len(meeting))]
                
                # Create a gene with one possibility for each section for the
                # lecture and add it to the chromosome.
                if len(indices) > 0:
                    # Find the Cartesian Product of the different types of
                    # sections to get all forms of the gene.
                    product = [dict(zip(indices.keys(), x))
                               for x in itertools.product(*indices.values())]
                
                    # Encode the lecture index into the gene.
                    for gene in product:
                        gene["LE"] = index
                        self.chromosomes[code].append(gene)
                else:
                    self.chromosomes[code].append({"LE": index})

    def getFitness(self, individual):
        """
        Calculates the fitness of an individual by adding points for certain
        factors. This includes: having no conflicts.

        :param self: the Algorithm object
        :param individual: the individual to calculate the fitness for
        :returns: the fitness value of the individual
        """
        fitness = 0
        schedule = self.schedule

        earliestTime = ClassTime.fromString("MTuWThFS 12:00a-8:00a")
        latestTime = ClassTime.fromString("MTuWThFS 4:30p-11:59p")
        lunch = ClassTime.fromString("MTuWThFS 12:00p-1:00p")

        # Sum the fitness for each section.
        for course, meetings in individual.items():
            index = meetings["LE"]
            meetingInfo = schedule[course][index]
            final = None

            if "FI" in meetingInfo:
                final = meetingInfo["FI"]["time"]

            for meetingType, meeting in meetings.items():
                item = meetingInfo[meetingType]

                if meetingType != "LE":
                    item = item[meeting]

                # Check for no conflicts.
                for course2, meetings2 in individual.items():
                    for meetingType2, meeting2 in meetings2.items():
                        index2 = meetings2["LE"]

                        meetingInfo2 = schedule[course2][index2]
                        item2 = meetingInfo2[meetingType2]

                        if meetingType2 != "LE":
                            item2 = item2[meeting2]

                        # Check for no time conflicts.
                        if not item["time"].conflictsWith(item2["time"]):
                            fitness += 1
                        else:
                            fitness -= 2

                        # Check for no finals conflicts.
                        if final is not None and "FI" in meetingInfo2:
                            final2 = meetingInfo2["FI"]["time"]

                            if not final.conflictsWith(final2):
                                fitness += 1

                                if final.isOnDay(final2.days):
                                    fitness -= 1
                                else:
                                    fitness += 1
                            else:
                                fitness -= 5

                # Check for too early class.
                if item["time"].isTimeAfter(earliestTime):
                    fitness += 1

                # Check for too late class.
                if item["time"].isTimeBefore(latestTime):
                    fitness += 1

                # Check for lunch break.
                if not item["time"].conflictsWith(lunch):
                    fitness += 1

            if final is not None:
                if final.isTimeAfter(earliestTime):
                    fitness += 1

                if final.isTimeBefore(latestTime):
                    fitness += 1

        return fitness

    def initiate(self, size, crossoverRate, mutateRate, elitism):
        """
        Creates an initial, random population so the genetic algorithm has a
        base to start from.

        :param self: the Algorithm object
        :param size: the population size
        """
        self.capacity = size
        self.crossoverRate = crossoverRate
        self.mutateRate = mutateRate
        self.elitism = elitism
        self.population = []

        # Keep adding random individuals until the population is full.
        while len(self.population) < self.capacity:
            individual = {}

            for locus, genes in self.chromosomes.items():
                index = randint(0, len(genes) - 1)
                individual[locus] = self.chromosomes[locus][index]

            self.population.append(individual)

        # Get fitness information for the current generation.
        self.calculateFitness()

    def calculateFitness(self):
        """
        Sorts the current population by fitness (least to greatest) and then
        calculates the fitness for each individual and the sum of the fitness
        values for the population.

        :param self: the Algorithm object
        """
        # Sort the population by fitness.
        self.population = sorted(self.population, key=lambda x:
                                 self.getFitness(x))

        # Calculate the fitnesses of the population.
        self.fitness = [0] * len(self.population)
        self.fitnessSum = 0
        
        for i in range(len(self.population)):
            self.fitness[i] = self.getFitness(self.population[i])
            self.fitnessSum += self.fitness[i]
        
        # Get the total fitness for a fitness proportionate selection.
        self.fitnessSum = float(self.fitnessSum)

    def evolve(self):
        """
        Picks which members of the population will not be discarded for the next
        generation by finding the fittest individuals.
        """
        # Select parents using fitness proportionate selection.
        def select():
            previousProb = 0.0

            for i in range(len(self.population)):
                chance = previousProb + float(self.fitness[i]) / self.fitnessSum
                previousProb = chance

                if uniform(0.0, 1.0) <= chance:
                    return self.population[i]

        # Keep the most fit individual for the next generation.
        nextGeneration = []

        for i in range(int(self.capacity * self.elitism)):
            nextGeneration.append(self.population[-(i + 1)])

        # Fill the next generation with offspring of selected parents.
        while len(nextGeneration) < self.capacity:
            parent1 = select()
            parent2 = select()

            nextGeneration.append(self.crossover(parent1, parent2))

        # Add some diversity to the next generation with random mutation.
        for individual in self.population:
            self.mutate(individual)

        # Make the next generation become the current generation.
        self.population = nextGeneration

        # Get fitness information for the current generation.
        self.calculateFitness()
            
    def crossover(self, parent1, parent2):
        """
        After selection occurs, parents will be chosen from remaining population
        and children will be created by crossing the genes at certain points.
        """
        child = {}

        # Copy genes from either the first parent or second parent.
        # Shallow copy is used here since the values are just numbers.
        for chromosome in parent1:
            if uniform(0.0, 1.0) < self.crossoverRate:
                child[chromosome] = parent2[chromosome].copy()
            else:
                child[chromosome] = parent1[chromosome].copy()

        return child

    def mutate(self, individual):
        """
        Picks random individuals in the population and mutates their genes to
        provide some additional genetic diversity.
        """
        for chromosome, gene in individual.items():
            if uniform(0.0, 1.0) < self.mutateRate:
                pool = self.chromosomes[chromosome]
                individual[chromosome] = pool[randint(0, len(pool) - 1)]

    def getHighestFitness(self):
        """
        Returns the fitness value of the most fit individual in the population.
        """
        if self.fitness:
            return self.fitness[len(self.fitness) - 1]

        return 0

    def getTotalFitness(self):
        """
        Returns the sum of all of the fitness values of individuals in the
        population.
        """
        return self.fitnessSum or 0

    def printFittest(self):
        fittest = self.population[len(self.population) - 1]

        for courseCode, info in fittest.items():
            courseIndex = info["LE"]
            course = self.schedule[courseCode][courseIndex]

            print(courseCode + ":")

            for meetingType, index in info.items():
                meeting = course[meetingType]
                time = "N/A"

                if meetingType != "LE":
                    time = meeting[index]["time"]
                else:
                    time = meeting["time"]

                print("\t" + meetingType + ": " + str(time))

            if "FI" in course:
                print("\tFI: " + str(course["FI"]["time"]))
