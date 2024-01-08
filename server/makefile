CC = gcc
CFLAGS = -std=c17 -Wall -Wextra
SRC_DIR = src
BUILD_DIR = build

# List of source files (assuming you have only one source file for simplicity)
SRC = $(wildcard $(SRC_DIR)/*.c)

# List of object files to build
OBJ = $(patsubst $(SRC_DIR)/%.c, $(BUILD_DIR)/%.o, $(SRC))

EXECUTABLE = $(BUILD_DIR)/server

all: $(BUILD_DIR) $(EXECUTABLE)

$(BUILD_DIR):
	mkdir -p $(BUILD_DIR)

$(EXECUTABLE): $(OBJ)
	$(CC) $(CFLAGS) $^ -o $@

$(BUILD_DIR)/%.o: $(SRC_DIR)/%.c
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	rm -rf $(BUILD_DIR)

.PHONY: all clean
