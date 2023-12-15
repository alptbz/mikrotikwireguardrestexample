import requests
from requests.auth import HTTPBasicAuth


class RestClientException(Exception):

    def __init__(self, message):
        super().__init__(message)


class RestClientWrapper:

    def __init__(self, host, username: str, password: str, verify_ssl = True):
        self._host = host
        self._api_base_url = f"https://{host}/rest/"
        self._verify_ssl = verify_ssl
        self._basic_auth = HTTPBasicAuth(username, password)

    def create_wireguard_keypair(self):
        wireguard_create_resp = requests.put(f'{self._api_base_url}interface/wireguard', json={'name': 'temp-1234'},
                                             verify=self._verify_ssl, auth=self._basic_auth)
        if wireguard_create_resp.status_code > 399:
            raise RestClientException("Could not create temporary wireguard interface")

        wireguard_created = wireguard_create_resp.json()

        wireguard_delete_resp = requests.delete(f'{self._api_base_url}interface/wireguard/{wireguard_created[".id"]}',
                                                verify=self._verify_ssl, auth=self._basic_auth)

        if wireguard_delete_resp.status_code > 399:
            raise RestClientException("Could not delete temporary wireguard interface")

        return wireguard_created

    def add_wireguard_peer(self, interface: str, public_key: str, allowed_address: str, comment: str = ""):
        data = {'public-key': public_key, 'allowed-address': allowed_address, 'interface': interface, 'comment': comment}
        wireguard_create_resp = requests.put(f'{self._api_base_url}interface/wireguard/peers', json=data,
                                             verify=self._verify_ssl, auth=self._basic_auth)
        if wireguard_create_resp.status_code > 399:
            raise RestClientException(f"Could not add wireguard peer {wireguard_create_resp.content}")

        return wireguard_create_resp.json()

    def _get_get(self, path):
        resp = requests.get(f'{self._api_base_url}{path}', verify=self._verify_ssl,
                                              auth=self._basic_auth)
        if resp.status_code > 399:
            raise RestClientException(f"Could not get {path}")
        return resp.json()

    def get_wireguard_interfaces(self):
        return self._get_get('interface/wireguard')

    def get_ip_addresses(self):
        return self._get_get('ip/address')

    def get_wireguard_peers(self):
        return self._get_get('interface/wireguard/peers')



