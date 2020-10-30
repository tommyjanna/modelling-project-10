from nnf import Var
from lib204 import Encoding



N_AIRPORTS = 3
pilot_a = []
pilot_b = []


class Flight:
  def __init__(self, airport):
    self.airport = airport
  
    

for i in range(N_AIRPORTS): 
  flight = Flight(i)
  pilot_a.append(Var(flight))



def iff(left, right):
    return (left.negate() | right) & (right.negate() | left)
  


# Call your variables whatever you want


#
# Build an example full theory for your setting and return it.
#
#  There should be at least 10 variables, and a sufficiently large formula to describe it (>50 operators).
#  This restriction is fairly minimal, and if there is any concern, reach out to the teaching staff to clarify
#  what the expectations are.
def example_theory():
    E = Encoding()
    # same_end = pilot_a[0] and pilot_a[-1]
  # flights_travelled = (pilot_a[1] and pilot_a[0]) or (pilot_a[1] and pilot_a[2]) or (pilot_a[0] and pilot_a[2])
    ending = pilot_a[2]  
    E.add_constraint(ending)

    return E


if __name__ == "__main__":

    T = example_theory()

    print("\nSatisfiable: %s" % T.is_satisfiable())
    print("# Solutions: %d" % T.count_solutions())
    print("   Solution: %s" % T.solve())

    print("\nVariable likelihoods:")
  #  for v,vn in zip([a,b,c,x,y,z], 'abcxyz'):
  #    print(" %s: %.2f" % (vn, T.likelihood(v)))
    print()
