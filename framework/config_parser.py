import os


class ConfigParser:
    def __init__(self, config_path=None):
        self.config_path = config_path or os.getenv(
            "CONFIG_PATH", "configs/config_perfect.ini"
        )
        self.duplicates = []
        self.invalid_lines = []
        self.config_data = {}
        self._load_config()

    def _load_config(self):
        if not self.config_path.endswith(".ini"):
            raise ValueError(
                f"Invalid file format: {self.config_path}. Expected '.ini' file"
            )
        if not os.path.isfile(self.config_path):
            raise FileNotFoundError(f"Config not found: {self.config_path}")

        current_section = None
        with open(self.config_path, "r", encoding="utf-8") as f:
            for line_num, line in enumerate(f, 1):
                current_section = self._process_line(
                    line.strip(), line_num, current_section
                )

    def _process_line(self, line, line_num, current_section):
        if not line or line.startswith((";", "#")):
            return current_section

        if line.startswith("[") and line.endswith("]"):
            return self._process_section(line, line_num)

        if "=" in line:
            return self._process_key_value(line, line_num, current_section)

        self.invalid_lines.append(f"Line {line_num}: Invalid format '{line}'")

    def _process_section(self, line, line_num):
        section = line[1:-1]
        if section in self.config_data:
            self.duplicates.append(f"Line {line_num}: Duplicate section [{section}]")
        else:
            self.config_data[section] = {}
        return section

    def _process_key_value(self, line, line_num, current_section):
        if current_section is None:
            self.invalid_lines.append(f"Line {line_num}: Key outside section '{line}'")
            return current_section

        key, sep, value = line.partition("=")
        key, value = key.strip(), value.strip()

        if not key:
            self.invalid_lines.append(f"Line {line_num}: Empty key in '{line}'")
        elif key in self.config_data[current_section]:
            self.duplicates.append(
                f"Line {line_num}: Duplicate key '{key}' in section '[{current_section}]'"
            )
        else:
            self.config_data[current_section][key] = value
        return current_section

    def get(self, section, key, default=None):
        return self.config_data.get(section, {}).get(key, default)

    def get_all_config(self):
        return self.config_data.copy()

    def get_duplicates(self):
        return self.duplicates.copy()

    def get_invalid_lines(self):
        return self.invalid_lines.copy()

    def is_valid(self):
        return not (self.duplicates or self.invalid_lines)

    def get_section(self, section):
        return self.config_data.get(section, {}).copy()

    def get_path(self):
        return self.config_path
