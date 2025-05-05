#!/bin/bash

# Run tests for ML Systems Journey
cd "$(dirname "$0")"

if [ ! -d "tests" ]; then
  echo "Error: tests directory not found!"
  exit 1
fi

# Pass all arguments to the Python test runner
python tests/run_tests.py "$@"