#!/bin/bash

# Set the Python interpreter (adjust if necessary)
PYTHON="python3"

# Generate sample data
echo "Generating sample data..."
$PYTHON generate_sample_data.py

# Perform indexing
echo "Performing indexing..."
$PYTHON indexing.py

echo "Data regeneration and indexing complete!"