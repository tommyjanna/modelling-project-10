from nnf import Var
from lib204 import Encoding

# Review this later
from nnf import true


N_AIRPORTS = 3
N_TIMESTEPS = 2 

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

    ### The pilot cannot be at the same airport in two adjacent timesteps.
    for timestep in range(N_TIMESTEPS - 1):
        for airport in range(N_AIRPORTS):
            E.add_constraint(~pilot_a[timestep][airport] | ~pilot_a[timestep + 1][airport])


    ### Pilot B can only make a single flight
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


    ### Pilot A and B can't be at the same airport at the same timestep.
    for timestep in range(N_TIMESTEPS):
        for airports in range(N_AIRPORTS):
            E.add_constraint(~pilot_a[timestep][airports] |  ~pilot_b[timestep][airports])

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
