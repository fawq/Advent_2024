import os
import sys

if not __package__:
    # Make CLI runnable from source tree with
    #    python src/package
    package_source_path = os.path.dirname(os.path.dirname(__file__))
    sys.path.insert(0, package_source_path)

from advent import day_25

if __name__ == "__main__":
    day_25.main()