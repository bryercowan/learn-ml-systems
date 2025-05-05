# ML Systems Journey Tests

This directory contains automated tests to verify the completion of tasks and acceptance criteria for the ML Systems Journey curriculum.

## Overview

The testing framework is designed to check if your implementations meet the acceptance criteria defined in the course README. Tests are organized by module and can be run individually or as a complete suite.

## Setup

To set up the testing environment, run:

```bash
make setup-tests
```

This will install the required dependencies for running the tests.

## Running Tests

### Run all core module tests:

```bash
make test
```

### Run all tests including optional modules:

```bash
make test-all
```

### Run tests for a specific module:

```bash
make test-module-0  # For Module 0
make test-module-1  # For Module 1
make test-module-A  # For Optional Module A
```

### Run tests for a specific sub-module:

```bash
make test-submodule-1-2  # For Module 1-2
make test-submodule-3-4  # For Module 3-4
```

### Run tests inside a container (for CUDA tests):

```bash
make test-container
```

### Run only CUDA-specific tests in container:

```bash
make test-cuda
```

### Run tests for a specific CUDA module:

```bash
make test-module-cuda-1  # For Module 3-1 Vector Add
make test-module-cuda-2  # For Module 3-2 Tiled Mat-Mul
```

### Generate a test report:

```bash
make test-html-report
```

### Run tests with coverage analysis:

```bash
make test-coverage
```

### Analyze test coverage with visualizations:

```bash
python tests/coverage_analysis.py --visualize
```

### List all available tests:

```bash
make list-tests
```

### Initialize test directory structure and placeholder files:

```bash
make init-test-structure
```

### Initialize files for a specific module:

```bash
make init-module-0-A  # For Module 0-A
make init-module-1-2  # For Module 1-2
make init-module-3-1  # For Module 3-1
```

## Test Structure

Each module has its own test file:

- `test_module0.py`: Tests for Module 0 (Course Setup, Kafka Hello-World, DevBox)
- `test_module1.py`: Tests for Module 1 (Data-Plumbing Fundamentals)
- `test_module2.py`: Tests for Module 2 (ML-Workflow Glue)
- `test_module3.py`: Tests for Module 3 (GPU-Performance Mindset)
- `test_module4.py`: Tests for Module 4 (Capstone)
- `test_optional_modules.py`: Tests for Optional Modules A, B, and C

## Test Framework Components

### Core Components

- `run_tests.py`: Main test runner with CLI options and reporting capabilities
- `utils.py`: Common utility functions used across test files
- `conftest.py`: Pytest fixtures for setup/teardown and shared resources

### Advanced Components

- `cuda_helpers.py`: Helper functions for GPU/CUDA testing
- `coverage_analysis.py`: Test coverage analysis and visualization
- `init_module.py`: Module initialization helper
- `init_test_structure.py`: Project structure initializer

## Reporting Features

The testing framework provides several types of test reports:

1. **Text Reports**: Plain text summaries of test results
2. **HTML Reports**: Interactive HTML reports with detailed test results
3. **JSON Reports**: Machine-readable data for CI/CD integration
4. **JUnit XML**: Compatible with common CI systems
5. **Coverage Reports**: Coverage analysis with visualizations

To generate a report, run:

```bash
python tests/run_tests.py --report html --output my_report.html
```

## CUDA Test Integration

The framework includes special support for CUDA tests:

1. **Container-based testing**: Tests run inside NVIDIA Docker containers
2. **Compute capability detection**: Tests adapt to available GPU hardware
3. **CUDA compilation helpers**: Simplifies building CUDA programs for testing
4. **Performance benchmarking**: Tools to measure and validate GPU performance

## Test Coverage Analysis

The coverage analysis tool helps identify untested curriculum components:

1. **Task extraction**: Extracts tasks from the course README
2. **Coverage calculation**: Determines test coverage percentage
3. **Visual reports**: Generates charts showing coverage by module
4. **Recommendations**: Suggests modules needing additional tests

## Troubleshooting

If tests are failing, check:

1. File paths - ensure files are in the expected locations
2. Permissions - make sure scripts are executable 
3. Dependencies - verify all required packages are installed
4. Container issues - for GPU tests, ensure CUDA is properly configured
5. Test output - check the detailed test reports for specific errors

### Common Issues

#### CUDA Tests Failing

- Ensure NVIDIA drivers are properly installed
- Use `make test-cuda` to run tests in a container with CUDA support
- Check `tests/cuda_helpers.py` for GPU compatibility

#### Missing Dependencies

If you encounter dependency errors, try:

```bash
make setup-tests
```

#### Test Report Generation Issues

If report generation fails, ensure you have the required dependencies:

```bash
pip install termcolor matplotlib pytest-cov
```