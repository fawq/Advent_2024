#!/bin/bash

main() {
    local day=$(printf "%02d" $1)

    mkdir -p day_$day

    [[ -f day_$day/data.txt ]] || touch day_$day/data.txt
    [[ -f day_$day/data_test.txt ]] || touch day_$day/data_test.txt
    [[ -f day_$day/part_1.py ]] || touch day_$day/part_1.py
    [[ -f day_$day/part_2.py ]] || touch day_$day/part_2.py
    [[ -L day_$day/utils && -d day_$day/utils ]] || ln -s ../utils day_$day/utils
}

main "$@"