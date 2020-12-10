from nnf import Var
from lib204 import Encoding
import random
import math

# Can be any value greater than 0 (these are good defaults)
N_AIRPORTS = 4
N_TIMESTEPS = 5


class Airport:
    """
    Represents a single airport at a given timestep.
    Each Pilot will have an array of Airports.
    """
    def __init__(self, airport):
        self.airport = airport

class Pilot:
    # Static counter for all instances
    count = 0

    def __init__(self, pilot_id, start):
        # Name the pilots starting at A, B, ...
        self.pilot_id = chr(pilot_id + 65)
        self.starting_airport = start

        # Increase static counter
        Pilot.count += 1

        self.location = []

        # Initialize array of Var's for each pilot representing their location
        for timestep in range(N_TIMESTEPS):
            airports = []
            for num in range(N_AIRPORTS):
                airport = Airport(num)
                airports.append(Var(airport))
            self.location.append(airports)

    def __str__(self):
        return "Pilot: %c --- Starting airport %d" % (self.pilot_id, self.starting_airport)


def find_max(values):
    """
    Returns index of max value in a list values.
    If there exists multiple, pick one at random.
    """

    greatest = 0
    greatest_indices = []

    for i in range(len(values)):
        if values[i] == greatest:
            greatest_indices.append(i)

        if values[i] > greatest:
            greatest_indices.clear()
            greatest = values[i]
            greatest_indices.append(i)

    # greatest_indices will have 1 or more indices. Pick one at random.
    return random.choice(greatest_indices)

def find_n_maxes(n, values):
    """
    NOTE: Pass values by VALUE!
    Returns indices of the n max values from a list.
    If more than n values have the same value, return those as well.
    """

    sorted_values = sorted(values)

    greatest_indices = []
    for i in range(n):
        found_index = 0
        for j in range(len(values)):
            if sorted_values[-1 - i] == values[j] and j not in greatest_indices:
                greatest_indices.append(j)


    return greatest_indices

def create_pilot(demand):
    """
    Adds a new pilot at the end of the list pilots.
    """
    new_pilot = Pilot(len(pilots), find_max(demand))
    
    # Set demand temporarily to -1, because another pilot cannot spawn here.
    demand[new_pilot.starting_airport] = -1
    pilots.append(new_pilot)

def display_pilots(pilots):
    """
    Displays a list of pilots.
    """
    for pilot in pilots:
        print(pilot)

def iff(left, right):
    return (left.negate() | right) & (right.negate() | left)

def xor(left, right):
    return (left & right).negate() & (left | right)

def display_solution(solution, verbose=False):
    """
    Converts normal NNF solution outputs to display each pilots flight statuses in order of timestep.
    Originally, the solution output is difficult to read and out of order.

    Normal solution output:
    {<__main__.Pilot object at 0x7f09c42d3280>: True, <__main__.Pilot object at 0x7f09c42cc820>: True, <__main__.Pilot object at 0x7f09c43d46a0>: False}   

    display_solution() output:
    Pilot A:
    Timestep 0:
    Airport 0: True
    Airport 1: False
    ...

    The above is an example of verbose output.
    By default, the solution is non-verbose, and prints a prettier model.
    E.g.
    Pilot A
    Airport 1 --> Airport 2 --> Airport 0 ...
    """
    for pilot in range(Pilot.count):
        # Print each pilot as a header
        print("Pilot " + pilots[pilot].pilot_id)

        for i in range(N_TIMESTEPS):
            if verbose:
                print("Timestep " + str(i))
            for j in range(N_AIRPORTS):
                keys = list(solution)
                for k in range(len(keys)):
                    if str(pilots[pilot].location[i][j]) == "Var(" + str(keys[k]) + ")":
                        if verbose:
                            print("Airport " + str(j) + ": " + str(solution[keys[k]]))
                        else:
                            if str(solution[keys[k]]) == 'True':
                                if i == N_TIMESTEPS - 1:
                                    print("Airport " + str(j) + "\n")
                                else:
                                    print("Airport " + str(j) + " --> ", end="")

def pilot_permute(pilots, options):
    """
    Determines all possible assignments from the first list pilots,
    onto the second list options. This is a wrapper function for padding
    the first list with "None" objects to calculate assignments.
    """

    # Pad the pilot list to be able to generate "assignment"
    pad_pilots = pilots[:]
    while len(pad_pilots) < len(options):
        pad_pilots.append(None)

    # Send padded list to normal permute function.
    return permute(pad_pilots)

def permute(pilots):
    """
    Returns a list of all permutations on a given list where each
    object is used once.
    """

    if len(pilots) == 0:
        return []


    if len(pilots) == 1:
        return [pilots]

    # List storing partial permutations
    partial = []

    for i in range(len(pilots)):
        # Save current pilot
        current = pilots[i]

        # Save every other object in list other than current
        rest = pilots[:i] + pilots[i + 1:]

        # Run recursive call on rest list
        for p in permute(rest):
            partial.append([current] + p)

    return partial


###########################################################################
### Initialize scenario
demand = []
pilots = []

# Generate demand
# The starting airport doesn't have any demand
for airport in range(N_AIRPORTS):
    demand.append(random.randint(0, N_TIMESTEPS - 1))

# Display demand
print("Randomly generated demand for " + str(N_AIRPORTS) + " airports...")
for i in range(N_AIRPORTS):
    print("Airport " + str(i) + " has a demand of " + str(demand[i]))


# Create pilots required based on demand
# No matter what, start with one pilot
temp_demand = demand[:]
total_demand = 0
create_pilot(temp_demand)

for val in demand:
    total_demand += val

    if val > Pilot.count * (N_TIMESTEPS // 2):
        create_pilot(temp_demand)
    
while Pilot.count * (N_TIMESTEPS - 1) < total_demand - Pilot.count:
    create_pilot(temp_demand)

# Display pilots
print("\nPilots calculated: " + str(Pilot.count))
print("Example starting location of airports (may not be same as what T.solve() shows, but valid nonetheless)...")
display_pilots(pilots)

# Update demand
for pilot in range(Pilot.count):
    demand[pilots[pilot].starting_airport] -= 1
###########################################################################

#
# Build an example full theory for your setting and return it.
#
#  There should be at least 10 variables, and a sufficiently large formula to describe it (>50 operators).
#  This restriction is fairly minimal, and if there is any concern, reach out to the teaching staff to clarify
#  what the expectations are.
def example_theory():
    E = Encoding()

    ###########################################################################
    ### First determine the the valid starting points for each pilot.
    # Based on the number of pilots, which airports should be filled?
    # There are r objects to fill from find_n_maxes()
    fill = find_n_maxes(Pilot.count, demand[:])

    # There are (n+r-1)C(r-1) ways to assign n objects to m things where order matters and repetition is not allowed.
    # Equivalent to n!/(n-r)!*r!
    starting = pilot_permute(pilots, fill)

    starting_constraint = ''
    for scenario in starting:
        first = True

        for i in range(len(scenario)):
            if scenario[i] == None:
                # This was a padded object, do nothing
                continue

            # Find out which pilot is chosen for a given airport
            for p in range(len(pilots)):
                if pilots[p].pilot_id == scenario[i].pilot_id:
                    if first:
                        starting_constraint += '(pilots[%d].location[0][%d]' % (p, fill[i])
                        first = False
                    else:
                        starting_constraint += ' & pilots[%d].location[0][%d]' % (p, fill[i])

        starting_constraint += ') | '

    starting_constraint = starting_constraint[:-3]
    E.add_constraint(eval(starting_constraint))


    # Extra Information: Uncomment to display all the permutations fo starting positions for the pilots.
    """
    print(starting_constraint)
    count = 0
    my = pilot_permute(pilots, fill)
    for i in range(len(my)):
        for j in range(len(my[i])):
            count += 1
    print("There are: " + str(count) + " different initial positions for the pilots")
    """
    ###########################################################################


    ###########################################################################
    ### Every pilot can only make one flight per timestep.
    for pilot in range(Pilot.count):
        only_one_airport = '('
        for timestep in range(N_TIMESTEPS):
            for airport in range(N_AIRPORTS):
                # Current airport in loop is true.
                only_one_airport += '(pilots[%d].location[%d][%d] &' % (pilot, timestep, airport)

                # All airports below airport are false, count up
                for count_up in range(0, airport):
                    only_one_airport += ' ~pilots[%d].location[%d][%d] &' % (pilot, timestep, count_up)

                # All airports above airport are false, count up
                for count_up in range(airport + 1, N_AIRPORTS):
                    only_one_airport += ' ~pilots[%d].location[%d][%d] &' % (pilot, timestep, count_up)

                # Remove the last & from the string
                only_one_airport = only_one_airport[:-2]
                only_one_airport += ') | '

            # Remove the last | from the string, use &'s to seperate timesteps
            only_one_airport = only_one_airport[:-3]
            only_one_airport += ') & ('

        # Remove the last & from the string.
        only_one_airport = only_one_airport[:-4]

        # Evaluate the string to turn it into NNF type
        E.add_constraint(eval(only_one_airport))
    ###########################################################################


    ###########################################################################
    ### Any two pilots cannot be at the same airport at the same timestep.
    for pilot in range(Pilot.count):
        for timestep in range(N_TIMESTEPS):
            for airport in range(N_AIRPORTS):
                only_one_pilot = ''
                
                # Current pilot is true
                only_one_pilot += '(pilots[%d].location[%d][%d] &' % (pilot, timestep, airport)

                # Negate all the pilots below
                for count_up in range(0, pilot):
                    only_one_pilot += ' ~pilots[%d].location[%d][%d] &' % (count_up, timestep, airport)

                # Negate all the pilots above 
                for count_up in range(pilot + 1, Pilot.count):
                    only_one_pilot += ' ~pilots[%d].location[%d][%d] &' % (count_up, timestep, airport)

                # Remove the last & and space
                only_one_pilot = only_one_pilot[:-2]
                only_one_pilot += ') | '

            # Remove the last | from the string.
            only_one_pilot = only_one_pilot[:-3]
            only_one_pilot += ' & '
        
        # Remove the last | from the string.
        only_one_pilot = only_one_pilot[:-3]
        only_one_pilot += ' & '

    only_one_pilot = only_one_pilot[:-3]

    E.add_constraint(eval(only_one_pilot))
    ###########################################################################

    
    ###########################################################################
    ### Each pilot cannot remain at the same airport in two adjacent timesteps.
    for pilot in range(Pilot.count):
        for timestep in range(N_TIMESTEPS - 1):
            for airport in range(N_AIRPORTS):
                # Pilot cannot be at the same location at an incremented timestep.
                E.add_constraint(~pilots[pilot].location[timestep][airport] | ~pilots[pilot].location[timestep + 1][airport])
    ###########################################################################


    ###########################################################################
    ### Pilot should only fly to an airport that has demand.
    for pilot in range(Pilot.count):
        for timestep in range(N_TIMESTEPS - 1):
            for airport in range(N_AIRPORTS):
                # For all pilots and every timestep and every airport,
                # if the airport has 0 demand, the pilot should not fly there.
                if demand[airport] == 0:
                    # UNLESS - Every other airport also has 0 demand.
                    for inner_airport in range(N_AIRPORTS):
                        if demand[inner_airport] != 0:
                            E.add_constraint(~pilots[pilot].location[timestep][airport])
                            break
    ###########################################################################

    return E


if __name__ == "__main__":

    T = example_theory()

    print("\nSatisfiable: %s" % T.is_satisfiable())
    
    if str(T.is_satisfiable()) == "False":
        print("\nThis randomly generated scenario has no solution.")
    else:
        print("\nNumber of solutions: %d" % T.count_solutions())
        print("\nSample solution:")
        display_solution(T.solve())


    """
    # Extra Information: Uncomment to display variable likelihoods
    print("\nVariable likelihoods:")
    for pilot in range(Pilot.count):
        for timestep in range(N_TIMESTEPS):
            for airport in range(N_AIRPORTS):
                name = "Pilot " + pilots[pilot].pilot_id + " at timestep " + str(timestep) + " at airport " + str(airport)
                print(" %s: %.2f" % (name, T.likelihood(pilots[pilot].location[timestep][airport])))
    """

    print()
