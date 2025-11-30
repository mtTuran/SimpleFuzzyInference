from FuzzyVariable import FuzzyVariable


class FuzzyOutputVariable(FuzzyVariable):
    def __init__(self, var_name):
        super().__init__(var_name)
        self.membership_clips = []

    