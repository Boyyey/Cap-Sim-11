# Makefile for Capacitor Simulator C Library

CC = gcc
CFLAGS = -Wall -Wextra -fPIC -O2
LDFLAGS = -shared

# Target library name
TARGET = libcapacitor_simulator.so

# Source files
SRCS = physics.c simulator.c

# Object files
OBJS = $(SRCS:.c=.o)

# Default target
all: $(TARGET)

# Build shared library
$(TARGET): $(OBJS)
	$(CC) $(LDFLAGS) -o $@ $^ -lm

# Compile source files to object files
%.o: %.c models.h
	$(CC) $(CFLAGS) -c $< -o $@

# Clean target
clean:
	rm -f $(OBJS) $(TARGET)

# Install target (optional)
install: $(TARGET)
	cp $(TARGET) /usr/local/lib/
	ldconfig

# Test target (optional)
test: $(TARGET)
	$(CC) -o test_simulator test_simulator.c -L. -lcapacitor_simulator -lm
	./test_simulator

.PHONY: all clean install test
