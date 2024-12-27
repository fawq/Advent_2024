import argparse
import os
import sys
from types import ModuleType
from typing import Optional

if not __package__:
    # Make CLI runnable from source tree with
    #    python src/package
    package_source_path = os.path.dirname(os.path.dirname(__file__))
    sys.path.insert(0, package_source_path)

from advent import day_20, day_21, day_22, day_23, day_24, day_25

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='My solutions to Advent of Code 2024')
    parser.add_argument("--day", default=25, type=int, help="Day which to run")
    parser.add_argument("--all", default=False, type=bool, help="Run all days")
    args = parser.parse_args()

    all_days: list[Optional[ModuleType]] = [None]*19 + [day_20, day_21, day_22, day_23, day_24, day_25]

    if args.all:
        for day in all_days:
            if day is not None:
                day.main()
    else:
        index = args.day - 1
        if all_days[index] is not None:
            all_days[index].main()