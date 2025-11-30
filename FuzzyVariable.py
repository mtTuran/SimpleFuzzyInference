class FuzzyVariable:
    def __init__(self, var_name):
        self.var_name = var_name
        self.membership_sets = []
        self.memberships = dict()

    def add_trapezoid_membership_set(self, set_name, set_min_x, set_max_x, set_flatness_start_x, set_flatness_end_x):
        def _membership(crisp_input):
            if crisp_input < set_min_x or crisp_input > set_max_x:
                return 0
            elif crisp_input < set_flatness_start_x:
                denominator = set_flatness_start_x - set_min_x
                return (crisp_input - set_min_x) / denominator       
            elif crisp_input > set_flatness_end_x:
                denominator = set_flatness_end_x - set_max_x
                return (crisp_input - set_max_x) / denominator
            else:
                return 1 
        self.membership_sets.append([set_name, _membership])
    
    def add_triangular_membership_set(self, set_name, set_min_x, set_peak_x, set_max_x):
        def _membership(crisp_input):
            if crisp_input < set_min_x or crisp_input > set_max_x:
                return 0
            elif crisp_input < set_peak_x:
                denominator = set_peak_x - set_min_x
                return (crisp_input - set_min_x) / denominator 
            elif crisp_input > set_peak_x:
                denominator = set_peak_x - set_max_x
                return (crisp_input - set_max_x) / denominator
            else:
                return 1 
        self.membership_sets.append([set_name, _membership])

    def get_memberships(self):
        if len(self.memberships) == 0:
            print("No fuzzified input available!")
            return [-1]
        return self.memberships
    