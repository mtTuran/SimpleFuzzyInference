class FuzzyVariable:
    """
    Represents a fuzzy variable with a defined universe of discourse (x_range).
    It supports multiple membership sets (Trapezoidal, Triangular).
    """

    # Class-level dictionary to keep track of all variables
    variables = {}

    def __init__(self, var_name, x_range):
        self.var_name = var_name
        self.x_range = x_range
        self.membership_sets = []
        
        # Register this instance to the static dictionary
        FuzzyVariable.variables[var_name] = self

    def get_name(self):
        return self.var_name
    
    def get_range(self):
        return self.x_range

    def add_trapezoid_membership_set(self, set_name, set_min_x, set_max_x, set_flatness_start_x, set_flatness_end_x):
        """
        Adds a trapezoidal set defined by 4 points: start, top-left, top-right, and end.
        """
        # Validate that the set falls within the variable's global range
        if set_min_x < self.x_range[0] or set_max_x > self.x_range[1]:
            print(f"The provided set is out of bounds for the pre-defined universe of discourse: {self.x_range}")
            return  
        
        def _membership(crisp_input):
            # Outside the support area
            if crisp_input < set_min_x or crisp_input > set_max_x:
                return 0
            
            # Rising edge (slope up)
            elif crisp_input < set_flatness_start_x:
                denominator = set_flatness_start_x - set_min_x
                return (crisp_input - set_min_x) / denominator       
            
            # Falling edge (slope down)
            elif crisp_input > set_flatness_end_x:
                denominator = set_flatness_end_x - set_max_x
                # Note: Denominator is negative here, creating the downward slope logic
                return (crisp_input - set_max_x) / denominator
            
            # Flat top (membership is 1.0)
            else:
                return 1 

        self.membership_sets.append([
            (set_name, set_min_x, set_max_x, set_flatness_start_x, set_flatness_end_x), 
            _membership
        ])
    
    def add_triangular_membership_set(self, set_name, set_min_x, set_peak_x, set_max_x):
        """
        Adds a triangular set defined by 3 points: start, peak, and end.
        """
        if set_min_x < self.x_range[0] or set_max_x > self.x_range[1]:
            print(f"The provided set is out of bounds for the pre-defined universe of discourse: {self.x_range}")
            return    

        def _membership(crisp_input):
            if crisp_input < set_min_x or crisp_input > set_max_x:
                return 0
            
            # Rising edge
            elif crisp_input < set_peak_x:
                denominator = set_peak_x - set_min_x
                return (crisp_input - set_min_x) / denominator 
            
            # Falling edge
            elif crisp_input > set_peak_x:
                denominator = set_peak_x - set_max_x
                return (crisp_input - set_max_x) / denominator
            
            # Peak point
            else:
                return 1 

        self.membership_sets.append([(set_name, set_min_x, set_peak_x, set_max_x), _membership])

    def compute_membership(self, crisp_input):
        """
        Calculates membership values for a given crisp input across all defined sets.
        """
        crisp_to_membership = {}
        
        if not self.membership_sets:
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
    