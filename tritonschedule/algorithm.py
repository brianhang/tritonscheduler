import pprint
import itertools

class Algorithm:
    def __init__(self, schedule):
        """
        Constructor for the Algorithm class. The constructor turns the Schedule
        output into chromosomes for individuals.
        """
        self.chromosomes = {}

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

    def initiate(self):
        """
        Creates an initial, random population so the genetic algorithm has a
        base to start from.
        """
        pass

    def select(self):
        """
        Picks which members of the population will not be discarded for the next
        generation by finding the fittest individuals.
        """
        pass

    def crossover(self):
        """
        After selection occurs, parents will be chosen from remaining population
        and children will be created by crossing the genes at certain points.
        """
        pass

    def mutate(self):
        """
        Picks random individuals in the population and mutates their genes to
        provide some additional genetic diversity.
        """

    def evolve(self):
        """
        Increments the generation and performs selection of fit individuals,
        reproduction of fit individuals, and random mutation.
        """
        pass

    def getHighestFitness(self):
        """
        Returns the fitness value of the most fit individual in the population.
        """

    def getTotalFitness(self):
        """
        Returns the sum of all of the fitness values of individuals in the
        population.
        """
