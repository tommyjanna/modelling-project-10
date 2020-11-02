from functools import total_ordering
from os import umask
from nnf import Var
from lib204 import Encoding

from nnf import true

"""
000
001
010
011 <- pre
100 <- post
101
110
111
"""

x_pre = []
pres = []
x_post = []
posts = []
BITS = 6

class Bit(object):
    def __init__(self, name):
        self.name = name
    def __hash__(self):
        return hash(self.name)
    def __str__(self):
        return self.name
    def __repr__(self):
        return str(self)

for i in range(BITS):
    pre = Bit(f'pre_{i}')
    post = Bit(f'post_{i}')
    pres.append(pre)
    posts.append(post)
    x_pre.append(Var(pre))
    x_post.append(Var(post))


def iff(left, right):
    return (left.negate() | right) & (right.negate() | left)


def display_solution(sol):
    bitvec_pre = ''
    bitvec_post = ''
    for p in pres:
        bitvec_pre += {True: '1', False: '0'}[sol.get(p, False)]
    for p in posts:
        bitvec_post += {True: '1', False: '0'}[sol.get(p, False)]
    print(" Pre: "+bitvec_pre)
    print("Post: "+bitvec_post)

def extract_solution(sol):
    bitvec = ''
    for p in posts:
        bitvec += {True: '1', False: '0'}[sol.get(p, False)]
    return bitvec

def set_pre(bits):
    f = true
    for i in range(BITS):
        if bits[i] == '0':
            f = f & ~x_pre[i]
        else:
            f = f & x_pre[i]
    return f


def example_theory():
    E = Encoding()

    # Final index
    E.add_constraint(iff(x_post[-1], ~x_pre[-1]))

    # Rest of the indices
    for i in range(len(x_pre)-1):
        # Set for everything to the right
        needs_to_flip = true
        for j in range(i+1, len(x_pre)):
            needs_to_flip &= x_pre[j]
        E.add_constraint(iff(x_post[i], (needs_to_flip & ~x_pre[i]) | (x_pre[i] & needs_to_flip.negate())))

    return E


if __name__ == "__main__":

    T = example_theory()

    # print("\nSatisfiable: %s" % T.is_satisfiable())
    # print("# Solutions: %d" % T.count_solutions())
    # print("   Solution: %s" % T.solve())

    T0 = example_theory()
    total_models = T.count_solutions()

    T = example_theory()
    T.add_constraint(x_pre[2] & ~x_post[2])
    sol = T.solve()
    display_solution(sol)
    print("Models: %d" % T.count_solutions())
    print("Models as percent: %.2f" % (T.count_solutions() / total_models))

    # bitvec = '0'*BITS
    # for i in range(2**BITS):
    #     T = example_theory()
    #     T.add_constraint(set_pre(bitvec))
    #     sol = T.solve()
    #     #display_solution(sol)
    #     print(bitvec)
    #     bitvec = extract_solution(sol) # return '001'


    print("\nVariable likelihoods:")
    for v,vn in zip(x_post, '01234'):
        print(" %s: %.2f" % (vn, T.likelihood(v)))
    print()
