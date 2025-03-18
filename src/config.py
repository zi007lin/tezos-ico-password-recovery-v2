import yaml
import os
from dataclasses import dataclass
import logging
import argparse
from typing import Dict, Any
from pathlib import Path

logger = logging.getLogger("TezosPasswordFinder")


@dataclass
class Config:
    email: str = ""
    address: str = ""
    mnemonic: str = ""
    min_length: int = 13
    max_length: int = 64
    component1: str = ""
    component2: str = ""
    component3: str = ""
    component4: str = ""

    @classmethod
    def load(cls, config_path: str = "config.yaml") -> "Config":
        if not os.path.exists(config_path):
            # Create default config
            default_config = cls()
            default_config.save(config_path)
            return default_config

        with open(config_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}

        return cls(
            email=data.get("email", ""),
            address=data.get("address", ""),
            mnemonic=data.get("mnemonic", ""),
            min_length=data.get("password_constraints", {}).get("min_length", 13),
            max_length=data.get("password_constraints", {}).get("max_length", 64),
            component1=data.get("components", {}).get("component1", ""),
            component2=data.get("components", {}).get("component2", ""),
            component3=data.get("components", {}).get("component3", ""),
            component4=data.get("components", {}).get("component4", ""),
        )

    def save(self, config_path: str = "config.yaml"):
        data = {
            "email": self.email,
            "address": self.address,
            "mnemonic": self.mnemonic,
            "password_constraints": {
                "min_length": self.min_length,
                "max_length": self.max_length,
            },
            "components": {
                "component1": self.component1,
                "component2": self.component2,
                "component3": self.component3,
                "component4": self.component4,
            },
        }

        with open(config_path, "w", encoding="utf-8") as f:
            yaml.dump(data, f, default_flow_style=False)


def get_env_config():
    """Get configuration from environment variables"""
    env_prefix = "TEZOS_RECOVERY_"
    env_config = {}

    # Map of environment variables to config keys
    env_mappings = {
        "EMAIL": "email",
        "MNEMONIC": "mnemonic",
        "ADDRESS": "address",
        "COMP1": "comp1",
        "COMP2": "comp2",
        "COMP3": "comp3",
        "COMP4": "comp4",
    }

    # Check each environment variable
    for env_key, config_key in env_mappings.items():
        env_value = os.environ.get(f"{env_prefix}{env_key}")
        if env_value:
            env_config[config_key] = env_value
            logger.info(f"Using environment variable {env_prefix}{env_key}")

    return env_config if env_config else None


def load_config() -> Dict[str, Any]:
    """
    Load configuration with precedence:
    1. Config file (config/config.yml)
    2. Command line arguments
    3. Environment variables
    """
    config = {
        "email": "",
        "mnemonic": "",
        "address": "",
        "comp1": "",
        "comp2": "",
        "comp3": "",
        "comp4": "",
    }

    # 3. Load from environment variables (lowest precedence)
    env_mapping = {
        "TEZOS_EMAIL": "email",
        "TEZOS_MNEMONIC": "mnemonic",
        "TEZOS_ADDRESS": "address",
        "TEZOS_COMP1": "comp1",
        "TEZOS_COMP2": "comp2",
        "TEZOS_COMP3": "comp3",
        "TEZOS_COMP4": "comp4",
    }

    for env_var, config_key in env_mapping.items():
        if os.getenv(env_var):
            config[config_key] = os.getenv(env_var)
            logger.info(f"Loaded {config_key} from environment variable {env_var}")

    # 2. Load from command line arguments (middle precedence)
    parser = argparse.ArgumentParser(description="Tezos Password Recovery")
    parser.add_argument("--email", help="ICO registration email")
    parser.add_argument("--mnemonic", help="Mnemonic phrase")
    parser.add_argument("--address", help="Tezos address (tz1...)")
    parser.add_argument("--comp1", help="First password component")
    parser.add_argument("--comp2", help="Second password component")
    parser.add_argument("--comp3", help="Third password component")
    parser.add_argument("--comp4", help="Fourth password component")

    args = parser.parse_args()

    # Update config with command line arguments if provided
    for key, value in vars(args).items():
        if value is not None:
            config[key] = value
            logger.info(f"Loaded {key} from command line argument")

    # 1. Load from config.yml (highest precedence)
    current_dir = Path(os.getcwd())
    logger.info(f"Current working directory: {current_dir}")

    possible_config_paths = [
        current_dir / "config" / "config.yml",  # ./config/config.yml
        current_dir.parent / "config" / "config.yml",  # ../config/config.yml
        Path.home() / ".config" / "tezos" / "config.yml",  # ~/.config/tezos/config.yml
    ]

    config_loaded = False
    for config_path in possible_config_paths:
        logger.info(f"Trying config path: {config_path}")
        try:
            with open(config_path, "r") as f:
                yaml_config = yaml.safe_load(f)
                if yaml_config:
                    for key in config.keys():
                        if yaml_config.get(key):
                            config[key] = yaml_config[key]
                            logger.info(f"Loaded {key} from config file")
                    config_loaded = True
                    logger.info(f"Successfully loaded config from {config_path}")
                    break
        except FileNotFoundError:
            logger.warning(f"Config file not found at {config_path}")
        except yaml.YAMLError as e:
            logger.error(f"Error parsing config file {config_path}: {e}")
        except Exception as e:
            logger.error(f"Unexpected error reading config file {config_path}: {e}")

    if not config_loaded:
        logger.warning("No config file was successfully loaded")

    # Log final configuration (excluding sensitive data)
    logger.info(
        "Final configuration loaded with values for: "
        + ", ".join(k for k, v in config.items() if v)
    )

    return config
