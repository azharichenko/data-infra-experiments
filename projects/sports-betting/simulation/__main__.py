from argparse import ArgumentParser

from simulation.models import create_tables
from simulation.scheduler import run_event_loop


# TODO: Create command for strategy registration
# TODO: Create command for backtesting new strategies
# TODO: Create command for database initalization/clean/refresh


def register_all_strategies() -> None:
    pass


def main() -> None:
    parser = ArgumentParser()
    parser.add_argument("--run", action="store_true")

    args = parser.parse_args()

    if args.run:
        create_tables()
        run_event_loop()


if __name__ == "__main__":
    main()
