# Config Validator Project

A project for **validating INI configuration files** based on predefined rules. It checks for required sections, parameters, and their values.

---

## ⚙️ Environment Setup

### Creating a virtual environment

**For Linux/macOS:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Installation

Install dependencies:
```bash
pip install -r requirements.txt
```

### Running Tests
```bash
# Uses the default config value from the task
pytest 

# With a specific config
CONFIG_PATH=configs/config_perfect.ini pytest 

# With verbose output
CONFIG_PATH=configs/config_perfect.ini pytest -v
```

### Test Run Artifacts

- **HTML reports**: `test_results/` 

## 🗂️ Project Structure

```
├── configs/             # Test configs
│   ├── config_.ini      # Examples of valid and invalid configs
├── framework/           # Parser logic
│   └── config_parser.py
├── tests/               # Autotests
│   └── test_.py
├── Makefile             # Task management
├── requirements.txt     # Dependencies
└── test_cases.md        # Test case descriptions
```

## 📌 Requirements

- Python 3.6+
- Dependencies: `pytest`, `pytest-html`

## 🚀 Using the Makefile

The project includes a Makefile for convenient management of key tasks.  
It can create a virtual environment, run tests, format code, and clean the project.

Main commands:

- `make init` — create and set up a virtual environment, install dependencies from `requirements.txt`  
- `make activate` — activate the virtual environment  
- `make test` — run tests with the default configuration  
- `make test_config` — run tests using `config_perfect.ini`  
- `make test_all` — run tests for all config files in the `configs` folder and generate html reports  
- `make clean` — remove temporary and generated files, clean caches and test results  

---

## 📑 Parameter Table

### Section: General

| Parameter                  | Allowed Values                                                                                      |
|---------------------------|-----------------------------------------------------------------------------------------------------|
| ScanMemoryLimit           | Integer in the range [1024-8192]                                                                    |
| PackageType               | `rpm` / `deb` (case-insensitive)                                                                    |
| ExecArgMax                | Integer in the range [10-100]                                                                       |
| AdditionalDNSLookup       | `true` / `false` / `yes` / `no` (case-insensitive)                                                  |
| CoreDumps                 | `true` / `false` / `yes` / `no` (case-insensitive)                                                  |
| RevealSensitiveInfoInTraces | `true` / `false` / `yes` / `no` (case-insensitive)                                              |
| ExecEnvMax                | Integer in the range [10-100]                                                                       |
| MaxInotifyWatches         | Integer in the range [1000-1000000]                                                                 |
| CoreDumpsPath             | Existing absolute path to a directory in the system                                                 |
| UseFanotify               | `true` / `false` / `yes` / `no` (case-insensitive)                                                  |
| KsvlaMode                 | `true` / `false` / `yes` / `no` (case-insensitive)                                                  |
| MachineId                 | UUID                                                                                                 |
| StartupTraces             | `true` / `false` / `yes` / `no` (case-insensitive)                                                  |
| MaxInotifyInstances       | Integer in the range [1024-8192]                                                                    |
| Locale                    | Language tag in the format defined by RFC 3066                                                      |

---

### Section: Watchdog

| Parameter                  | Allowed Values                                                                                      |
|---------------------------|-----------------------------------------------------------------------------------------------------|
| ConnectTimeout            | Integer in the range [1-120] with `m` suffix (minutes)                                              |
| MaxVirtualMemory          | `off` / `auto` or a float in the range (0, 100]                                                     |
| MaxMemory                 | `off` / `auto` or a float in the range (0, 100]                                                     |
| PingInterval              | Integer in the range [100-10000]                                                                    |