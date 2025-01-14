#!/bin/bash

# Mimic a traditional cpp

# Separate flags and input files
flags=()
files=()
while [ $# -ne 0 ]; do
    if [ -z "$1" ]; then
        # Ignore empty arguments
        shift
        continue
    fi
    if [ "x$1" = 'x-' ]; then
        # A single hypen is a file (stdin)
        files+=("$1")
        shift
        continue
    fi
    case "$1" in
        -*)
            # We hope that flags don't take arguments...
            flags+=("$1")
            shift
            ;;
        *)
            files+=("$1")
            shift
            ;;
    esac
done
if [ ${#files[@]} -eq 0 ]; then
    # Read from stdin if there are no input files
    files+=('-')
fi
exec cc -E -traditional-cpp -x c "${flags[@]}" "${files[@]}"
