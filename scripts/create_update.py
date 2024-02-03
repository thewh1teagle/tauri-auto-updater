import requests
import json
from typing import List
from pathlib import Path
import fnmatch
import requests
from datetime import datetime, timezone
import sys

USERNAME = 'thewh1teagle'
REPO = 'tauri-auto-updater'


# Windows x86 not supported in updater platforms
# Patterns to match against updater platforms
PLATFORMS = {
    '*aarch64.app*': 'darwin-aarch64',
    '*x64.app*': 'darwin-x86_64',
    '*x86_64.app*': 'darwin-x86_64',
    '*AppImage.tar.gz*': 'linux-x86_64',
    '*x64-setup.nsis*': 'windows-x86_64',
    # '*x64_*.msi.zip*': 'windows-x86_64'
}

def get_updater_platform(name: str):
    for pattern, platform in PLATFORMS.items():
        if fnmatch.fnmatch(name, pattern):
            return platform
    raise Exception(f'Platform not found for {name}')

def get_releases(username, repo):
    url = f'https://api.github.com/repos/{username}/{repo}/releases/latest'
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def create_signatures(assets: List[dict]):
    assets_names = [i['name'] for i in assets]
    signatures = []
    for asset in assets:
        name = asset['name']
        if '.sig' in name or not any(i in name for i in ('.tar.gz', '.zip')):
            continue
            # Linux / MacOS
        sig = next((i for i in assets if i['name'] == f'{name}.sig'), None)
        if not sig:
            print(f'Sig not found for {name}', file=sys.stderr)
            continue
        try:
            platform = get_updater_platform(name)
        except Exception as e:
            print(e, file=sys.stderr)
            continue
        signature_url = sig['browser_download_url']
        sig_resp = requests.get(signature_url)
        sig_resp.raise_for_status()
        target_data = {'platform': platform, 'signature': sig_resp.text, 'url': asset['browser_download_url']}
        signatures.append(target_data)
    return signatures

def create_update_json(version: str, signatures: List[dict], notes: str = None):
    now_utc = datetime.now(timezone.utc)
    pub_date = now_utc.strftime("%Y-%m-%dT%H:%M:%SZ")

    update = {
        'version': version,
        'pub_date': pub_date,
        'platforms': {}
    }
    for signature in signatures:
        platform = signature['platform']
        url = signature['url']
        signature_str = signature['signature']
        
        update['platforms'][platform] = {
            'url': url,
            'signature': signature_str,
        }
    return update

def get_update(username, repo):
    release = get_releases(username, repo)
    version: str = release['tag_name']
    notes = None
    signatures = create_signatures(release['assets'])
    update = create_update_json(version, signatures)
    return json.dumps(update, indent=4)


update = get_update(USERNAME, REPO)
print(update)
