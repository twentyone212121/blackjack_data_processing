#!/bin/bash

# Get the directory of the script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
GAME_RESULTS_PATH="$SCRIPT_DIR/data/results.myformat"
GAME_OUTPUT_DIR="$SCRIPT_DIR/output/game"

# Run game.py script 12 times
for i in {1..12}; do
    echo "Blackjack CLI game. Round $i"
    python3 "$SCRIPT_DIR/scripts/game.py" $GAME_RESULTS_PATH
    read -p "Press Enter to continue..."
done

# Run process.py script
echo "Running data processing on the game data..."
python3 "$SCRIPT_DIR/scripts/process.py" $GAME_RESULTS_PATH $GAME_OUTPUT_DIR

if [ $? -eq 0 ]; then
    echo "Finished running data processing successfully." 
    echo "Find results in the $GAME_OUTPUT_DIR folder."
else
    echo "Error: Python script encountered an issue."
fi

