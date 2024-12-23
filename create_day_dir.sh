#!/bin/bash

main() {
    local day=$(printf "%02d" $1)

    SOURCE="src/advent"
    mkdir -p $SOURCE/day_$day

    [[ -f $SOURCE/day_$day/data.txt ]] || touch $SOURCE/day_$day/data.txt
    [[ -f $SOURCE/day_$day/data_test.txt ]] || touch $SOURCE/day_$day/data_test.txt
    [[ -f $SOURCE/day_$day.py ]] || touch $SOURCE/day_$day.py
}

main "$@"