import requests

from . import _http_client


class TfcRegistryClient(
    _http_client.HttpClient,
):
    base_url = 'https://app.terraform.io/api/v2/'
    
    def __init__(
        self,
        api_token,
        org_name,
    ):
        self.api_token = api_token
        self.org_name = org_name
        self.headers = {
            'Authorization': f'Bearer {self.api_token}'
        }
    
    def list_providers(
        self,
    ):   
        response = self.send_request(
            method=requests.get,
            url=f'{self.base_url}organizations/{self.org_name}/registry-providers',
            headers=self.headers,
        )

        return response.json()
    
    def get_provider(
        self,
        registry_name,
        namespace,
        name,
    ):
        response = self.send_request(
            method=requests.get,
            url=f'{self.base_url}organizations/{self.org_name}/registry-providers',
            params={
                'registry_name': registry_name,
                'namespace': namespace,
                'name': name
            },
            headers=self.headers,
        )

        return response.json()
    
    def list_modules(
        self,
    ):
        response = self.send_request(
            method=requests.get,
            url=f'{self.base_url}organizations/{self.org_name}/registry-modules',
            headers=self.headers,
        )

        return response.json()
    
    def get_module(
        self,
        registry_name,
        namespace,
        name,
        provider,
    ):
        response = self.send_request(
            method=requests.get,
            url=f'{self.base_url}organizations/{self.org_name}/registry-modules',
            params={
                'registry_name': registry_name,
                'namespace': namespace,
                'name': name,
                'provider': provider
            },
            headers=self.headers,
        )

        return response.json()
