from FuzzyVariable import FuzzyVariable

class FuzzyInputVariable(FuzzyVariable):
    """
    Represents an input variable in the fuzzy system.
    It handles the fuzzification process of a crisp input.
    """
    def __init__(self, var_name, x_range):
        super().__init__(var_name, x_range)
        self.memberships = {}

    def fuzzify(self, crisp_input):
        """
        Takes a crisp input value and computes membership values 
        for all sets defined in this variable.
        """
        # Clear previous values before new fuzzification
        if self.memberships:
            self.memberships.clear()
        
        crisp_to_membership = self.compute_membership(crisp_input)
        
        if not crisp_to_membership:
            print("Fuzzification failed!")
            return
            
        # Store new membership values
        for set_name, membership in crisp_to_membership.items():
            self.memberships[set_name] = membership
        
    def get_memberships(self):
        if not self.is_applicable():
            print("No fuzzification is performed!")
            return None
        return self.memberships
    
    def clean_memberships(self):
        self.memberships.clear()

    def is_applicable(self):
        """Returns True if the variable has currently valid membership values."""
        return len(self.memberships) > 0
    