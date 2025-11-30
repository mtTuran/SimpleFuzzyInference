from FuzzyInputVariable import FuzzyInputVariable
from FuzzyOutputVariable import FuzzyOutputVariable

if __name__ == '__main__':
    test_input_var = FuzzyInputVariable("test_input_var")
    test_input_var.add_trapezoid_membership_set("kucuk", 0, 20, 5, 12)
    test_input_var.add_triangular_membership_set("orta", 17, 22, 30)
    test_input_var.fuzzify(18)
    print(test_input_var.get_memberships())