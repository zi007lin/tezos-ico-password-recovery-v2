import yaml
import os
from dataclasses import dataclass
import logging

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


def load_config(exe_path=None):
    """Load configuration with priority: ENV > YAML > Command Line"""
    config = {}

    try:
        # First try environment variables (highest priority)
        env_config = get_env_config()
        if env_config:
            config.update(env_config)
            logger.info("Using environment variables for configuration")

        # Then try YAML file
        if not config:  # Only if no env vars found
            if exe_path:
                config_dir = os.path.dirname(exe_path)
            else:
                config_dir = os.path.dirname(os.path.abspath(__file__))

            config_path = os.path.join(config_dir, "TezosPasswordRecovery.yml")

            if os.path.exists(config_path):
                with open(config_path, "r") as f:
                    yaml_config = yaml.safe_load(f)
                    if yaml_config:
                        config.update(yaml_config)
                        logger.info(f"Using configuration from {config_path}")

    except Exception as e:
        logger.error(f"Error loading config: {str(e)}")

    return config if config else None
