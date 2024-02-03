# Automatic tauri updates including CI integration

```console
# Password is 123123
cargo tauri signer generate -w .tauri/app.key
```

Set in Github secrets for action:
```console
export TAURI_PRIVATE_KEY="dW50cnVzdGVkIGNvbW1lbnQ6IHJzaWduIGVuY3J5cHRlZCBzZWNyZXQga2V5ClJXUlRZMEl5a1hsMHhLUTQrWHoveDVzQkRDU3k1UmZnT3IwcmtWcndaU1NmeDFvRE5mY0FBQkFBQUFBQUFBQUFBQUlBQUFBQVVnMVdpcm9ETzdHT1RVb1doeFpSL3B2cUJKOGFpV3ZpL09UbVFUMDliOGZTbU80VjFobnhkNmNwdnA0OUhiN0p4eHFySm9DMHcrT2plc0VpWi9haHR0WjlmTGpBUHJXMzZicG0xdHdxb0ZMS1BKaFZRYURBYTBha1ZZbW9EdmttWWRFOElQdUlWclU9Cg=="
export TAURI_KEY_PASSWORD="123123"
```

For changing version to next one:
1. Increment version in `tauri.conf.json` and `Cargo.toml`
2. Push and trigger workflow
3. Wait for finish and publish the drafted release
4. 
Thtat's all, automatic update will be send to users...
