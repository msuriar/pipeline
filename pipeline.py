"""Simulate a pipeline with multiple stations able to produce units of work."""
import random

def main():
  """Set up and run pipeline."""
  pipeline = Pipeline(6)
  ticks = range(20)
  for _ in ticks:
    pipeline.dump()
    pipeline.tick()

def pipelineprint(pipeline):
  """Pretty print pipeline."""
  totals = [ s.total for s in pipeline ]
  print ' ---> '.join([str(t) for t in totals])


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
    pipeline[-1] = Station(sink=True)
    for i in reversed(range(1, self.length - 1)):
      pipeline[i] = Station(succ=pipeline[i+1])
    pipeline[0] = Station(src=True, succ=pipeline[1])
    return pipeline

  def tick(self):
    """Advance pipeline."""
    for stations in self.stations:
      stations.work()

  def dump(self):
    """Dump pretty printed pipeline."""

    totals = [str(s.total) for s in self.stations]
    totals[0] = ">>>"
    print ' ---> '.join(totals)

class Station(object):
  """Station is a class representing each workstation."""
  def __init__(self, src=False, sink=False, succ=None):
    self.src = src
    self.sink = sink
    self.succ = succ
    self.total = 0

  def rcv(self, amount):
    """Receive work."""
    self.total += amount

  def work(self):
    """Do work."""
    if self.src:
      self.succ.rcv(random.choice(range(1, 7)))
    elif not self.sink:
      throughput = min(self.total, random.choice(range(1, 7)))
      self.succ.rcv(throughput)
      self.total -= throughput

if __name__ == "__main__":
  main()
