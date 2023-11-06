# Définition du système de transition fini ST
class FiniteTransitionSystem:
    def __init__(self, states, initial_states, transition_function):
        self.states = states
        self.initial_states = initial_states
        self.transition_function = transition_function

    # Définition d'une méthode permettant de vérifier que l'invariant (PHI) est validé par le système de transition
    def invariant_checking(self, PHI):
        self.R = set()
        self.U = []
        self.b = True
        self.PHI = PHI
        
        while (self.initial_states - self.R) and self.b:    # Effectuer le balayage sur tous les états initiaux en trouvant qu'un état invalide l'invariant ou que tous les états le valident
            s = next(iter(self.initial_states - self.R))    # Choisir arbitrairement un état initial qui n'est pas dans R
            self.visite(s)
        if self.b:
            return "oui"    # ST satisfait toujours PHI
        else:
            return ("non", self.U)  # La pile U fournit un contre-exemple

    # Définition d'une méthode permettant de balayer les états accessibles depuis l'état courant (s), et de vérifier si un de ces états ne valide pas l'invariant (PHI)
    def visite(self, s):
        self.U.append(s)    # On empile s sur la pile U
        self.R.add(s)   # On marque s comme accessible
    
        while self.U and self.b:    # Effectuer le balayage sur l'état courant et sur tous les états accessible depuis celui ci, en trouvant qu'un état invalide l'invariant ou que tous les états le valident
            s_prime = self.U[-1]    # s' est le premier élément de la pile
            
            if self.post(s_prime).issubset(self.R):
                self.U.pop()
                self.b = self.b and self.PHI.check(s_prime) # s' vérifie PHI
            else:
                s_double_prime = next(iter(self.post(s_prime) - self.R))    # Choisir arbitrairement un état accessible depuis s' qui n'est pas dans R
                self.U.append(s_double_prime)   # s'' est un nouvel état accessible
                self.R.add(s_double_prime)
    
    # Définition d'une méthode permettant de récupéré l'ensemble des états accessibles depuis l'état courant (state)
    def post(self, state):
        return set(self.transition_function[state])

# Définition d'une proposition logique PHI
class LogicalProposition:
    def __init__(self, predicate):
        self.predicate = predicate
    
    def check(self, state):
        return self.predicate(state)
        
# Exemple 1 modélisant un sémaphore binaire avec la propriété d'exclusion mutuelle
def exemple1():
    states = {'n1,n2', 'p1,n2', 'n1,p2', 'p1,p2', 'c1,n2', 'n1,c2', 'c1,p2', 'p1,c2'}
    initial_states = {'n1,n2'}
    transition_function = {
        'n1,n2': ['p1,n2', 'n1,p2'],
        'p1,n2': ['c1,n2', 'p1,p2'],
        'n1,p2': ['n1,c2', 'p1,p2'],
        'p1,p2': ['c1,p2', 'p1,c2'],
        'c1,p2': ['n1,p2'],
        'p1,c2': ['p1,n2'],
        'c1,n2': ['c1,p2','n1,n2'],
        'n1,c2': ['p1,c2','n1,n2']
    }
    
    ST = FiniteTransitionSystem(states, initial_states, transition_function)
    PHI = LogicalProposition(lambda state: state != 'c1,c2')
    
    result = ST.invariant_checking(PHI)
    
    if result == "oui":
        print("ST satisfait toujours PHI.")
    else:
        print("ST ne satisfait pas PHI. Contre-exemple :", result[1])

# Exemple 2 modélisant un système de deux feux tricolores
def exemple2():
    states = {'r1,v2', 'r1,o2', 'r1,r2', 'o1,r2', 'v1,r2', 'o1,v2', 'o1,o2', 'v1,o2', 'v1,v2'}
    initial_states = {'r1,r2'}
    transition_function = {
        'r1,v2': ['r1,o2'],
        'r1,o2': ['r1,r2'],
        'r1,r2': ['r1,v2', 'v1,r2'],
        'o1,r2': ['r1,r2'],
        'v1,r2': ['o1,r2'],
        'o1,v2': ['r1,v2', 'o1,o2'],
        'o1,o2': ['r1,o2', 'o1,r2'],
        'v1,o2': ['o1,o2', 'v1,r2'],
        'v1,v2': ['o1,v2', 'v1,o2']
    }
    
    ST = FiniteTransitionSystem(states, initial_states, transition_function)
    PHI = LogicalProposition(lambda state: state != 'o1,v2' and state != 'o1,o2' and state != 'v1,o2' and state != 'v1,v2')
   
    result = ST.invariant_checking(PHI)
    
    if result == "oui":
        print("ST satisfait toujours PHI.")
    else:
        print("ST ne satisfait pas PHI. Contre-exemple :", result[1])

# Fonction principale     
if __name__ == "__main__":
    exemple1()
    exemple2()