"""
Analyzer functions
"""

import sys
import os.path
from copy import deepcopy

# Interface to use the ugly old version
a = Analyzer()
anames           = a.anames
states           = a.states
initial          = a.initial
accepting        = a.accepting
frontier         = a.frontier
finished         = a.finished
deadend          = a.deadend
runstarts        = a.runstarts
unsafe           = a.unsafe
explore          = a.explore
state            = a.state
initial_state    = a.initial_state
runstarts_states = a.runstarts_states
accepting_states = a.accepting_states
frontier_states  = a.frontier_states
finished_states  = a.finished_states
deadend_states   = a.deadend_states
unsafe_states    = a.unsafe_states
save             = a.save
actiondef        = Analyzer.actiondef
quote_string     = Analyzer.quote_string
transition       = Analyzer.transition
# /Interface

class Analyzer ():
    def __init__ (self):
        # rebind in explore
        self.anames = []
        # state's index here is its state number in lists, graph below
        self.states = []
        # always, keep as well as runstarts (below) for backward compat.
        self.initial = 0
        self.accepting = []
        # unexplored states in graph, may add more transitions
        self.frontier = []
        # terminal states that are accepting states
        self.finished = []
        # terminal states that are not accepting states
        self.deadend = []
        # initial states of test runs after the first, if any
        self.runstarts = []
        self.unsafe = []
        # a set (no dups) but we want a sequence to see them in order
        self.graph = []

    def explore(self, mp, maxTransitions):
        self.anames = mp.anames
        explored = []
        fsm = [] # list of transitions with mp states not state numbers
        more_runs = True # TestSuite might have multiple runs
        while more_runs:
          initialState = mp.Current()
          self.frontier.append(initialState)
          # includes initial state even if no transitions
          self.states.append(initialState)
          # might already be there
          iInitial = self.states.index(initialState)
          runstarts.append(iInitial)
          # initial state might be accepting even if no transitions
          if mp.Accepting():
            self.accepting.append(iInitial)
          if not mp.StateInvariant():
            self.unsafe.append(iInitial)
          while self.frontier:
            if len(self.graph) == maxTransitions:
                break
            # head, keep in mind current might lead nowhere
            current = self.frontier[0]
            # tail
            self.frontier = self.frontier[1:]
            # might already be there
            icurrent = self.states.index(current)
            # states we checked, some might lead nowhere
            explored.append(current)
            # assign state in mp, need deepcopy here
            mp.Restore(deepcopy(current))
            # all actions, not cleanup
            transitions = mp.EnabledTransitions(list())
            # terminal state, no enabled transitions
            if not transitions:
              if icurrent in self.accepting:
                finished.append(icurrent)
              else:
                deadend.append(icurrent)
            for (aname, args, result, next, next_properties) in transitions:
              # EnabledTransitions doesn't return tran's where not statefilter
              # if next_properties['statefilter']: 
                if len(self.graph) < maxTransitions:
                    if next not in explored and next not in self.frontier:
                        # append for breadth-first, push on head for depth-first
                        # self.frontier contents are already copies
                        self.frontier.append(next)
                    transition = (current, (aname, args, result), next)
                    if transition not in fsm:
                        fsm.append(transition)
                        if current not in self.states:
                            self.states.append(current)
                        if next not in self.states:
                            # next might never be in explored
                            self.states.append(next)
                        inext = self.states.index(next)
                        self.graph.append((icurrent, (aname,args,result), inext))
                        if mp.Accepting() and icurrent not in self.accepting:
                            self.accepting.append(icurrent)
                        if not mp.StateInvariant() and icurrent not in self.unsafe:
                            self.unsafe.append(icurrent)
                        if next_properties['accepting'] and inext not in self.accepting:
                            self.accepting.append(inext)
                        if not next_properties['stateinvariant'] and inext not in self.unsafe:
                            self.unsafe.append(inext)
                else:
                    # found transition that will not be included in graph
                    # not completely explored after all
                    self.frontier.insert(0,current)
                    # explored.remove(current) # not necessary
                    break
                # end if < ntransitions else ...
            # end for transitions
          # end while self.frontier
         
          # continue exploring test suite with multiple runs
          more_runs = False
          if mp.TestSuite:
              try:
                  mp.Reset()
                  more_runs = True
              except StopIteration: # raised by TestSuite Reset after last run
                  pass # no more runs, we're done
        # end while more_runs

    def state(self, i, state):
        return '%s : %s,' % (i, state)

    def initial_state(self): # all FSMs
        return 'initial = %s' % self.initial

    def runstarts_states(self): # initial states of test runs after the first, if any
        return 'runstarts = %s' % self.runstarts

    def accepting_states(self):
        return 'accepting = %s' % self.accepting

    def frontier_states(self):
        return 'frontier = %s' % [ self.states.index(s) for s in self.frontier ]

    def finished_states(self):
        return 'finished = %s' % self.finished

    def deadend_states(self):
        return 'deadend = %s' % self.deadend

    def unsafe_states(self):
        return 'unsafe = %s' % self.unsafe

    def save(self, name):
        f = open("%s.py" % name, 'w')
        f.write('\n# %s' % os.path.basename(sys.argv[0])) # echo command line ...
        f.write(' %s\n' % ' '.join(['%s' % arg for arg in sys.argv[1:]])) # ...etc.
        f.write('# %s states, %s transitions, %s accepting states, %s unsafe states, %s finished and %s deadend states\n' % \
                (len(self.states), len(self.graph),   len(self.accepting),
                 len(self.unsafe), len(self.finished),len(self.deadend)))
        f.write('\n# actions here are just labels, but must be symbols with __name__ attribute\n\n')
        f.writelines([ actiondef(aname)+'\n' for aname in self.anames ])
        f.write('\n# states, key of each state here is its number in graph etc. below\n\n')
        f.write('states = {\n')
        for i,s in enumerate(self.states):
            f.write('  %s\n' % state(i,s))
        f.write('}\n')
        f.write('\n# initial state, accepting states, unsafe states, frontier states, deadend states\n\n')
        f.write('%s\n' % self.initial_state())
        f.write('%s\n' % self.accepting_states())
        f.write('%s\n' % self.unsafe_states())
        f.write('%s\n' % self.frontier_states())
        f.write('%s\n' % self.finished_states())
        f.write('%s\n' % self.deadend_states())
        f.write('%s\n' % self.runstarts_states())
        f.write('\n# finite state machine, list of tuples: (current, (action, args, result), next)\n\n')
        f.write('graph = (\n')
        f.writelines([ '  %s,\n' % self.transition(t) for t in graph ])
        f.write(')\n')
        f.close()
        
    @classmethod
    def actiondef(aname):
        return 'def %s(): pass' % aname

    @classmethod
    def quote_string(x): # also appears in Dot
        if isinstance(x,tuple):
            return str(x)
        else:
            return "'%s'" % x if isinstance(x, str) else "%s" % x

    @classmethod
    def transition(t):
        # return '%s' % (t,) # simple but returns quotes around action name
        current, (action, args, result), next = t
        return '(%s, (%s, %s, %s), %s)' % (current, action, args, 
                                           quote_string(result), next)
