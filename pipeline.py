"""Simulate a pipeline with multiple stations able to produce units of work."""
import random

def main():
  """Set up and run pipeline."""
  pipeline = Pipeline(6)
  ticks = range(20)
  for _ in ticks:
    pipeline.dump()
    pipeline.tick()

class Pipeline(object):
  """Pipeline class."""
  def __init__(self, length, minwork=1, maxwork=7):
    self.length = length
    self.minwork = minwork
    self.maxwork = maxwork
    self.stations = self.__buildpipeline()

  def __buildpipeline(self):
    """Construct pipeline."""
    pipeline = [None]*self.length
    pipeline[-1] = Station(minwork=self.minwork, maxwork=self.maxwork)
    for i in reversed(range(1, self.length - 1)):
      pipeline[i] = Station(succ=pipeline[i+1], minwork=self.minwork,
          maxwork=self.maxwork)
    pipeline[0] = Station(src=True, succ=pipeline[1], minwork=self.minwork,
        maxwork=self.maxwork)
    return pipeline

  def __str__(self):
    return ' ---> '.join([str(s) for s in self.stations])

  def tick(self):
    """Advance pipeline."""
    for station in self.stations:
      station.tick()

  def dump(self):
    """Dump pretty printed pipeline."""
    print self

class Station(object):
  """Station is a class representing each workstation."""
  def __init__(self, src=False, succ=None, minwork=1, maxwork=7):
    self.src = src
    self.succ = succ
    self.minwork = minwork
    self.maxwork = maxwork
    self.in_q = 0
    self.out_q = 0

  def __str__(self):
    if self.src:
      return ">>>"
    elif self.sink:
      return "[ {}||{} ]".format(self.in_q, self.out_q)
    else:
      return "[ {},{} ]".format(self.in_q, self.out_q)

  @property
  def sink(self):
    "Is this a sink station?"
    return None == self.succ

  def tick(self):
    """Tick."""
    amount = self.work()
    self.send(amount)

  def rcv(self, amount):
    """Receive work."""
    self.in_q += amount

  def work(self):
    """Do work."""
    amount = random.choice(range(self.minwork, self.maxwork))
    if not self.src:
      amount  = min(amount, self.in_q)

    self.in_q -= amount
    self.out_q += amount
    return amount

  def send(self, amount):
    """Send to next station."""
    if not self.sink:
      self.out_q -= amount
      self.succ.rcv(amount)

if __name__ == "__main__":
  main()
