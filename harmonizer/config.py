"""
Configuration Manager for Python Code Harmonizer.
Loads settings from pyproject.toml or harmonizer.yaml.
"""

import os
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

# Try to import tomli for TOML parsing
try:
    import tomli
except ImportError:
    # Fallback for Python 3.11+
    try:
        import tomllib as tomli
    except ImportError:
        tomli = None

# Try to import yaml
try:
    import yaml
except ImportError:
    yaml = None


@dataclass
class HarmonizerConfig:
    # Thresholds
    max_disharmony: float = 1.0
    max_imbalance: float = 0.8
    min_density: float = 0.1

    # Paths
    exclude_patterns: List[str] = field(
        default_factory=lambda: [
            "venv",
            ".venv",
            "__pycache__",
            ".git",
            "build",
            "dist",
            ".pytest_cache",
            "tests",
        ]
    )
    report_output: str = "harmonizer_report.html"

    # Analysis
    complexity_weight: float = 0.2  # For dynamic simulation
    custom_vocabulary: Dict[str, str] = field(default_factory=dict)
    source_path: Optional[str] = None
    root_dir: Optional[str] = None


class ConfigLoader:
    _YAML_FILENAMES = (
        ".harmonizer.yml",
        ".harmonizer.yaml",
        "harmonizer.yml",
        "harmonizer.yaml",
    )

    @staticmethod
    def load(target_dir: str = ".", search_parents: bool = False) -> HarmonizerConfig:
        """
        Load configuration from target directory.
        Priority:
        1. harmonizer.yaml / .harmonizer.yaml / .harmonizer.yml
        2. pyproject.toml
        3. Defaults
        """
        config = HarmonizerConfig()
        config.root_dir = os.path.abspath(target_dir)

        config_path, config_type = ConfigLoader._locate_config_path(target_dir, search_parents)
        if not config_path:
            return config

        try:
            if config_type == "toml":
                ConfigLoader._load_from_pyproject(config, config_path)
            else:
                ConfigLoader._load_from_yaml(config, config_path)
        except Exception as exc:  # pragma: no cover - defensive logging
            print(f"Warning: Failed to load {config_path}: {exc}")
            return config

        config.source_path = config_path
        config.root_dir = os.path.dirname(config_path)
        return config

    @staticmethod
    def load_nearest(start_dir: str = ".") -> HarmonizerConfig:
        """
        Load configuration searching parent directories for the first config file.
        """
        return ConfigLoader.load(start_dir, search_parents=True)

    @staticmethod
    def _update_config(config: HarmonizerConfig, data: Dict[str, Any]):
        """Update config object with dictionary data"""
        if "thresholds" in data:
            t = data["thresholds"]
            if "max_disharmony" in t:
                config.max_disharmony = float(t["max_disharmony"])
            if "max_imbalance" in t:
                config.max_imbalance = float(t["max_imbalance"])
            if "min_density" in t:
                config.min_density = float(t["min_density"])

        if "analysis" in data:
            a = data["analysis"]
            if "complexity_weight" in a:
                config.complexity_weight = float(a["complexity_weight"])

        if "paths" in data:
            p = data["paths"]
            if "exclude" in p:
                config.exclude_patterns = list(p["exclude"])
            if "report" in p:
                config.report_output = p["report"]

        if "exclude" in data:
            config.exclude_patterns = list(data["exclude"])

        if "custom_vocabulary" in data:
            custom_vocab = data.get("custom_vocabulary") or {}
            # Merge so later sources can override defaults
            config.custom_vocabulary.update(custom_vocab)

    @staticmethod
    def _locate_config_path(
        start_dir: str, search_parents: bool
    ) -> Tuple[Optional[str], Optional[str]]:
        current_dir = os.path.abspath(start_dir)
        while True:
            for filename in ConfigLoader._YAML_FILENAMES:
                candidate = os.path.join(current_dir, filename)
                if os.path.exists(candidate) and yaml:
                    return candidate, "yaml"

            toml_path = os.path.join(current_dir, "pyproject.toml")
            if os.path.exists(toml_path) and tomli:
                return toml_path, "toml"

            if not search_parents:
                break

            parent_dir = os.path.dirname(current_dir)
            if parent_dir == current_dir:
                break
            current_dir = parent_dir

        return None, None

    @staticmethod
    def _load_from_yaml(config: HarmonizerConfig, path: str) -> None:
        if not yaml:
            raise RuntimeError("PyYAML is not installed")

        with open(path, "r", encoding="utf-8") as handle:
            data = yaml.safe_load(handle) or {}
            if data:
                ConfigLoader._update_config(config, data)

    @staticmethod
    def _load_from_pyproject(config: HarmonizerConfig, path: str) -> None:
        if not tomli:
            raise RuntimeError("tomli/tomllib is not available for TOML parsing")

        with open(path, "rb") as handle:
            data = tomli.load(handle)

        tool_config = data.get("tool", {}).get("harmonizer", {})
        if tool_config:
            ConfigLoader._update_config(config, tool_config)
