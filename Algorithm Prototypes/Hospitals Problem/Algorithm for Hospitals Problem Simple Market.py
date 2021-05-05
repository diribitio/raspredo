class Hospital: 
    def __init__(self, name):
        self.name = name
        self.current_applicants = []
        self.max_applicants = 3
    
    def set_ranking(self, ranking_applicants):
        self.ranking_applicants = ranking_applicants
        
    def get_application(self, new_applicant):
        if len(self.current_applicants) >= self.max_applicants:
            for applicant in self.current_applicants:
                if self.ranking_applicants.index(new_applicant) < self.ranking_applicants.index(applicant):
                    applicant.get_declination()
                    self.current_applicants.remove(applicant)
                    print("'->", self.name, "declines to", applicant.name)
                    self.current_applicants.append(new_applicant)
                    print("'->", self.name, "accepts")
                    return True
            print("'->", self.name, "declines")
            return False
        else:
            self.current_applicants.append(new_applicant)
            print("'->", self.name, "accepts")
            return True
    
    def get_current_applicants(self):
        current_appicants_names = ""
        
        for current_applicant in self.current_applicants:
            current_appicants_names += current_applicant.name + " | "
        
        return current_appicants_names
    
    def match(self):
        print(self.name, "has", len(self.current_applicants), "out of", self.max_applicants, "applicants: |", self.get_current_applicants())
        
class Applicant:
    def __init__(self, name):
        self.name = name
        self.current_hospital = 0
    
    def set_ranking(self, original_ranking_hospitals, ranking_hospitals):
        self.original_ranking_hospitals = original_ranking_hospitals
        self.ranking_hospitals = ranking_hospitals
    
    def apply(self):
        if not self.current_hospital:
            print(self.name, "applies to", self.ranking_hospitals[0].name)
            if self.ranking_hospitals[0].get_application(self):
                self.current_hospital = self.ranking_hospitals[0]
            else:
                self.ranking_hospitals.pop(0)
                self.current_hospital = 0
        
    def get_declination(self):
        self.ranking_hospitals.pop(0)
        self.current_hospital = 0
    
    def match(self):
        print(self.name, self.current_hospital.name)

def check_finished():
    free_applicants = False
    free_hospitals = False

    for applicant in applicants:
        if not applicant.current_hospital:
            free_applicants = True
    
    for hospital in hospitals:
        if len(hospital.current_applicants) < hospital.max_applicants:
            free_hospitals = True
    
    if free_applicants and free_hospitals:
        return False
    else:
        return True

def ckeck_solution():
    for applicant in applicants:
        for hospital in hospitals:
            for current_applicant in hospital.current_applicants:
                if applicant.original_ranking_hospitals.index(hospital) < applicant.original_ranking_hospitals.index(applicant.current_hospital) and hospital.ranking_applicants.index(applicant) < hospital.ranking_applicants.index(current_applicant):
                    return "The matches are not stable"
    return "The matches are stable"
    
A = Applicant("A")
B = Applicant("B")
C = Applicant("C")
D = Applicant("D")
E = Applicant("E")
F = Applicant("F")

X = Hospital("X")
Y = Hospital("Y")
Z = Hospital("Z")

applicants = [A, B, C, D, E, F]
hospitals = [X, Y, Z]

A.set_ranking([Y, X, Z], [Y, X, Z])
B.set_ranking([Z, Y, X], [Z, Y, X])
C.set_ranking([X, Z, Y], [X, Z, Y])
D.set_ranking([Y, X, Z], [Y, X, Z])
E.set_ranking([Y, Z, X], [Y, Z, X])
F.set_ranking([X, Z, Y], [X, Z, Y])

X.set_ranking([B, A, C, D, F, E])
Y.set_ranking([C, B, A, F, E, D])
Z.set_ranking([E, F, A, C, D, B])

while check_finished() == False:
    for applicant in applicants:
        applicant.apply()

for hospital in hospitals:
    hospital.match()

print(ckeck_solution())