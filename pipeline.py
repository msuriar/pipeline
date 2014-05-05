"""Simulate a pipeline with multiple stations able to produce units of work."""
import random

def main():
  """Set up and run pipeline."""
  pipe = Pipeline(6)
  ticks = range(20)
  for _ in ticks:
    print pipe.summary
    pipe.tick()

class Pipeline(object):
  """Pipeline class."""
  def __init__(self, length, minwork=1, maxwork=7):
    self.length = length
    self.minwork = minwork
    self.maxwork = maxwork
    self.stations = self.__buildpipeline()
    self.ticks = 0

  def __buildpipeline(self):
    """Construct pipeline."""
    pipe = [None]*self.length
    pipe[-1] = Station(minwork=self.minwork, maxwork=self.maxwork)
    for i in reversed(range(1, self.length - 1)):
      pipe[i] = Station(succ=pipe[i+1], minwork=self.minwork,
          maxwork=self.maxwork)
    pipe[0] = Station(src=True, succ=pipe[1], minwork=self.minwork,
        maxwork=self.maxwork)
    return pipe

  def __str__(self):
    return ' ---> '.join([str(s) for s in self.stations])

  def tick(self):
    """Advance pipeline."""
    for station in self.stations:
      station.tick()
    self.ticks += 1

  @property
  def summary(self):
    """Summary of pipeline."""
    output = "WIP: {}; Done: {}; Throughput: {}"
    return output.format(self.work_in_progress, self.completed_work,
        self.throughput)

  @property
  def work_in_progress(self):
    """Work in progress across pipeline."""
    return sum((s.work_in_progress for s in self.stations))

  @property
  def completed_work(self):
    """Completed work across pipeline."""
    return sum((s.completed_work for s in self.stations))

  @property
  def throughput(self):
    """Throughput of this pipeline at this point in time."""
    if self.ticks != 0:
      return float(self.completed_work)/self.ticks
    else:
      return 0

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
      return "[{}||{}]".format(self.in_q, self.out_q)
    else:
      return "[{},{}]".format(self.in_q, self.out_q)

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

  @property
  def work_in_progress(self):
    """Work in progress at this station."""
    if self.src:
      return self.out_q
    elif self.sink:
      return self.in_q
    else:
      return self.in_q + self.out_q

  @property
  def completed_work(self):
    """Completed work at this station."""
    if self.sink:
      return self.out_q
    else:
      return 0

if __name__ == "__main__":
  main()
