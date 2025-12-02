from FuzzyInputVariable import FuzzyInputVariable
from FuzzyOutputVariable import FuzzyOutputVariable

if __name__ == '__main__':
    '''
    test_input_var = FuzzyInputVariable("test_input_var")
    test_input_var.add_trapezoid_membership_set("kucuk", 0, 20, 5, 12)
    test_input_var.add_triangular_membership_set("orta", 17, 22, 30)
    test_input_var.fuzzify(18)
    print(test_input_var.get_memberships())
    '''
    test_out_var = FuzzyOutputVariable("test_output_var", (0, 100))
    test_out_var.add_trapezoid_membership_set("kucuk", 0, 30, 0, 20)
    test_out_var.add_trapezoid_membership_set("orta", 25, 65, 30, 60)
    test_out_var.add_trapezoid_membership_set("buyuk", 60, 100, 70, 100)

    test_out_var.clip_membership_set("kucuk", 0.1)
    test_out_var.clip_membership_set("orta", 0.2)
    test_out_var.clip_membership_set("buyuk", 0.5)

    test_out_var.aggregate_outputs()
    result = test_out_var.defuzzify()
    print(result)