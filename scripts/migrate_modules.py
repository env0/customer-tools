"""
This script is designed to migrate your TFC modules into env0.

Prerequisites:
- Python 3
- API key, secret and org ID for env0
- Token and Org name for TFC
- GIT_ADDRESS is github.com by default

Usage:
python3 migrate_modules.py

The script will:
- Retrieve the modules data from TFC
- Create relevant modules in env0.
"""

import clients


TFC_TOKEN = ''
TFC_ORG_NAME = ''

ENV0_API_KEY = ''
ENV0_API_SECRET = ''
ENV0_ORGANIZATION_ID = ''

GIT_ADDRESS = 'github.com'


def get_tfc_providers(
    client,
):
    tfc_providers_list = []
    providers = client.list_providers()
    for provider in providers['data']: 
        enriched_provider = client.get_provider(
            registry_name=provider['attributes']['registry-name'], 
            namespace=provider['attributes']['namespace'], 
            name=provider['attributes']['name'],
        )
        tfc_providers_list.append(enriched_provider)
        
    return tfc_providers_list

def get_tfc_modules(
    client,
):
    tfc_modules_list = []
    modules = client.list_modules()
    for module in modules['data']: 
        enriched_module = client.get_module(
            registry_name=module['attributes']['namespace'], 
            namespace=module['attributes']['registry-name'], 
            provider=module['attributes']['provider'], 
            name=module['attributes']['name'],
        )
        tfc_modules_list.append(enriched_module)
        
    return tfc_modules_list


if __name__ == '__main__':
    tfc_client = clients.tfc_registry.TfcRegistryClient(
        api_token=TFC_TOKEN,
        org_name=TFC_ORG_NAME,
    )
    env0_client = clients.env0.Env0APIClient(
        api_key=ENV0_API_KEY,
        api_secret=ENV0_API_SECRET,
    )
    
    tfc_modules = get_tfc_modules(
      client=tfc_client,
    )
    
    for tfc_module in tfc_modules:
        for inner_data in tfc_module['data']:
            env0_client.create_module(
                module_name=inner_data['attributes']['name'],
                module_provider=inner_data['attributes']['provider'],
                repository=GIT_ADDRESS + inner_data.get('attributes', {}).get('vcs-repo', {}).get('identifier', ''),
                org_id=ENV0_ORGANIZATION_ID
            )
    