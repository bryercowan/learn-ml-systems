.PHONY: test test-all test-container setup-tests clean test-coverage test-cuda test-module-cuda-% test-html-report

# Default target
test:
	@echo "Running core module tests..."
	@python tests/run_tests.py

# Run all tests including optional modules
test-all:
	@echo "Running all tests including optional modules..."
	@python tests/run_tests.py --all

# Run tests in container (for CUDA tests)
test-container:
	@echo "Running tests inside container (for CUDA tests)..."
	@docker run --rm -it --gpus all -v $(PWD):/ws -w /ws nvcr.io/nvidia/pytorch:24.03-py3 \
		bash -c "cd /ws && pip install -r tests/requirements.txt && python tests/run_tests.py --container"

# Run tests only for CUDA modules (3-1 to 3-6)
test-cuda:
	@echo "Running CUDA-specific tests..."
	@docker run --rm -it --gpus all -v $(PWD):/ws -w /ws nvcr.io/nvidia/pytorch:24.03-py3 \
		bash -c "cd /ws && pip install -r tests/requirements.txt && python tests/run_tests.py --container --module 3"

# Run tests for a specific CUDA module
test-module-cuda-%:
	@echo "Running container tests for CUDA module 3-$*..."
	@docker run --rm -it --gpus all -v $(PWD):/ws -w /ws nvcr.io/nvidia/pytorch:24.03-py3 \
		bash -c "cd /ws && pip install -r tests/requirements.txt && python tests/run_tests.py --container --module 3 --sub-module $*"

# Run specific module tests
test-module-%:
	@echo "Running tests for module $*..."
	@python tests/run_tests.py --module $*

# Run specific sub-module tests
test-submodule-%:
	@module=$$(echo $* | cut -d '-' -f 1); \
	submodule=$$(echo $* | cut -d '-' -f 2); \
	echo "Running tests for module $$module, sub-module $$submodule..."; \
	python tests/run_tests.py --module $$module --sub-module $$submodule

# Generate HTML test report
test-html-report:
	@echo "Running tests and generating HTML report..."
	@python tests/run_tests.py --report html --output test_report.html

# Run tests with coverage analysis
test-coverage:
	@echo "Running tests with coverage analysis..."
	@pytest tests/ --cov=./ --cov-report=term --cov-report=html:coverage_report

# Setup test environment
setup-tests:
	@echo "Setting up test environment..."
	@pip install -r tests/requirements.txt

# List all available tests
list-tests:
	@python tests/run_tests.py --list

# Initialize test directory structure
init-test-structure:
	@echo "Initializing test directory structure..."
	@python tests/init_test_structure.py

# Initialize a specific module
init-module-%:
	@echo "Initializing module $*..."
	@python tests/init_module.py $*

# Clean up 
clean:
	@echo "Cleaning up..."
	@find . -name "__pycache__" -type d -exec rm -rf {} +
	@find . -name "*.pyc" -delete
	@find . -name ".pytest_cache" -type d -exec rm -rf {} +
	@find . -name "coverage_report" -type d -exec rm -rf {} +
	@find . -name "test_report.*" -delete