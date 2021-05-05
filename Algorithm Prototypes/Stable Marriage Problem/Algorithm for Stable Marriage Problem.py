class Woman:
    def __init__(self, name):
        self.name = name
        self.current_man = 0
    
    def set_ranking(self, ranking_men):
        self.ranking_men = ranking_men
        
    def get_proposal(self, man):
        if self.current_man:
            if self.ranking_men.index(man) < self.ranking_men.index(self.current_man):
                self.current_man.get_declination()
                print("'->", self.name, "declines to", self.current_man.name)
                self.current_man = man
                print("'->", self.name, "accepts")
                return True
            else:
                print("'->", self.name, "declines")
                return False
        else:
            self.current_man = man
            print("'->", self.name, "accepts")
            return True
    
    def marry(self):
        print(self.name, "is now married to", self.current_man.name)
        
class Man:
    def __init__(self, name):
        self.name = name
        self.current_woman = 0
    
    def set_ranking(self, original_ranking_women, ranking_women):
        self.original_ranking_women = original_ranking_women
        self.ranking_women = ranking_women
    
    def propose(self):
        if not self.current_woman:
            print(self.name, "proposes to", self.ranking_women[0].name)
            if self.ranking_women[0].get_proposal(self):
                self.current_woman = self.ranking_women[0]
            else:
                self.ranking_women.pop(0)
                self.current_woman = 0
        
    def get_declination(self):
        self.ranking_women.pop(0)
        self.current_woman = 0
    
    def marry(self):
        if self.current_woman:
            print(self.name, "is now married to", self.current_woman.name)
        else:
            print(self.name, "is not married")

def check_finished():    
    for man in men:
        if not man.current_woman:
            return False
    
    for woman in women:
        if not woman.current_man:
            return False
    
    return True

def ckeck_solution():
    for man in men:
        for woman in women:
            if man.original_ranking_women.index(woman) < man.original_ranking_women.index(man.current_woman) and woman.ranking_men.index(man) < woman.ranking_men.index(woman.current_man):
                return "The marriages are not stable"
    return "The marriages are stable"
    
A = Man("A")
B = Man("B")
C = Man("C")

X = Woman("X")
Y = Woman("Y")
Z = Woman("Z")

men = [A, B, C]
women = [X, Y, Z]

A.set_ranking([Y, X, Z], [Y, X, Z])
B.set_ranking([Y, Z, X], [Y, Z, X])
C.set_ranking([X, Z, Y], [X, Z, Y])

X.set_ranking([B, A, C])
Y.set_ranking([C, B, A])
Z.set_ranking([B, C, A])

while check_finished() == False:
    for man in men:
        man.propose()

for man in men:
    man.marry()

print(ckeck_solution())