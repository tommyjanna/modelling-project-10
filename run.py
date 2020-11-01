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
    airport_list = []
    for flight in range(N_AIRPORTS):
        flight = Flight(flight)
        airport_list.append(Var(flight))
    pilot_a.append(airport_list)

print(pilot_a)

"""
for i in range(N_AIRPORTS): 
  flight = Flight(i)
  pilot_a.append(Var(flight))
  pilot_b.append(Var(flight))
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
    for timestep in range(N_TIMESTEPS):
        print("Timestep " + str(timestep))
        for flight in range(N_AIRPORTS):
            keys = list(solution)
            print("Airport " + str(flight) + ": " + str(solution[keys[flight]]))

#
# Build an example full theory for your setting and return it.
#
#  There should be at least 10 variables, and a sufficiently large formula to describe it (>50 operators).
#  This restriction is fairly minimal, and if there is any concern, reach out to the teaching staff to clarify
#  what the expectations are.
def example_theory():
    E = Encoding()
    
    # Pilot A must make exactly 2 flights.
    """for flight in range(N_AIRPORTS):
        
        if pilot_a[i] == true:
            flight_sum += 1
    """

    for timestep in range(N_TIMESTEPS):
        E.add_constraint((pilot_a[timestep][0] & ~pilot_a[timestep][1] & ~pilot_a[timestep][2]) | (~pilot_a[timestep][0] & pilot_a[timestep][1] & ~pilot_a[timestep][2]) | (~pilot_a[timestep][0] & ~pilot_a[timestep][1] & pilot_a[timestep][2]))


    # Pilot A cannot travel to the same airport in its 2 timesteps.
    for i in range(N_AIRPORTS):
        E.add_constraint(pilot_a[0][i] & ~pilot_a[1][i])

        #E.add_constraint((pilot_b[timestep][0] & ~pilot_b[timestep][1] & ~pilot_b[timestep][2]) | (~pilot_b[timestep][0] & pilot_b[timestep][1] & ~pilot_b[timestep][2]) | (~pilot_b[timestep][0] & ~pilot_b[timestep][1] & pilot_b[timestep][2]))

    # E.add_constraint((pilot_a[0] & pilot_a[1] & ~pilot_a[2]) | (pilot_a[0] & pilot_a[2] & ~pilot_a[1]) | (pilot_a[1] & pilot_a[2] & ~pilot_a[0]))
    
    # Pilot A and Pilot B must end at different airports.

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
