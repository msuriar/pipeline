"""Generate statistics from pipeline runs."""
import pipeline

def main():
  """Set up and run pipeline."""
  pipe = pipeline.Pipeline(6)
  ticks = range(20)
  for _ in ticks:
    print pipe.summary
    pipe.tick()

if __name__ == "__main__":
  main()
