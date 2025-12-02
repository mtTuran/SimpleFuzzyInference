from FuzzyVariable import FuzzyVariable

class FuzzyOutputVariable(FuzzyVariable):
    def __init__(self, var_name, x_range):
        super().__init__(var_name, x_range)
        self.membership_clips = dict()
        self.aggregated_memberships = []

    def add_trapezoid_membership_set(self, set_name, set_min_x, set_max_x, set_flatness_start_x, set_flatness_end_x):
        super().add_trapezoid_membership_set(set_name, set_min_x, set_max_x, set_flatness_start_x, set_flatness_end_x)
        self.membership_clips[set_name] = 0

    def add_triangular_membership_set(self, set_name, set_min_x, set_peak_x, set_max_x):
        super().add_triangular_membership_set(set_name, set_min_x, set_peak_x, set_max_x)
        self.membership_clips[set_name] = 0

    def clip_membership_set(self, set_name, clip_level):
        self.membership_clips[set_name] = clip_level

    def aggregate_outputs(self):
        for x in range(self.x_range[0], self.x_range[1] + 1, 1):
            memberships = self.compute_membership(x)
            upper_bound_set = max(memberships, key=lambda key: min(memberships[key], self.membership_clips[key]))
            clipped_membership = min(memberships[upper_bound_set], self.membership_clips[upper_bound_set])
            self.aggregated_memberships.append(clipped_membership)

    def defuzzify(self):
        if len(self.aggregated_memberships) == 0:
            print("Rule evaluations are not aggregated!")
            return None
        nominator = 0
        denominator = 0.000001
        for membership, x in zip(*[self.aggregated_memberships, range(self.x_range[0], self.x_range[1] + 1, 1)]):
            nominator = nominator + (membership * x)
            denominator = denominator + membership
        center_of_gravity = nominator / denominator
        return center_of_gravity

    def clean_aggregated_memberships(self):
        self.aggregated_memberships.clear()

    def clean_clip_levels(self):
        self.membership_clips.clear()
    