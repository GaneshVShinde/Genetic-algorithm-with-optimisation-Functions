import random 

class genetic(object):
    def __init__(self,
                functionToOptimize,min,max,bitSize,
                popSize= 100,muteProbab=0.01,fitPopSize=40):
        if(callable(functionToOptimize)):
            self.fitness_func = functionToOptimize 
        else:
            raise ValueError('functionToOptimize should be callable object')
        
        if (len(min) == len(max)):
            self.max = max
            self.min = min
        else:
            raise ValueError('min and max length should be equal')
        
        self.popSize = popSize
        self.bitSize = bitSize
        self.numVer = len(max)
        self.chromosome = self.genrate_random_population()
        self.mutationProbab = muteProbab
        self.fitPopSize = fitPopSize

    def get_decimals(self,singleChromoSone):
        dec = []
        l = 0
        h = self.bitSize
        for i in range(len(self.min)):
            dec.append(self.eval_binToDec(singleChromoSone[l:h],self.min[i],self.max[i]))
            l = h
            h = h + h
        return(dec)


    def cal_fitness(self):
        fitnessVal = [self.fitness_func(self.get_decimals(chromo)) for chromo in self.chromosome]
        return(fitnessVal)

    def mutation(self,mutateNoOfBits=1):
        for i in range(len(self.chromosome)):
            if (random.uniform(0.0,1.0) < self.mutationProbab):
                bitsTochamge=random.sample(range(0,self.bitSize),mutateNoOfBits)
                for bit in bitsTochamge:
                    self.chromosome[i][bit] = int(not self.chromosome[i][bit])

    def genrate_new_population(self,crossNumParent=2):
        best_parents=self.selection()

        offsprings = []
        while(len(offsprings)<self.popSize):
            parents=random.sample(range(0,len(best_parents)),crossNumParent)
            c1,c2=self.two_pointCrossOver(best_parents[parents[0]],best_parents[parents[1]])
            offsprings.append(c1)
            offsprings.append(c2)
        self.chromosome = offsprings
        self.mutation()

    def two_pointCrossOver(self,p1,p2):
        totalBitSize = len(self.min)*self.bitSize
        lb=random.choice(range(1,int(totalBitSize/2))) #lower bit
        mb=random.choice(range(int(totalBitSize/2),totalBitSize)) #max bit
        c1 = p1[0:lb]+p2[lb:mb]+p1[mb:totalBitSize]
        c2 = p2[0:lb]+p1[lb:mb]+p2[mb:totalBitSize]
        return((c1,c2))

    def one_pointCrossOver(self,p1,p2):
        totalBitSize = len(self.min)*self.bitSize
        h1=random.choice(range(1,(totalBitSize -1)))
        c1 = p1[0:h1]+p2[h1:totalBitSize]
        c2 = p2[0:h1]+p1[h1:totalBitSize]
        return((c1,c2))

    def selection(self):
        # selecting directly 50 best but implement tornament or Roulette Wheel Selection
        fit=self.cal_fitness()
        selected=[x for _,x in sorted(zip(fit,self.chromosome))]
        #print(selected[0:10])
        return(selected[0:self.fitPopSize])


    def find_optimum(self,epochs=100):
        self.chromosome = self.genrate_random_population()
        self.finalVals=[]
        for i in range(epochs):
            self.genrate_new_population()
            fitnessVal=self.cal_fitness()
            self.finalVals=[(x,self.get_decimals(y)) for x,y in sorted(zip(fitnessVal,self.chromosome))]
            #self.finalVals.append( lst)
        return(self.finalVals[0])


    def eval_binToDec(self,binVal,min_=None,max_=None):
        min = min_
        max = max_
        if(min==None):
            min = self.min
            max = self.max
        return(min +( ((max - min)/((2**self.bitSize) ))*
                sum([(2**i) * binVal[i] for i in range(self.bitSize) ])))

    def genrate_random_population(self):
        """initialy this is just for binaty kind of stuff but need implememntation for 
        set of decimal nos as well"""
        totalBitSize = len(self.min)*self.bitSize
        return([[random.choice((0,1)) for _ in range(totalBitSize)] for i in range(self.popSize)])



func = lambda x: x[0]*x[0]

def Sphere (list):
    return sum(map(lambda x: x ** 2, list))

rosenbrock = lambda x:((1-x[0])**2) + ((x[1]-(x[0]**2))**2)

beale = lambda x:((1.5-x[0]+(x[0]*x[1]))**2)+((2.25-x[0]+(x[0]*x[1]**2))**2)+((2.625-x[0]+(x[0]*x[1]**3))**2)

if __name__== "__main__":
    b=genetic(beale,[-5.12,-5.12],[5.12,5.12],12)
    # b.chromosome[0]=[0,0,0,0,0,0,0,0,0,0] 
    # b.chromosome[1]=[0,0,0,0,0,0,0,0,0,0]
    print(b.find_optimum(500))



# def genetic():
#     pass

