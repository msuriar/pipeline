"""Simulate a pipeline with multiple stations able to produce units of work."""
import random

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
