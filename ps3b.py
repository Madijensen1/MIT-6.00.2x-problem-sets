# Problem Set 3: Simulating the Spread of Disease and Virus Population Dynamics 

import random
import pylab

''' 
Begin helper code
'''

class NoChildException(Exception):
    """
    NoChildException is raised by the reproduce() method in the SimpleVirus
    and ResistantVirus classes to indicate that a virus particle does not
    reproduce. You can use NoChildException as is, you do not need to
    modify/add any code.
    """

'''
End helper code
'''

#
# PROBLEM 1
#
class SimpleVirus(object):

    """
    Representation of a simple virus (does not model drug effects/resistance).
    """
    def __init__(self, maxBirthProb, clearProb):
        """
        Initialize a SimpleVirus instance, saves all parameters as attributes
        of the instance.        
        maxBirthProb: Maximum reproduction probability (a float between 0-1)        
        clearProb: Maximum clearance probability (a float between 0-1).
        """

        self.MaxBirthProb = maxBirthProb
        self.clearProb = clearProb

    def getMaxBirthProb(self):
        """
        Returns the max birth probability.
        """
        return self.MaxBirthProb

    def getClearProb(self):
        """
        Returns the clear probability.
        """
        return self.clearProb

    def doesClear(self):
        """ Stochastically determines whether this virus particle is cleared from the
        patient's body at a time step. 
        returns: True with probability self.getClearProb and otherwise returns
        False.
        """
        if self.getClearProb() == 1:
            return True
        elif self.getClearProb() == 0:
            return False
        else:
            clear = random.random()
            if clear <= self.getClearProb():
                return True
            else:
                return False


    
    def reproduce(self, popDensity):
        """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the Patient and
        TreatedPatient classes. The virus particle reproduces with probability
        self.maxBirthProb * (1 - popDensity).
        
        If this virus particle reproduces, then reproduce() creates and returns
        the instance of the offspring SimpleVirus (which has the same
        maxBirthProb and clearProb values as its parent).         

        popDensity: the population density (a float), defined as the current
        virus population divided by the maximum population.         
        
        returns: a new instance of the SimpleVirus class representing the
        offspring of this virus particle. The child should have the same
        maxBirthProb and clearProb values as this virus. Raises a
        NoChildException if this virus particle does not reproduce.               
        """
        if popDensity == 1:
            raise NoChildException
        elif self.getMaxBirthProb() == 1:
            return SimpleVirus(self.getMaxBirthProb(),self.getClearProb())
        elif self.getMaxBirthProb() == 0:
            raise NoChildException
        else:
            toReproduce = random.random()
            if toReproduce <= self.getMaxBirthProb()*(1-popDensity):
                return SimpleVirus(self.getMaxBirthProb(),self.getClearProb())
            else:
                raise NoChildException
                


class Patient(object):
    """
    Representation of a simplified patient. The patient does not take any drugs
    and his/her virus populations have no drug resistance.
    """    

    def __init__(self, viruses, maxPop):
        """
        Initialization function, saves the viruses and maxPop parameters as
        attributes.

        viruses: the list representing the virus population (a list of
        SimpleVirus instances)

        maxPop: the maximum virus population for this patient (an integer)
        """

        self.viruses = viruses
        self.MaxPop = maxPop

    def getViruses(self):
        """
        Returns the viruses in this Patient.
        """
        return self.viruses


    def getMaxPop(self):
        """
        Returns the max population.
        """
        return self.MaxPop


    def getTotalPop(self):
        """
        Gets the size of the current total virus population. 
        returns: The total virus population (an integer)
        """

        return len(self.viruses)    


    def update(self):
        """
        Update the state of the virus population in this patient for a single
        time step. update() should execute the following steps in this order:
        
        - Determine whether each virus particle survives and updates the list
        of virus particles accordingly.   
        
        - The current population density is calculated. This population density
          value is used until the next call to update() 
        
        - Based on this value of population density, determine whether each 
          virus particle should reproduce and add offspring virus particles to 
          the list of viruses in this patient.                    

        returns: The total virus population at the end of the update (an
        integer)
        """
        if self.getMaxPop() == 0:
            return 0
        #determines whether each particle survives
        removeVirus = []
        for virus in self.getViruses():
            if virus.doesClear() == True:
                removeVirus.append(virus)
        #updates virus list 
        for virus in removeVirus:
            self.viruses.remove(virus)

        #determine virus reproduction
        currentVirusList = self.getViruses()[:]
        for virus in currentVirusList:
            try:
                #calculates current population density
                currentPopDens = self.getTotalPop()/self.getMaxPop()
                #reproduces
                baby = virus.reproduce(currentPopDens)
                self.viruses.append(baby)
            except NoChildException:
                #Virus failed to reproduce - we dont need to do anything except ignore
                pass

        return self.getTotalPop()

#
# PROBLEM 2
#
def simulationWithoutDrug(numViruses, maxPop, maxBirthProb, clearProb,
                          numTrials):
    """
    Run the simulation and plot the graph for problem 3 (no drugs are used,
    viruses do not have any drug resistance).    
    For each of numTrials trial, instantiates a patient, runs a simulation
    for 300 timesteps, and plots the average virus population size as a
    function of time.

    numViruses: number of SimpleVirus to create for patient (an integer)
    maxPop: maximum virus population for patient (an integer)
    maxBirthProb: Maximum reproduction probability (a float between 0-1)        
    clearProb: Maximum clearance probability (a float between 0-1)
    numTrials: number of simulation runs to execute (an integer)
    """

    averagesList = []
    for i in range(numTrials):
        #create virus list
        virusList = []
        for j in range(numViruses):
            virusList.append(SimpleVirus(maxBirthProb,clearProb))
        #create patient with virus list
        newP = Patient(virusList,maxPop)
        #run simulation 300 times
        for k in range(300):
            newP.update()
            #find average at each step and add to list
            try:
                averagesList[k] = float((averagesList[k]+newP.getTotalPop())/2)

            except IndexError:
                averagesList.append(float(newP.getTotalPop()))

        #create pylab graph
    x = range(300)
    y = averagesList
    pylab.plot(x,y, label = "SimpleVirus")    
    pylab.xlabel("Time Steps")
    pylab.ylabel("Average Virus Population")
    pylab.title("SimpleVirus simulation")
    pylab.legend(loc = "best")
    pylab.show()

#simulationWithoutDrug(100,1000,0.1,0.05,100)


#
# PROBLEM 3
#
class ResistantVirus(SimpleVirus):
    """
    Representation of a virus which can have drug resistance.
    """   

    def __init__(self, maxBirthProb, clearProb, resistances, mutProb):
        """
        Initialize a ResistantVirus instance, saves all parameters as attributes
        of the instance.

        maxBirthProb: Maximum reproduction probability (a float between 0-1)       

        clearProb: Maximum clearance probability (a float between 0-1).

        resistances: A dictionary of drug names (strings) mapping to the state
        of this virus particle's resistance (either True or False) to each drug.
        e.g. {'guttagonol':False, 'srinol':False}, means that this virus
        particle is resistant to neither guttagonol nor srinol.

        mutProb: Mutation probability for this virus particle (a float). This is
        the probability of the offspring acquiring or losing resistance to a drug.
        """

        SimpleVirus.__init__(self, maxBirthProb, clearProb)
        self.resistances = resistances
        self.mutProb = mutProb


    def getResistances(self):
        """
        Returns the resistances for this virus.
        """
        return self.resistances

    def getMutProb(self):
        """
        Returns the mutation probability for this virus.
        """
        return self.mutProb

    def isResistantTo(self, drug):
        """
        Get the state of this virus particle's resistance to a drug. This method
        is called by getResistPop() in TreatedPatient to determine how many virus
        particles have resistance to a drug.       

        drug: The drug (a string)

        returns: True if this virus instance is resistant to the drug, False
        otherwise.
        """
        if drug in self.getResistances().keys():
            if self.getResistances()[drug] == True:
                return True
            else:
                return False
        else:
            return False


    def reproduce(self, popDensity, activeDrugs):
        """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the TreatedPatient class.

        A virus particle will only reproduce if it is resistant to ALL the drugs
        in the activeDrugs list. For example, if there are 2 drugs in the
        activeDrugs list, and the virus particle is resistant to 1 or no drugs,
        then it will NOT reproduce.

        Hence, if the virus is resistant to all drugs
        in activeDrugs, then the virus reproduces with probability:      

        self.maxBirthProb * (1 - popDensity).                       

        If this virus particle reproduces, then reproduce() creates and returns
        the instance of the offspring ResistantVirus (which has the same
        maxBirthProb and clearProb values as its parent). The offspring virus
        will have the same maxBirthProb, clearProb, and mutProb as the parent.

        For each drug resistance trait of the virus (i.e. each key of
        self.resistances), the offspring has probability 1-mutProb of
        inheriting that resistance trait from the parent, and probability
        mutProb of switching that resistance trait in the offspring.       

        For example, if a virus particle is resistant to guttagonol but not
        srinol, and self.mutProb is 0.1, then there is a 10% chance that
        that the offspring will lose resistance to guttagonol and a 90%
        chance that the offspring will be resistant to guttagonol.
        There is also a 10% chance that the offspring will gain resistance to
        srinol and a 90% chance that the offspring will not be resistant to
        srinol.

        popDensity: the population density (a float), defined as the current
        virus population divided by the maximum population       

        activeDrugs: a list of the drug names acting on this virus particle
        (a list of strings).

        returns: a new instance of the ResistantVirus class representing the
        offspring of this virus particle. The child should have the same
        maxBirthProb and clearProb values as this virus. Raises a
        NoChildException if this virus particle does not reproduce.
        """
        if popDensity == 1:
            raise NoChildException
        #check if virus has resistance to all drugs
        resistance = True
        while resistance:
            if len(activeDrugs) > 0:
                for drug in activeDrugs:
                    resistance = self.isResistantTo(drug)
                break
            else: 
                break
        if resistance == False:
            raise NoChildException
        else:
            #create offspring 
            babyresist = {}
            resistprob = random.random()
            if resistprob <= self.getMaxBirthProb() * (1 - popDensity):
                if self.getMutProb() == 0:
                    babyresist = self.getResistances().copy()
                elif self.getMutProb() == 1:
                    for key,value in self.getResistances().items():
                        if value == True:
                            babyresist[key] = False
                        else:
                            babyresist[key] = True
                #if mutation prob is a float
                else:
                    #figure out offspring resistances
                    for key,value in self.getResistances().items():
                        singleDrugResist = random.random()
                        #check if parents resist is passed on
                        if singleDrugResist <= self.getMutProb():
                            if value == True:
                                babyresist[key] = True
                            else:
                                babyresist[key] = False
                        else:
                            if value == True:
                                babyresist[key] = False
                            else:
                                babyresist[key] = True
                return ResistantVirus(self.getMaxBirthProb(),self.getClearProb(),babyresist,self.getMutProb())
            else:
                raise NoChildException
            

class TreatedPatient(Patient):
    """
    Representation of a patient. The patient is able to take drugs and his/her
    virus population can acquire resistance to the drugs he/she takes.
    """

    def __init__(self, viruses, maxPop):
        """
        Initialization function, saves the viruses and maxPop parameters as
        attributes. Also initializes the list of drugs being administered
        (which should initially include no drugs).              

        viruses: The list representing the virus population (a list of
        virus instances)

        maxPop: The  maximum virus population for this patient (an integer)
        """

        Patient.__init__(self, viruses, maxPop)
        self.postcondition = []


    def addPrescription(self, newDrug):
        """
        Administer a drug to this patient. After a prescription is added, the
        drug acts on the virus population for all subsequent time steps. If the
        newDrug is already prescribed to this patient, the method has no effect.

        newDrug: The name of the drug to administer to the patient (a string).

        postcondition: The list of drugs being administered to a patient is updated
        """

        if newDrug not in self.postcondition:
            self.postcondition.append(newDrug)


    def getPrescriptions(self):
        """
        Returns the drugs that are being administered to this patient.

        returns: The list of drug names (strings) being administered to this
        patient.
        """

        return self.postcondition


    def getResistPop(self, drugResist):
        """
        Get the population of virus particles resistant to the drugs listed in
        drugResist.       

        drugResist: Which drug resistances to include in the population (a list
        of strings - e.g. ['guttagonol'] or ['guttagonol', 'srinol'])

        returns: The population of viruses (an integer) with resistances to all
        drugs in the drugResist list.
        """

        drugResistSum = 0
        #get each virus object
        for virus in self.getViruses():
            #loop through the drug resistance dictionary of each virus
            virusCheck = True
            #loop through drugresist
            for drug in drugResist:
                #check if drug is in resistance list
                if drug not in virus.getResistances().keys():
                    virusCheck = False
                #check status of drug
                elif virus.getResistances()[drug] == False:
                    virusCheck = False
            if virusCheck == True:
                drugResistSum += 1
        return drugResistSum
                


    def update(self):
        """
        Update the state of the virus population in this patient for a single
        time step. update() should execute these actions in order:

        - Determine whether each virus particle survives and update the list of
          virus particles accordingly

        - The current population density is calculated. This population density
          value is used until the next call to update().

        - Based on this value of population density, determine whether each 
          virus particle should reproduce and add offspring virus particles to 
          the list of viruses in this patient.
          The list of drugs being administered should be accounted for in the
          determination of whether each virus particle reproduces.

        returns: The total virus population at the end of the update (an
        integer)
        """

        if self.getMaxPop() == 0:
            return 0
        #determines whether each particle survives
        removeVirus = []
        for virus in self.getViruses():
            if virus.doesClear() == True:
                removeVirus.append(virus)
        #updates virus list 
        for virus in removeVirus:
            self.viruses.remove(virus)

        #determine virus reproduction
        currentVirusList = self.getViruses()[:]
        for virus in currentVirusList:
            try:
                #calculates current population density
                currentPopDens = self.getTotalPop()/self.getMaxPop()
                #reproduces
                baby = virus.reproduce(currentPopDens,self.getPrescriptions())
                self.viruses.append(baby)
            except NoChildException:
                #Virus failed to reproduce - we dont need to do anything except ignore
                pass

        return self.getTotalPop()


#
# PROBLEM 4
#
def simulationWithDrug(numViruses, maxPop, maxBirthProb, clearProb, resistances,
                       mutProb, numTrials):
    """
    Runs simulations and plots graphs for problem 5.

    For each of numTrials trials, instantiates a patient, runs a simulation for
    150 timesteps, adds guttagonol, and runs the simulation for an additional
    150 timesteps.  At the end plots the average virus population size
    (for both the total virus population and the guttagonol-resistant virus
    population) as a function of time.

    numViruses: number of ResistantVirus to create for patient (an integer)
    maxPop: maximum virus population for patient (an integer)
    maxBirthProb: Maximum reproduction probability (a float between 0-1)        
    clearProb: maximum clearance probability (a float between 0-1)
    resistances: a dictionary of drugs that each ResistantVirus is resistant to
                 (e.g., {'guttagonol': False})
    mutProb: mutation probability for each ResistantVirus particle
             (a float between 0-1). 
    numTrials: number of simulation runs to execute (an integer)
    
    """
    totalAverage = []
    resistAverage = []
    #starts trial
    for i in range(numTrials):
        #create numVirus viruses
        patientViruses = []
        for l in range(numViruses):
            patientViruses.append(ResistantVirus(maxBirthProb,clearProb,resistances,mutProb))
        #create patient
        patient = TreatedPatient(patientViruses,maxPop)
        for j in range(300):
            #add the drug
            if j == 150:
                patient.addPrescription("guttagonol")
            patient.update()
            #find average at each step and add to list
            try:
                totalAverage[j].append(patient.getTotalPop())
            except IndexError:
                totalAverage.append([patient.getTotalPop()])
            #find average at each step for total and resist avg and add to list
            try:
                resistAverage[j].append(patient.getResistPop(["guttagonol"]))
            except IndexError:
                resistAverage.append([patient.getResistPop(["guttagonol"])])

    finaltotal = []
    for numlist in totalAverage:
        finaltotal.append(sum(numlist)/len(numlist))

    finalresist = []
    for numlist in resistAverage:
        finalresist.append(sum(numlist)/len(numlist))   

    #create pylab graph
    x1 = range(300)
    y1 = finaltotal
    pylab.plot(x1,y1, label = "ResistantVirus")
    x2 = range(300)
    y2 = finalresist
    pylab.plot(x2,y2, label = "ResistantVirus with Guttagonol")
    pylab.xlabel("Time Steps")
    pylab.ylabel("Average Virus Population")
    pylab.title("SimpleVirus simulation")
    pylab.legend(loc = "best")
    pylab.show()
    print(finalresist)




simulationWithDrug(1, 10, 1.0, 0.0, {}, 1.0, 5)