"""Passthrough shim for KeyVault extension."""
import sys

import structlog
from meltano.edk.logging import pass_through_logging_config

from key_vault_ext.extension import KeyVault


def pass_through_cli() -> None:
    """Pass through CLI entry point."""
    pass_through_logging_config()
    ext = KeyVault()
    ext.pass_through_invoker(
        structlog.getLogger("azure_invoker"), *sys.argv[1:] if len(sys.argv) > 1 else []
    )