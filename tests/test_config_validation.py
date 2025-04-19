import pytest
import os

# import uuid
from framework.config_parser import ConfigParser
import re


@pytest.fixture(scope="module")
def validator():
    try:
        return ConfigParser()
    except (FileNotFoundError, ValueError) as e:
        pytest.skip(f"Skipping tests: {str(e)}")


def test_config_is_valid(validator):
    assert validator.is_valid(), (
        f"Config file contains errors:\n"
        f"Duplicates: {validator.get_duplicates()}\n"
        f"Invalid lines: {validator.get_invalid_lines()}"
    )


def validate_locale(locale_str):
    pattern = r"^[a-zA-Z]{2,3}(?:_[a-zA-Z]{2})?(?:\.[a-zA-Z0-9-]+)?$"  # POSIX
    # pattern = r'^[a-zA-Z]{2,3}(?:-[a-zA-Z]{2})?$' # RFC 3066
    return bool(re.fullmatch(pattern, locale_str))


def is_float(v):
    try:
        float(v)
        return True
    except ValueError:
        return False


PARAM_VALIDATORS = {
    "General": {
        "ScanMemoryLimit": lambda v: v.isdigit() and 1024 <= int(v) <= 8192,
        "PackageType": lambda v: v.lower() in ["rpm", "deb"],
        "ExecArgMax": lambda v: v.isdigit() and 10 <= int(v) <= 100,
        "AdditionalDNSLookup": lambda v: v.lower() in ["true", "false", "yes", "no"],
        "CoreDumps": lambda v: v.lower() in ["true", "false", "yes", "no"],
        "RevealSensitiveInfoInTraces": lambda v: v.lower()
        in ["true", "false", "yes", "no"],
        "ExecEnvMax": lambda v: v.isdigit() and 10 <= int(v) <= 100,
        "MaxInotifyWatches": lambda v: v.isdigit() and 1000 <= int(v) <= 1000000,
        "CoreDumpsPath": lambda v: os.path.isabs(v) and os.path.isdir(v),
        "UseFanotify": lambda v: v.lower() in ["true", "false", "yes", "no"],
        "KsvlaMode": lambda v: v.lower() in ["true", "false", "yes", "no"],
        "MachineId": lambda v: re.fullmatch(
            r"^[0-9a-f]{8}-([0-9a-f]{4}-){3}[0-9a-f]{12}$", v, re.I
        ),
        "StartupTraces": lambda v: v.lower() in ["true", "false", "yes", "no"],
        "MaxInotifyInstances": lambda v: v.isdigit() and 1024 <= int(v) <= 8192,
        "Locale": validate_locale,
    },
    "Watchdog": {
        "ConnectTimeout": lambda v: v.endswith("m")
        and v[:-1].isdigit()
        and 1 <= int(v[:-1]) <= 120,
        "MaxVirtualMemory": lambda v: v.lower() in ["auto", "off"]
        or (is_float(v) and 0 < float(v) <= 100),
        "MaxMemory": lambda v: v.lower() in ["auto", "off"]
        or (is_float(v) and 0 < float(v) <= 100),
        "PingInterval": lambda v: v.isdigit() and 100 <= int(v) <= 10000,
    },
}

REQUIRED_SECTIONS = set(PARAM_VALIDATORS.keys())


def test_required_sections_exist(validator):
    config_sections = set(validator.get_all_config().keys())
    missing_sections = REQUIRED_SECTIONS - config_sections
    assert (
        not missing_sections
    ), f"Missing required sections: {', '.join(sorted(missing_sections))}"


def test_no_unknown_sections(validator):
    config_sections = set(validator.get_all_config().keys())
    unknown_sections = config_sections - REQUIRED_SECTIONS
    assert (
        not unknown_sections
    ), f"Unknown sections detected: {', '.join(sorted(unknown_sections))}"


def test_no_extra_parameters(validator):
    config_data = validator.get_all_config()

    for section in REQUIRED_SECTIONS & set(config_data.keys()):
        section_params = set(config_data[section].keys())
        allowed_params = set(PARAM_VALIDATORS[section].keys())
        extra_params = section_params - allowed_params

        assert (
            not extra_params
        ), f"Invalid parameters in section [{section}]: {', '.join(sorted(extra_params))}"


@pytest.mark.parametrize(
    "section,param",
    [
        (section, param)
        for section in PARAM_VALIDATORS
        for param in PARAM_VALIDATORS[section]
    ],
)
def test_parameter_values(validator, section, param):
    if section not in validator.get_all_config():
        pytest.skip(f"Section [{section}] not found")

    value = validator.get(section, param)
    assert value is not None, f"Parameter {param} missing in section [{section}]"
    assert PARAM_VALIDATORS[section][param](
        value
    ), f"Invalid value for [{section}]/{param}: {value}"


def test_no_duplicate_sections(validator):
    duplicates = [d for d in validator.get_duplicates() if "Duplicate section" in d]
    assert not duplicates, f"Found duplicate sections: {duplicates}"


def test_no_duplicate_keys(validator):
    duplicates = [d for d in validator.get_duplicates() if "Duplicate key" in d]
    assert not duplicates, f"Found duplicate keys: {duplicates}"


def test_no_invalid_lines(validator):
    assert not validator.get_invalid_lines(), "Found invalid lines in config file"
