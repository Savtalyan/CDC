import logging

from simulator import Simulator

logging.basicConfig(
    level = logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)

if __name__ == "__main__":
    Simulator.start()