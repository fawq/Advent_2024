import os
import sys

if not __package__:
    # Make CLI runnable from source tree with
    #    python src/package
    package_source_path = os.path.dirname(os.path.dirname(__file__))
    sys.path.insert(0, package_source_path)

from advent import day_20, day_21, day_22, day_23

if __name__ == "__main__":
    choosen_part = "day_23"
    match choosen_part:
        case "day_20":
            day_20.main()
        case "day_21":
            day_21.main()
        case "day_22":
            day_22.main()
        case "day_23":
            day_23.main()