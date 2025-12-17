from FuzzyVariable import FuzzyVariable

class FuzzyRule:
    def __init__(self, output_variable_name, aggregation_set_name, priority=1):
        self.output_variable_name = output_variable_name
        self.aggregation_set_name = aggregation_set_name
        self.priority = priority
        self.conditions = dict()

    def set_priority(self, priority):
        self.priority = priority

    def get_priority(self):
        return self.priority

    def get_number_of_conditions(self):
        return len(self.conditions.keys())

    def get_aggregation_information(self):
        return self.output_variable_name, self.aggregation_set_name

    def add_condition(self, input_variable_name, monotonic_selection_set_name):
        self.conditions[input_variable_name] = monotonic_selection_set_name

    def is_applicable(self):
        for var_name, _ in self.conditions.items():
            var = FuzzyVariable.get_variable_by_name(var_name)
            if not var.is_applicable():
                return False
        return True

    def __call__(self):
        min_eval = 1
        for var_name, selection_set in self.conditions.items():
            var = FuzzyVariable.get_variable_by_name(var_name)
            if var is None:
                print(f"A non-existing condition variable has been provided: {var_name}")
                exit(-1)
            if not var.is_applicable():
                print(f"Input for the {var_name} variable was not fuzzified!")
                exit(-1)
            memberships = var.get_memberships()
            condition_selection = memberships.get(selection_set, None)
            if condition_selection is None:
                print(f"Provided '{selection_set}' set has not been created for the variable '{var_name}'!")
                exit(-1)
            min_eval = min(min_eval, condition_selection)
        return min_eval
    
    def __str__(self):
        if_part = " AND ".join([f"{var} IS {s_set}" for var, s_set in self.conditions.items()])
        return f"IF {if_part} THEN {self.output_variable_name} IS {self.aggregation_set_name}"
