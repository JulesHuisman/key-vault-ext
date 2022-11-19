"""Meltano KeyVault extension."""
from __future__ import annotations

import os
import pkgutil
import subprocess
import sys
from pathlib import Path
from typing import Any

import structlog
from meltano.edk import models
from meltano.edk.extension import ExtensionBase
from meltano.edk.process import Invoker, log_subprocess_error

from key_vault_ext.environment import Environment
from key_vault_ext.key_vault import KeyVault

log = structlog.get_logger()


class KeyVaultExtension(ExtensionBase):
    """Extension implementing the ExtensionBase interface."""

    def __init__(self) -> None:
        """Initialize the extension."""
        self.keyvault_bin = "az"  # verify this is the correct name
        self.keyvault_invoker = Invoker(self.keyvault_bin)

    def invoke(self, command_name: str | None, *command_args: Any) -> None:
        """Invoke the underlying cli, that is being wrapped by this extension.

        Args:
            command_name: The name of the command to invoke.
            command_args: The arguments to pass to the command.
        """
        try:
            self.keyvault_invoker.run_and_log(command_name, *command_args)
        except subprocess.CalledProcessError as err:
            log_subprocess_error(f"keyvault {command_name}", err, "KeyVault invocation failed")
            sys.exit(err.returncode)

    def describe(self) -> models.Describe:
        """Describe the extension.

        Returns:
            The extension description
        """
        return models.Describe(
            commands=[
                models.ExtensionCommand(
                    name="keyvault_extension",
                    description="extension commands",
                ),
                models.InvokerCommand(
                    name="keyvault_invoker",
                    description="pass through invoker",
                ),
            ]
        )

    def hydrate(self) -> None:
        """
        Fetch secrets from Azure Key Vault and store them in a .env file.
        """
        environment = Environment(".env")
        key_vault = KeyVault()

        variables = {
            **environment.variables,
            **key_vault.variables,
        }

        environment.write_variables(variables)
