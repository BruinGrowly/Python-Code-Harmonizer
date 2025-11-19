"""
Configuration Manager for Python Code Harmonizer.
Loads settings from pyproject.toml or harmonizer.yaml.
"""

import os
import sys
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

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


class ConfigLoader:
    @staticmethod
    def load(target_dir: str = ".") -> HarmonizerConfig:
        """
        Load configuration from target directory.
        Priority:
        1. harmonizer.yaml
        2. pyproject.toml
        3. Defaults
        """
        config = HarmonizerConfig()

        # 1. Try harmonizer.yaml
        yaml_path = os.path.join(target_dir, "harmonizer.yaml")
        if os.path.exists(yaml_path) and yaml:
            try:
                with open(yaml_path, "r", encoding="utf-8") as f:
                    data = yaml.safe_load(f)
                    if data:
                        ConfigLoader._update_config(config, data)
                print(f"Loaded config from {yaml_path}")
                return config
            except Exception as e:
                print(f"Warning: Failed to load {yaml_path}: {e}")

        # 2. Try pyproject.toml
        toml_path = os.path.join(target_dir, "pyproject.toml")
        if os.path.exists(toml_path) and tomli:
            try:
                with open(toml_path, "rb") as f:
                    data = tomli.load(f)
                    tool_config = data.get("tool", {}).get("harmonizer", {})
                    if tool_config:
                        ConfigLoader._update_config(config, tool_config)
                        print(f"Loaded config from {toml_path}")
            except Exception as e:
                print(f"Warning: Failed to load {toml_path}: {e}")

        return config

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

        if "paths" in data:
            p = data["paths"]
            if "exclude" in p:
                config.exclude_patterns = p["exclude"]
            if "report" in p:
                config.report_output = p["report"]

        if "analysis" in data:
            a = data["analysis"]
            if "complexity_weight" in a:
                config.complexity_weight = float(a["complexity_weight"])
