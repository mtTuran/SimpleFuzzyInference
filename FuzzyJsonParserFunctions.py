from FuzzyInputVariable import FuzzyInputVariable
from FuzzyOutputVariable import FuzzyOutputVariable
from FuzzyRule import FuzzyRule

def parse_vars_util(json_dict, variable_type):
    all_vars = dict()
    vars_dict_list = json_dict[variable_type]
    for variable in vars_dict_list:
        var_name = variable["var_name"]
        x_range = tuple(variable["x_range"])
        if variable_type == "InputSets":
            new_fuzzy_var = FuzzyInputVariable(var_name, x_range)
        else:
            new_fuzzy_var = FuzzyOutputVariable(var_name, x_range)

        for set in variable["sets"]:
            set_name = set["set_name"]
            set_type = set["set_type"]
            set_min_x = set["set_min_x"]
            set_max_x = set["set_max_x"]
            if set_type == "trapezoid":
                set_flatness_start_x = set["set_flatness_start_x"]
                set_flatness_end_x = set["set_flatness_end_x"]
                new_fuzzy_var.add_trapezoid_membership_set(set_name, set_min_x, set_max_x, set_flatness_start_x, set_flatness_end_x)
            else:
                set_peak_x = set["set_peak_x"]
                new_fuzzy_var.add_triangular_membership_set(set_name, set_min_x, set_peak_x, set_max_x)

        all_vars[var_name] = new_fuzzy_var

    return all_vars
 

def parse_input_vars(json_dict):
    all_input_vars = parse_vars_util(json_dict, "InputSets")
    return all_input_vars


def parse_output_vars(json_dict):
    all_output_vars = parse_vars_util(json_dict, "OutputSets")
    return all_output_vars


def parse_rules_util(json_dict, rule_type):
    new_rules_list = []
    rules_to_be_parsed = json_dict[rule_type]

    output_variable_name = rules_to_be_parsed["output_variable_name"]
    for rule in rules_to_be_parsed["Rules"]:
        aggregation_set_name = rule["aggregation_set_name"]
        new_rule = FuzzyRule(output_variable_name, aggregation_set_name)
        for condition in rule["conditions"]:
            input_variable_name = condition["input_variable_name"]
            monotonic_selection_set_name = condition["monotonic_selection_set_name"]
            new_rule.add_condition(input_variable_name, monotonic_selection_set_name)

        priority = rule.get("priority", new_rule.get_number_of_conditions())
        new_rule.set_priority(priority)
        new_rules_list.append(new_rule)

    return new_rules_list


def parse_rules(json_dict):
    all_rules = dict()
    all_rules["HouseRules"] = parse_rules_util(json_dict, "HouseRules")
    all_rules["ApplicationRules"] = parse_rules_util(json_dict, "ApplicationRules")
    all_rules["LoanRules"] = parse_rules_util(json_dict, "LoanRules")
    return all_rules
