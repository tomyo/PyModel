
# pma Stack.Stack
# 15 states, 28 transitions, 15 accepting states, 0 unsafe states, 0 finished and 0 deadend states

# actions here are just labels, but must be symbols with __name__ attribute

def push(): pass
def pop(): pass

# states, key of each state here is its number in graph etc. below

states = {
  0 : {'Stack': {'stack': []}},
  1 : {'Stack': {'stack': [2]}},
  2 : {'Stack': {'stack': [1]}},
  3 : {'Stack': {'stack': [2, 2]}},
  4 : {'Stack': {'stack': [1, 2]}},
  5 : {'Stack': {'stack': [2, 1]}},
  6 : {'Stack': {'stack': [1, 1]}},
  7 : {'Stack': {'stack': [2, 2, 2]}},
  8 : {'Stack': {'stack': [1, 2, 2]}},
  9 : {'Stack': {'stack': [2, 1, 2]}},
  10 : {'Stack': {'stack': [1, 1, 2]}},
  11 : {'Stack': {'stack': [2, 2, 1]}},
  12 : {'Stack': {'stack': [1, 2, 1]}},
  13 : {'Stack': {'stack': [2, 1, 1]}},
  14 : {'Stack': {'stack': [1, 1, 1]}},
}

# initial state, accepting states, unsafe states, frontier states, deadend states

initial = 0
accepting = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
unsafe = []
frontier = []
finished = []
deadend = []
runstarts = [0]

# finite state machine, list of tuples: (current, (action, args, result), next)

graph = (
  (0, (push, (2,), None), 1),
  (0, (push, (1,), None), 2),
  (1, (pop, (), 2), 0),
  (1, (push, (2,), None), 3),
  (1, (push, (1,), None), 4),
  (2, (pop, (), 1), 0),
  (2, (push, (2,), None), 5),
  (2, (push, (1,), None), 6),
  (3, (pop, (), 2), 1),
  (3, (push, (2,), None), 7),
  (3, (push, (1,), None), 8),
  (4, (pop, (), 1), 1),
  (4, (push, (2,), None), 9),
  (4, (push, (1,), None), 10),
  (5, (pop, (), 2), 2),
  (5, (push, (2,), None), 11),
  (5, (push, (1,), None), 12),
  (6, (pop, (), 1), 2),
  (6, (push, (2,), None), 13),
  (6, (push, (1,), None), 14),
  (7, (pop, (), 2), 3),
  (8, (pop, (), 1), 3),
  (9, (pop, (), 2), 4),
  (10, (pop, (), 1), 4),
  (11, (pop, (), 2), 5),
  (12, (pop, (), 1), 5),
  (13, (pop, (), 2), 6),
  (14, (pop, (), 1), 6),
)
