"""Simulate a pipeline with multiple stations able to produce units of work."""
import random

def main():
  """Set up and run pipeline."""
  pipeline = [None]*6
  pipeline[5] = Station(sink=True)
  for i in range(1, 5).reverse():
    pipeline[i] = Station(succ=i+1)
  pipeline[0] = Station(src=True, succ=1)

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
    if not self.sink:
      throughput = min(self.total, random.choice(range(1, 7)))
      self.succ.total += throughput
