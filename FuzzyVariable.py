class FuzzyVariable:

    variables = dict()

    def __init__(self, var_name, x_range):
        self.var_name = var_name
        self.x_range = x_range
        self.membership_sets = []
        FuzzyVariable.variables[var_name] = self

    def get_name(self):
        return self.var_name
    
    def get_range(self):
        return self.x_range

    def add_trapezoid_membership_set(self, set_name, set_min_x, set_max_x, set_flatness_start_x, set_flatness_end_x):
        if set_min_x < self.x_range[0] or set_max_x > self.x_range[1]:
            print(f"The provided set is out of bounds for the pre-defined universe of discourse: {self.x_range}")
            return  
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
        self.membership_sets.append([(set_name, set_min_x, set_max_x, set_flatness_start_x, set_flatness_end_x), _membership])
    
    def add_triangular_membership_set(self, set_name, set_min_x, set_peak_x, set_max_x):
        if set_min_x < self.x_range[0] or set_max_x > self.x_range[1]:
            print(f"The provided set is out of bounds for the pre-defined universe of discourse: {self.x_range}")
            return    
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
        self.membership_sets.append([(set_name, set_min_x, set_peak_x, set_max_x), _membership])

    def compute_membership(self, crisp_input):
        crisp_to_membership = dict()
        if len(self.membership_sets) == 0:
            print("No membership set is defined!")
            return crisp_to_membership
        for params, mem_func in self.membership_sets:
            set_name = params[0]
            crisp_to_membership[set_name] = mem_func(crisp_input)
        return crisp_to_membership
    
    def get_membership_sets_params(self):
        return [params for params, _ in self.membership_sets]
    
    @staticmethod
    def get_variable_by_name(var_name):
        return FuzzyVariable.variables.get(var_name, None)
    