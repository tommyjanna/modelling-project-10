from nnf import Var
from lib204 import Encoding
import random
import math


N_AIRPORTS = 4
N_TIMESTEPS = 5
N_PILOT_B_MAX_FLIGHTS = N_TIMESTEPS - 1


class Flight:
    def __init__(self, airport):
        self.airport = airport

class Pilot:
    count = 0

    def __init__(self, pilot_id, start):
        self.pilot_id = chr(pilot_id + 65)
        self.current_airport = start
        Pilot.count += 1

    def __str__(self):
        return "Pilot: %c --- Current airport %d" % (self.pilot_id, self.current_airport)

    def fly():
        pass


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

    greatest_indices = []
    for i in range(n):
        greatest = 0

        for j in range(len(values)):
            if values[j] > greatest:
                greatest = values[j]

        values.remove(greatest)
        greatest_indices.append(greatest)

    # Add extra values from the list of the same value...
    for i in range(len(values)):
        if values[i] in greatest_indices:
            greatest_indices.append(values[i])

    return greatest_indices

def create_pilot():
    """
    Adds a new pilot at the end of the list pilots.
    """
    new_pilot = Pilot(len(pilots), find_max(demand))
    demand[new_pilot.current_airport] -= 1
    pilots.append(new_pilot)

def display_pilots(pilots):
    for pilot in pilots:
        print(pilot)



demand = []
pilots = []

##### OLD CODE TO BE REPLACED
pilot_a = []
pilot_b = []

# Each pilot exists as an array of the class Flight.
# There is a Flight object for every airport in the scenario multiplied
# by the total number of timesteps. If a Flight is marked as True,
# the pilot is at that airport at that given timestep. Otherwise, False.
for timestep in range(N_TIMESTEPS):
    # Initialize pilot A variables
    airport_list = []
    for flight in range(N_AIRPORTS):
        flight = Flight(flight)
        airport_list.append(Var(flight))
    pilot_a.append(airport_list)

    # Initialize pilot B variables
    airport_list = []
    for flight in range(N_AIRPORTS):
        flight = Flight(flight)
        airport_list.append(Var(flight))
    pilot_b.append(airport_list)
##### END OLD CODE TO BE REPLACED

# Generate demand
# The starting airport doesn't have any demand
for airport in range(N_AIRPORTS):
    demand.append(random.randint(0, N_TIMESTEPS - 1))


# Create pilots required based on demand
# No matter what, start with one pilot
create_pilot()
total_demand = 0

for val in demand:
    total_demand += val

    if val > Pilot.count * (N_TIMESTEPS // 2):
        create_pilot()
    
while Pilot.count * (N_TIMESTEPS - 1) < total_demand:
    create_pilot()


# Display demand
for i in range(N_AIRPORTS):
    print(str(i) + ": Demand " + str(demand[i]))

print("Pilots calculated: " + str(Pilot.count))

display_pilots(pilots)

""" Display pilot variable addresses
for i in range(3):
    for j in range(3):
        print(pilot_a[i][j])

for i in range(3):
    for j in range(3):
        print(pilot_b[i][j])
"""

def iff(left, right):
    return (left.negate() | right) & (right.negate() | left)


"""
Converts normal NNF solution outputs to display each pilots flight statuses in order of timestep.
Originally, the solution output is difficult to read and out of order.

Normal solution output:
{<__main__.Flight object at 0x7f09c42d3280>: True, <__main__.Flight object at 0x7f09c42cc820>: True, <__main__.Flight object at 0x7f09c43d46a0>: False}   

display_solution() output:
Pilot A:
Timestep 0:
Airport 0: True
Airport 1: False
...
"""
def display_solution(solution):
    print("Pilot A")
    for i in range(N_TIMESTEPS):
        print("Timestep " + str(i))
        for j in range(N_AIRPORTS):
            keys = list(solution)
            for k in range(len(keys)):
                if str(pilot_a[i][j]) == "Var(" + str(keys[k]) + ")":
                    print("Airport " + str(j) + ": " + str(solution[keys[k]]))

    print("\nPilot B")
    for i in range(N_TIMESTEPS):
        print("Timestep " + str(i))
        for j in range(N_AIRPORTS):
            keys = list(solution)
            for k in range(len(keys)):
                if str(pilot_b[i][j]) == "Var(" + str(keys[k]) + ")":
                    print("Airport " + str(j) + ": " + str(solution[keys[k]]))


#
# Build an example full theory for your setting and return it.
#
#  There should be at least 10 variables, and a sufficiently large formula to describe it (>50 operators).
#  This restriction is fairly minimal, and if there is any concern, reach out to the teaching staff to clarify
#  what the expectations are.
def example_theory():
    E = Encoding()

    ### First determine the the valid starting points for each pilot.
    # Based on the number of pilots, which airports should be filled?
    # There are n!/(n-r)! ways to assign n objects to m things where order matters and repetition is not allowed.
    for i in math.factorial(len(pilots)) / math.factorial(len(pilots) - len(find_n_maxes(len(pilots), demand))):
        #E.add_constraint(pilots[i])
        pass
    
    
    
    ### Pilot A can only make one flight per timestep.
    # Use a string to build the logical expression dynamically.
    only_one_airport = ""

    for timestep in range(N_TIMESTEPS):
        only_one_airport += "("
        for airport in range(N_AIRPORTS):
            # Current airport in loop is true.
            only_one_airport += "(pilot_a[%d][%d] &" % (timestep, airport)

            # All airports below airport are false, count up
            for count_up in range(0, airport):
                only_one_airport += " ~pilot_a[%d][%d] &" % (timestep, count_up)

            # All airports above airport are false, count up
            for count_up in range(airport + 1, N_AIRPORTS):
                only_one_airport += " ~pilot_a[%d][%d] &" % (timestep, count_up)

            # Remove the last & from the string
            only_one_airport = only_one_airport[:-2]
            only_one_airport += ") | "
        
        # Remove the last | from the string, use &'s to seperate timesteps
        only_one_airport = only_one_airport[:-3]
        only_one_airport += ") & "

    # Remove the last & from the string.
    only_one_airport = only_one_airport[:-3] 
    
    # Evaluate the string to turn it into NNF type
    E.add_constraint(eval(only_one_airport))


    ### Pilot A cannot be at the same airport in two adjacent timesteps.
    for timestep in range(N_TIMESTEPS - 1):
        for airport in range(N_AIRPORTS):
            E.add_constraint(~pilot_a[timestep][airport] | ~pilot_a[timestep + 1][airport])

    
    ### Pilot B can only make one flight per timestep, and can only fly one flight LESS than pilot A.
    # Use a string to build the logical expression dynamically.
    pilot_b_flights = ""

    for timestep in range(N_TIMESTEPS):
        pilot_b_flights += "("
        for airport in range(N_AIRPORTS):
            # Current airport in loop is true.
            pilot_b_flights += "(pilot_b[%d][%d] &" % (timestep, airport)

            # All airports below airport are false, count up
            for count_up in range(0, airport):
                pilot_b_flights += " ~pilot_b[%d][%d] &" % (timestep, count_up)

            # All airports above airport are false, count up
            for count_up in range(airport + 1, N_AIRPORTS):
                pilot_b_flights += " ~pilot_b[%d][%d] &" % (timestep, count_up)

            # Remove the last & from the string
            pilot_b_flights = pilot_b_flights[:-2]
            pilot_b_flights += ") | "
        
        # Remove the last | from the string, use &'s to seperate timesteps
        pilot_b_flights = pilot_b_flights[:-3]
        pilot_b_flights += ") & "

    # Remove the last & from the string.
    pilot_b_flights = pilot_b_flights[:-3] 

    # Evaluate the string to turn it into NNF type
    E.add_constraint(eval(pilot_b_flights))

    
    ### Pilot B cannot be at the same airport in two adjacent timesteps if they still have flights left to make denoted by N_PILOT_MAX_FLIGHTS.
    for timestep in range(N_PILOT_B_MAX_FLIGHTS - 1):
        for airport in range(N_AIRPORTS):
            E.add_constraint(~pilot_b[timestep][airport] | ~pilot_b[timestep + 1][airport])


    ### Further, pilot B will remain at this airport after he is finished all its flights.
    for timestep in range(N_PILOT_B_MAX_FLIGHTS, N_TIMESTEPS):
        for airport in range(N_AIRPORTS):
            E.add_constraint(iff(pilot_b[timestep - N_TIMESTEPS - 1][airport], pilot_b[-1][airport]))
    

    ### Pilot A and B can't be at the same airport at the same timestep (other than timestep 0).
    for timestep in range(1, N_TIMESTEPS):
        for airports in range(N_AIRPORTS):
            E.add_constraint(~pilot_a[timestep][airports] |  ~pilot_b[timestep][airports])


    ### Pilot A and B both start at airport 0
    E.add_constraint(pilot_a[0][0] & pilot_b[0][0])

    return E


if __name__ == "__main__":

    T = example_theory()

    print("\nSatisfiable: %s" % T.is_satisfiable())
    print("\nNumber of solutions: %d" % T.count_solutions())
    print("\nSample solution:")
    display_solution(T.solve())
    # print("   Solution: %s" % T.solve())

    print("\nVariable likelihoods:")
    """
    for flight in range(N_AIRPORTS):
        for v,vn in zip([a,b,c,x,y,z], 'abcxyz'):
            print(" %s: %.2f" % (vn, T.likelihood(v)))
    """
    print()
