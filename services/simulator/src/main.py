import logging

from simulator import Simulator
from sqlalchemy import create_engine

import config
from models import Base

engine = create_engine(config.DATABASE_URL)
Base.metadata.create_all(engine)
engine.dispose()

logging.basicConfig(
    level = logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)

if __name__ == "__main__":
    Simulator.start()