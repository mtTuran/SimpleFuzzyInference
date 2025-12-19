from FuzzyVariable import FuzzyVariable

class FuzzyOutputVariable(FuzzyVariable):
    """
    Represents an output variable. It handles rule implication (clipping),
    aggregation of resulting sets, and defuzzification.
    """
    def __init__(self, var_name, x_range):
        super().__init__(var_name, x_range)
        self.membership_clips = {}
        self.aggregated_memberships = []

    def add_trapezoid_membership_set(self, set_name, set_min_x, set_max_x, set_flatness_start_x, set_flatness_end_x):
        super().add_trapezoid_membership_set(set_name, set_min_x, set_max_x, set_flatness_start_x, set_flatness_end_x)
        # Initialize clip level to 0 for the new set
        self.membership_clips[set_name] = 0

    def add_triangular_membership_set(self, set_name, set_min_x, set_peak_x, set_max_x):
        super().add_triangular_membership_set(set_name, set_min_x, set_peak_x, set_max_x)
        self.membership_clips[set_name] = 0

    def clip_membership_set(self, set_name, clip_level):
        """
        Updates the activation level (clip) for a specific set.
        Uses MAX to ensure that if multiple rules trigger the same output set, 
        the strongest rule dominates.
        """
        self.membership_clips[set_name] = max(clip_level, self.membership_clips[set_name])

    def aggregate_outputs(self):
        """
        Constructs the final aggregated fuzzy shape by iterating through
        the universe of discourse (x_range) and applying the clip levels.
        """
        # Step size is 1 (discrete integration)
        for x in range(self.x_range[0], self.x_range[1] + 1, 1):
            memberships = self.compute_membership(x)
            
            # Find the membership set that yields the highest value at point x after clipping.
            # This effectively computes the Union (OR) of all active output sets.
            upper_bound_set = max(
                memberships, 
                key=lambda key: min(memberships[key], self.membership_clips[key])
            )
            
            # The value at x is limited by the clip level (implication)
            clipped_membership = min(memberships[upper_bound_set], self.membership_clips[upper_bound_set])
            self.aggregated_memberships.append(clipped_membership)

    def defuzzify(self):
        """
        Calculates the crisp output value using the Center of Gravity (Centroid) method.
        formula: sum(mu(x) * x) / sum(mu(x))
        """
        if not self.aggregated_memberships:
            print("Rule evaluations are not aggregated!")
            return None
        
        numerator = 0
        denominator = 0
        
        # Iterate over x values and their corresponding aggregated membership values
        x_values = range(self.x_range[0], self.x_range[1] + 1, 1)
        
        for membership, x in zip(self.aggregated_memberships, x_values):
            numerator += (membership * x)
            denominator += membership
            
        if denominator == 0:
            return None
            
        center_of_gravity = numerator / denominator
        return center_of_gravity

    def clean_aggregated_memberships(self):
        self.aggregated_memberships.clear()

    def clean_clip_levels(self):
        for key in self.membership_clips.keys():
            self.membership_clips[key] = 0
