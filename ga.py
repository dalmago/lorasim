import random
from multiprocessing import Process, Queue
from loraDir import run as runSim

# MAXIMIZE, MINIMIZE = 1, 2

class Individual(object):
    alleles = (0,1)
    length = 6
    seperator = ''
    # optimization = MINIMIZE

    def __init__(self, chromosome=None):
        # self.nodes _nodes

        self.chromosome = chromosome or self._makechromosomes()
        self.score = None  # set during evaluation

    def fitness(self, optimum=None):
        # de 0 a 100
        # 0 eh baixo
        self.der, self.energy = self._evaluate()

        fit = self.der

        self.score = fit

        return fit

    def crossover(self, other):

        length = nodes*self.length

        crossover_point_1 = random.randrange(0, length)
        crossover_point_2 = random.randrange(crossover_point_1, length)

        new_chromossome = self.chromosome[:crossover_point_1]
        new_chromossome.extend(other.chromosome[crossover_point_1:crossover_point_2])
        new_chromossome.extend(self.chromosome[crossover_point_2:])

        # chrom = self.chromosome[:length//3]
        # chrom.extend(other.chromosome[length//3:2*length//3])
        # chrom.extend(self.chromosome[2*length//3:])

        if random.random() < 0.1:
            mutation_len = round(length*random.uniform(0, 0.3))

            for i in range(mutation_len):
                index = random.randrange(0, length)
                new_chromossome[index] ^= 1


        # chrom = self.chromosome[:nodes*self.length//2]
        # chrom.extend(other.chromosome[nodes*self.length//2:])

        ind = Individual(chromosome=new_chromossome)
        ind.fitness()

        return ind

    def _evaluate(self):
        der = []
        energy = []

        process = []
        data_q = Queue()

        for i in range(10):
            p = Process(target=runSim, args=(4, self._get_sf_bw(), nodes, data_q))
            process.append(p)
            p.start()

        for i in range(10):
            process[i].join()

            if data_q.empty():
                raise Exception("Data queue empty")

            x,y = data_q.get()
            der.append(x)
            energy.append(y)

        return sum(der)/len(der), sum(energy)/len(energy)


    def _get_sf_bw(self):
        sf_bw = []

        for i in range(int(len(self.chromosome)/self.length)):
            c = self.chromosome[i*self.length:(i+1)*self.length]

            sf = 0
            for j in range(4):
                sf += c[j] * 2 ** j

            if sf < 7 or sf > 12:
                sf = 12

            bw = 0
            for j in range(4, 6):
                bw += c[j] * (2 ** (j - 4))

            if bw == 0:
                bw = 125
            elif bw == 1:
                bw = 250
            else:
                bw = 500

            sf_bw.append([sf, bw])

        return sf_bw


    def _makechromosomes(self):
        "makes a chromosome from randomly selected alleles."
        chromo = []
        for n in range(nodes):
            c = [random.choice(self.alleles) for gene in range(self.length)]
            while not self._is_valid_chromosome(c):
                c = [random.choice(self.alleles) for gene in range(self.length)]

            chromo.extend(c)

        return chromo

    def _is_valid_chromosome(self, chromosome):
        """
        (ordem inversa dos bits)
        ex.:
        chromossome: 110101

        1101 - sf 11
        01  - bw 500 (0-125, 1-250, 2-500)

        """
        sf = 0
        for i in range(4):
            sf += chromosome[i] * 2**i

        if sf < 7 or sf > 12:
            return False

        bw = 0
        for i in range(4, 6):
            bw += chromosome[i] * (2**(i-4))

        if bw > 2:
            return False
        return True

class Environment(object):
    def __init__(self, kind, population=None, size=300, maxgenerations=600,
                 generation=0, crossover_rate=0.90, mutation_rate=0.02,
                 optimum=None):
        self.kind = kind
        self.size = size
        self.optimum = optimum
        self.population = population or self._makepopulation()
        for individual in self.population:
            individual.fitness(self.optimum)
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.maxgenerations = maxgenerations
        self.generation = generation
        # self.best = max(self.population, key=lambda x: x.score)
        self.population.sort(key=lambda indiv: indiv.score, reverse=True)
        self.best = self.population[0]
        self.report()

    def step(self):
        self.generation += 1
        self.population = self.population[:self.size // 2]
        self.bests = self.population[:]
        random.shuffle(self.bests)

        for i in range(len(self.bests)//2):
            self.population.append(self.bests[i*2].crossover(self.bests[(i+1)*2 -1]))

        for i in range(len(self.bests) // 2):
            self.population.append(
                self.bests[(i + 1) * 2 - 1].crossover(self.bests[i * 2])
            )

        self.population.sort(key=lambda indiv: indiv.score, reverse=True)
        self.best = self.population[0]
        self.report()

    def _makepopulation(self):
        return [self.kind() for individual in range(self.size)]

    def _goal(self):
        return self.generation >= self.maxgenerations or self.best.score >= self.optimum

    def run(self):
        try:
            while not self._goal():
                self.step()
        except KeyboardInterrupt:
            self.report()

    def report(self):
        print("=" * 70)
        print("generation: ", self.generation)
        print("best:       ", self.best.score)
        print("der:        ", self.best.der)
        print("energy:     ", self.best.energy)
        print("nodes       ", nodes)

nodes = 200
env = Environment(Individual, optimum=1)
env.run()
