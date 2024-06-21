"""This file contains the Day class and all of its related functions."""

from numpy import array, count_nonzero

from .course import Course

COURSE_LENGTH = 18

class Day:

    def __init__(self, course: Course, score_list: list):
        self.course = course
        self.raw_score_list = score_list
        self.points = self.calculate_points()

    @property
    def total_raw_score(self):
        """A property used to calculate the total raw score for the day."""
        return sum(self.raw_score_list)

    def get_calcutta_scores(self, handicap: int):
        """This function will accept a handicap and generate the net scores after applying
        the handicap to the raw scores."""
        hole_modifiers = self.generate_dots(handicap)
        net_score_list = list(array(self.raw_score_list)-array(self.course.par_order))
        bonus_points = sum(-score for score in net_score_list if score<0)
        deductions = count_nonzero(net_score_list == 3)
        modifiers = bonus_points - deductions
        net_score_list = list(array(net_score_list)-array(hole_modifiers))
        for i, score in enumerate(net_score_list):
            if score == 3:
                net_score_list[i] = 2

        return net_score_list, modifiers

    def generate_dots(self, handicap: int):
        """This function will calculate the hole by hole modifiers for a given course.
        These modifiers are applied to the player's raw score for the Calcutta."""

        handicap_order = self.course.handicap_order
        hole_modifiers = []
        for hole in handicap_order:
            if (handicap - COURSE_LENGTH - hole) >= 0:
                hole_modifiers.append(2)
            elif (handicap - hole) >= 0:
                hole_modifiers.append(1)
            else:
                hole_modifiers.append(0)

        if len(hole_modifiers) != COURSE_LENGTH:
            raise ValueError("Not enough holes provided for hole modifier calculations.")
        
        return hole_modifiers
    
    def calculate_points(self):
        """This function will calculate the number of points earned using the stableford system."""

        # Define score mapping of Stableford System
        stableford_conversion = {
            3 : -1,
            2 : 0,
            1 : 1,
            0 : 2,
            -1 : 4,
            -2 : 6,
            -3 : 8,
            -4 : 12
        }

        net_score_list = array(self.raw_score_list) - array(self.course.par_order)

        # Begin calculating the dogfight score
        points = 0
        for hole, net_score in enumerate(net_score_list):
            
            # Verify that the score is possible and in the dictionary.
            if net_score not in stableford_conversion or self.course.par_order[hole]+net_score <= 0:
                raise KeyError(f"Invalid score of {self.score_list[hole]} on Hole {hole+1}")

            points += stableford_conversion[net_score]
        
        return points
    
    def get_net_points(self, handicap: int):
        return self.points - (36-handicap)
        