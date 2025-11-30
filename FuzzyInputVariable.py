from FuzzyVariable import FuzzyVariable

class FuzzyInputVariable(FuzzyVariable):
    def __init__(self, var_name):
        super().__init__(var_name)

    def fuzzify(self, crisp_input):
        if len(self.membership_sets) == 0:
            print("No membership set is defined!")
            return -1
        for set_name, mem_func in self.membership_sets:
            self.memberships[set_name] = mem_func(crisp_input)

        