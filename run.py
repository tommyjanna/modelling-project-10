from nnf import Var
from lib204 import Encoding

# Review this later
from nnf import true


N_AIRPORTS = 3
N_TIMESTEPS = 3
N_PILOT_B_MAX_FLIGHTS = N_TIMESTEPS - 1

pilot_a = []
pilot_b = []

class Flight:
  def __init__(self, airport):
    self.airport = airport


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


def display_solution(solution):
    # Normal solution output:
    # {<__main__.Flight object at 0x7f09c42d3280>: True, <__main__.Flight object at 0x7f09c42cc820>: True, <__main__.Flight object at 0x7f09c43d46a0>: False}   

    """ FINAL
    for timestep in range(N_TIMESTEPS):
        for flight in range(N_AIRPORTS):
            keys = list(solution)
            if str(solution[keys[flight]]) == "True":
                print("Pilot A - Timestep " + str(timestep))
                keys = list(solution)
                print("Airport #" + str(flight))
    """ 
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
#                print(pilot_b[i][j])
#                print(str(keys[k]))
                if str(pilot_b[i][j]) == "Var(" + str(keys[k]) + ")":
                    print("Airport " + str(j) + ": " + str(solution[keys[k]]))


    """ Hell lies within this codeblock
    print("Pilot A")
    for timestep in range(N_TIMESTEPS):
        print("Timestep " + str(timestep))
        for flight in range(N_AIRPORTS):
            keys = list(solution)
            print("Airport " + str(flight) + ": " + str(solution[keys[flight + (N_AIRPORTS * timestep)]]) + str(pilot_a[timestep][flight]))
    """

#
# Build an example full theory for your setting and return it.
#
#  There should be at least 10 variables, and a sufficiently large formula to describe it (>50 operators).
#  This restriction is fairly minimal, and if there is any concern, reach out to the teaching staff to clarify
#  what the expectations are.
def example_theory():
    E = Encoding()
    
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
    
    # Some sexy stuff 
    # print(only_one_airport)
    # print(eval(only_one_airport))

    # Evaluate the string to turn it into NNF type
    E.add_constraint(eval(only_one_airport))

    ### Pilot A always starts on airport 1!
    # E.add_constraint(pilot_a[0][0])

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

    print(pilot_b_flights)
    # Evaluate the string to turn it into NNF type
    E.add_constraint(eval(pilot_b_flights))

    # Further, pilot B will remain at this airport after he is finished flying.
    """ Why doesn't this version work?
    for timestep in range(N_PILOT_B_MAX_FLIGHTS, N_TIMESTEPS):
        for airport in range(N_AIRPORTS):
            E.add_constraint(iff(pilot_b[timestep - N_TIMESTEPS - 1][airport], pilot_b[-1][airport]))
    """
    for airport in range(N_AIRPORTS):
        E.add_constraint(iff(pilot_b[-2][airport], pilot_b[-1][airport]))

    ### Pilot B cannot be at the same airport in two adjacent timesteps (except their last timestep of course).
    for timestep in range(N_TIMESTEPS - 2):
        for airport in range(N_AIRPORTS):
            E.add_constraint(~pilot_b[timestep][airport] | ~pilot_b[timestep + 1][airport])


    """### Pilot B can only make a single flight
    single_flight = ""

    for n in range(N_TIMESTEPS * N_AIRPORTS):
        single_flight += "("
        for timestep in range(N_TIMESTEPS):
            for airport in range(N_AIRPORTS):
                if n == (timestep * 3) + airport:
                    single_flight += "pilot_b[%d][%d] & " % (timestep, airport)
                else:
                    single_flight += "~pilot_b[%d][%d] & " % (timestep, airport)

        single_flight = single_flight[:-3]
        single_flight += ") | "

    single_flight = single_flight[:-3]
    # print(single_flight)
    E.add_constraint(eval(single_flight))
    """ 

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
    #for flight in range(N_AIRPORTS):
    #    for v,vn in zip([a,b,c,x,y,z], 'abcxyz'):
    #  print(" %s: %.2f" % (vn, T.likelihood(v)))
    print()
