from FuzzyVariable import FuzzyVariable

class FuzzyInputVariable(FuzzyVariable):
    def __init__(self, var_name, x_range):
        super().__init__(var_name, x_range)
        self.memberships = dict()

    def fuzzify(self, crisp_input):
        if self.memberships.keys():
            self.memberships.clear()
        crisp_to_membership = self.compute_membership(crisp_input)
        if len(crisp_to_membership) == 0:
            print("Fuzzification failed!")
            return
        for set_name, membership in crisp_to_membership.items():
            self.memberships[set_name] = membership
        return self.get_memberships()
        
    def get_memberships(self):
        if len(self.memberships) == 0:
            print("No fuzzified input available!")
            return None
        return self.memberships
    
    def clean_memberships(self):
        self.memberships.clear()

        