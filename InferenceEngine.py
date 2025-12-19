from FuzzyInputVariable import FuzzyInputVariable
from FuzzyJsonParserFunctions import parse_input_vars, parse_output_vars, parse_rules, sort_rule_types_by_priority_util, sort_output_vars_by_rule_types_util

class InferenceEngine:
    """
    The core engine that orchestrates the fuzzy inference process.
    It manages inputs, outputs, rules, and the execution flow (fuzzification -> inference -> defuzzification).
    """

    def __init__(self, json_dict):
        self.input_vars = parse_input_vars(json_dict)
        self.output_vars = parse_output_vars(json_dict)
        self.rules = parse_rules(json_dict)
        self.execution_trace = []

        # Initialize 'Derived' variables. 
        # These are used for multi-stage inference where the output of one stage 
        # becomes the input of the next stage.
        for var_name, out_var in self.output_vars.items():
            derived_variable = FuzzyInputVariable("computed_" + var_name, out_var.get_range())
            self.input_vars[derived_variable.get_name()] = derived_variable

        # Determine the execution order based on dependencies
        self.ordered_rule_type_names = sort_rule_types_by_priority_util(json_dict, self.rules)
        self.ordered_output_var_names = sort_output_vars_by_rule_types_util(json_dict, self.ordered_rule_type_names)

    def __call__(self, args_dict):
        """
        Main execution method. 
        Args:
            args_dict: A dictionary containing crisp input values {var_name: value}
        """
        result_dict = {}

        # 1. Reset state from previous runs
        self.clean_old_computations()

        # 2. Fuzzify the initial raw inputs
        for var_name, var_arg in args_dict.items():
            var = self.input_vars.get(var_name, None)
            
            if var is None:
                print(f"An argument for a non-existing input variable '{var_name}' was provided!")
                return None
            
            if var_arg is None:
                continue
            
            var.fuzzify(var_arg)

        # 3. Process rules in the defined order (Sequential Inference)
        # This loop handles the cascading logic: Output of Step N -> Input of Step N+1
        for rule_type, out_var_name in zip(self.ordered_rule_type_names, self.ordered_output_var_names):
            
            applicable_rules = self.get_applicable_rules_by_priority(rule_type)
            
            if applicable_rules:
                # Calculate rule strengths and apply clipping (Implication)
                fired_rules = self.apply_rules(rule_type, applicable_rules)
                self.execution_trace.extend(fired_rules)
                
                # Combine results and convert back to a crisp number (Aggregation & Defuzzification)
                # 'derive=True' ensures this result is fed back as an input for the next loop iteration
                crisp_result = self.aggregate_and_defuzzify(out_var_name, derive=True)
            else:
                crisp_result = None
            
            result_dict[out_var_name] = crisp_result
            
        return result_dict
  
    def get_applicable_rules_by_priority(self, rule_type): 
        """
        Filters rules that have valid inputs ready and sorts them by priority.
        """
        applicable_rules = [
            rule_index for rule_index in range(len(self.rules[rule_type])) 
            if self.rules[rule_type][rule_index].is_applicable()
        ]
        # Sort rules: Higher priority rules first
        applicable_rules.sort(reverse=True, key=lambda name: self.rules[rule_type][name].get_priority())
        return applicable_rules

    def apply_rules(self, rule_type, applicable_rules):
        """
        Evaluates the IF part of the rules and clips the THEN part (Output sets).
        """
        fired_in_this_step = []
        
        for rule_index in applicable_rules:
            rule = self.rules[rule_type][rule_index]
            
            # rule() calls the __call__ method of FuzzyRule to get min_eval (strength)
            clip_level = rule()
            
            if clip_level > 0:
                out_var_name, out_agg_name = rule.get_aggregation_information()
                out_var = self.output_vars[out_var_name]
                
                # Update the output set's maximum active region (clipping)
                out_var.clip_membership_set(out_agg_name, clip_level)
                
                fired_in_this_step.append({
                    "rule_type": rule_type,
                    "logic": str(rule),
                    "strength": round(clip_level, 4)
                })
                
        return fired_in_this_step

    def aggregate_and_defuzzify(self, output_var_name, derive=True):
        """
        Combines clipped sets, calculates the centroid, and optionally 
        feeds the result back into the system as a new input.
        """
        var = self.output_vars[output_var_name]
        
        # Merge all clipped sets into one shape
        var.aggregate_outputs()
        
        # Calculate crisp value (Center of Gravity)
        crisp_result = var.defuzzify()
        
        # Feedback loop logic:
        # If this output is needed for a future rule, create a "computed" input variable for it.
        if derive:
            derived_variable = self.input_vars["computed_" + var.get_name()]
            
            # Copy membership definitions from Output var to Input var 
            # so the system understands the fuzzy sets of this intermediate value.
            param_tuples = var.get_membership_sets_params()
            for params in param_tuples:
                if len(params) == 5:
                    derived_variable.add_trapezoid_membership_set(*params)
                else:
                    derived_variable.add_triangular_membership_set(*params)
            
            # Immediately fuzzify the result so it's ready for the next iteration in __call__
            if crisp_result is not None:
                derived_variable.fuzzify(crisp_result)
                
        return crisp_result

    def clean_old_computations(self):
        """Resets all variables and traces for a fresh inference run."""
        for _, var in self.input_vars.items():
            var.clean_memberships()
            
        for _, var in self.output_vars.items():
            var.clean_aggregated_memberships()
            var.clean_clip_levels()
            
        self.execution_trace = []

    def get_execution_trace(self):
        return self.execution_trace
    