from typing import Dict

import structlog
from dotenv import dotenv_values

logger = structlog.get_logger()


class Environment:
    def __init__(self, dotenv_path: str) -> None:
        self.dotenv_path = dotenv_path

    @property
    def variables(self) -> Dict[str, str]:
        """Use python-dotenv to load all local variables."""
        return dotenv_values(self.dotenv_path)

    def write_variables(self, variables: Dict[str, str]) -> None:
        """Write all environment variables to a .env file."""
        with open(self.dotenv_path, mode="w") as env_file:
            for variable_name, variable_value in variables.items():
                logger.info(f"Writing {variable_name}")
                env_file.write(f"{variable_name}={variable_value}\n")
