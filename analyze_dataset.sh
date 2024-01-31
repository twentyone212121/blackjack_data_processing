#!/bin/bash

# Get the directory of the script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
DATASET_PATH="$SCRIPT_DIR/data/blkjckhands.csv"
DATASET_OUTPUT_DIR="$SCRIPT_DIR/output/900k"

# Run process.py script
echo "Running data processing on the dataset (900k entries)..."
python3 "$SCRIPT_DIR/scripts/process.py" $DATASET_PATH $DATASET_OUTPUT_DIR

if [ $? -eq 0 ]; then
    echo "Finished running data processing successfully." 
    echo "Find results in the $DATASET_OUTPUT_DIR folder."
else
    echo "Error: Python script encountered an issue."
fi

