from FuzzyInputVariable import FuzzyInputVariable
from FuzzyJsonParserFunctions import parse_input_vars, parse_output_vars, parse_rules, sort_rule_types_by_priority_util, sort_output_vars_by_rule_types_util

class InferenceEngine:
    def __init__(self, json_dict):
        self.input_vars = parse_input_vars(json_dict)
        self.output_vars = parse_output_vars(json_dict)
        self.rules = parse_rules(json_dict)

        for var_name, out_var in self.output_vars.items():
            derived_variable = FuzzyInputVariable("computed_" + var_name, out_var.get_range())
            self.input_vars[derived_variable.get_name()] = derived_variable

        self.ordered_rule_type_names = sort_rule_types_by_priority_util(json_dict, self.rules)
        self.ordered_output_var_names = sort_output_vars_by_rule_types_util(json_dict, self.ordered_rule_type_names)

    def __call__(self, args_dict):
        result_dict = dict()

        # clean the computations made during the previous call
        self.clean_old_computations()

        # fuzzify the provided inputs
        for var_name, var_arg in args_dict.items():
            var = self.input_vars.get(var_name, None)
            if var is None:
                print(f"An argument for a non-existing input variable '{var_name}' was provided!")
                return None
            if var_arg is None:
                continue
            var.fuzzify(var_arg)

        # appyly, aggregate, defuzzify rules ordered by first rule type and rule priority
        for rule_type, out_var_name in zip(self.ordered_rule_type_names, self.ordered_output_var_names):
            applicable_rules = self.get_applicable_rules_by_priority(rule_type)
            if len(applicable_rules) != 0:
                self.apply_rules(rule_type, applicable_rules)
                crisp_result = self.aggregate_and_defuzzify(out_var_name, derive=True)
            else:
                crisp_result = None
            result_dict[out_var_name] = crisp_result
        return result_dict
  
    def get_applicable_rules_by_priority(self, rule_type): 
        applicable_rules = [rule_index for rule_index in range(len(self.rules[rule_type])) if self.rules[rule_type][rule_index].is_applicable()]
        applicable_rules.sort(reverse=True, key=lambda name: self.rules[rule_type][name].get_priority())
        return applicable_rules

    def apply_rules(self, rule_type, applicable_rules):
        for rule_index in applicable_rules:
            rule = self.rules[rule_type][rule_index]
            clip_level = rule()
            out_var_name, out_agg_name = rule.get_aggregation_information()
            out_var = self.output_vars[out_var_name]
            out_var.clip_membership_set(out_agg_name, clip_level)

    def aggregate_and_defuzzify(self, output_var_name, derive=True):
        var = self.output_vars[output_var_name]
        var.aggregate_outputs()
        crisp_result = var.defuzzify()
        if derive:
            derived_variable = self.input_vars["computed_" + var.get_name()]
            param_tuples = var.get_membership_sets_params()
            for params in param_tuples:
                if len(params) == 5:
                    derived_variable.add_trapezoid_membership_set(*params)
                else:
                    derived_variable.add_triangular_membership_set(*params)
            if crisp_result is not None:
                derived_variable.fuzzify(crisp_result)
        return crisp_result

    def clean_old_computations(self):
        for _, var in self.input_vars.items():
            var.clean_memberships()
        for _, var in self.output_vars.items():
            var.clean_aggregated_memberships()
            var.clean_clip_levels()

        