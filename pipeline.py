"""Simulate a pipeline with multiple stations able to produce units of work."""
import random

def main():
  """Set up and run pipeline."""
  pipeline = [None]*6
  pipeline[5] = Station(sink=True)
  for i in reversed(range(1, 5)):
    pipeline[i] = Station(succ=pipeline[i+1])
  pipeline[0] = Station(src=True, succ=pipeline[1])

  ticks = range(20)
  for _ in ticks:
    for station in pipeline:
      station.work()

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
