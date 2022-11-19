import logging
import os
from functools import lru_cache
from typing import Dict, List

from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

logging.getLogger('azure.mgmt.resource').setLevel(logging.WARNING)


class KeyVault:
    vault_url = f"https://{os.environ['KEY_VAULT_NAME']}.vault.azure.net"

    @property
    @lru_cache
    def client(self):
        """The client to connect to Azure Key Vault."""
        credential = DefaultAzureCredential()
        return SecretClient(vault_url=self.vault_url, credential=credential)

    @property
    def all_secrets(self) -> List[str]:
        """Returns all the secret names found in the Key Vault."""
        return [secret.name for secret in self.client.list_properties_of_secrets()]

    def get_secret_value(self, secret_name: str) -> str:
        """Get a specific secret by it's name."""
        return self.client.get_secret(secret_name).value

    def to_upper_snake_case(self, secret_name: str) -> str:
        """Transform a secret-name to UPPER_CASE_SNAKE_CASE."""
        return secret_name.replace("-", "_").upper()

    @property
    def variables(self) -> Dict[str, str]:
        """Get all the variables from key vault and rename them."""
        return {
            self.to_upper_snake_case(secret_name): self.get_secret_value(secret_name)
            for secret_name in self.all_secrets
        }
