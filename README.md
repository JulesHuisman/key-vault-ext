# Key Vault Extension

KeyVault is A meltano utility extension for KeyVault that wraps the `az keyvault` command.

## Command

1. Set the following config.

```
config:
    key_vault_name: <The name of your key vault: "example-vault">
    azure_subscription: <The name of your subscription: "subscription">
    azure_tenant: <The name of your tenant: "example.com">
```

2. Login to Azure.

```
meltano invoke key-vault:login
```

3. Set the right permissions on your account. (You might not have rights to do this.)

```
meltano invoke key-vault:set-permission user@domain.com
```

4. Hydrate your .env file.

```
meltano invoke key-vault:hydrate-env
```
