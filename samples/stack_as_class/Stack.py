class Stack(object):
  # State
  def __init__(self):
    self.stack = list()

  # Actions
  def push(self, x):
    self.stack.insert(0,x)

  def pop(self):
    result = self.stack[0]
    del self.stack[0]
    return result

  def popEnabled(self):
    return self.stack


  ### Metadata
  # TODO: get this automaticaly
  # FIXME: put this away somehow for more elegancy
  state = ('stack',)
  actions = (push, pop)
  enablers = { pop:(popEnabled,) }
  domains = { push: {'x':[1,2]} }

  def StateFilter(self):
    return len(self.stack) < 4

  # needed for multiple test runs
  def Reset(self): 
    self.stack = []