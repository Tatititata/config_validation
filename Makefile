PYTHON = python3
VENV = .venv
PIP = $(VENV)/bin/pip

init: venv_clean $(VENV)/bin/activate

venv_clean:
	@rm -rf .venv || true 

$(VENV)/bin/activate: requirements.txt
	@echo "Creating virtual environment..."
	$(PYTHON) -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	@echo "Virtual environment ready. Use 'make activate'"

activate:
	@echo "Run: source $(VENV)/bin/activate"

.PHONY: clean test help format test-all 

CONFIG_DIR := configs
CONFIGS := $(basename $(notdir $(wildcard $(CONFIG_DIR)/*.ini)))
TEST_RESULT_DIR := test_results

.PHONY: test-all $(CONFIGS) clean

test_all: $(CONFIGS)
	@echo "All tests done"

$(CONFIGS): %: $(CONFIG_DIR)/%.ini | $(TEST_RESULT_DIR)
	@echo "\nTesting config files: $<"
	CONFIG_PATH=$(abspath $<) pytest --tb=short --html=$(TEST_RESULT_DIR)/$*.html || true

$(TEST_RESULT_DIR):
	mkdir -p $(TEST_RESULT_DIR)

help:
	@echo "Available commands:"
	@echo "  make clean       - Remove all generated files"
	@echo "  init
	@echo "  make activate    - "
	@echo "  make test        - Run default test with /var/opt/kaspersky/config.ini"
	@echo "  make test_all    - Run tests with different valid and not valid configs"
	@echo "  make test_config - Run tests with config_perfect.ini"

clean:
	@echo "Cleaning project..."
	@find . -type d -name "__pycache__" -exec rm -rf {} + >/dev/null 2>&1 || true
	@find . -type f -name "*.pyc" -delete >/dev/null 2>&1 || true
	@find . -type f -name "*.pyo" -delete >/dev/null 2>&1 || true
	@find . -type f -name "*.pyd" -delete >/dev/null 2>&1 || true
	@find . -type d -name ".pytest_cache" -exec rm -rf {} + >/dev/null 2>&1 || true
	@find . -type d -name ".mypy_cache" -exec rm -rf {} + >/dev/null 2>&1 || true
	@rm -rf $(TEST_RESULT_DIR) >/dev/null 2>&1 || true
	@echo "Project cleaned!"

test:
	@pytest -v 

test_config:
	CONFIG_PATH=$(CONFIG_DIR)/config_perfect.ini pytest -v 


