from ipaddress import IPv4Network, IPv4Address
from pathlib import Path
from typing import List
import segno
import helpers
from restclientwrapper import RestClientWrapper

# This parameters are required to run the script
HOST = "" # example: 192.168.23.149
VERIFY_SSL = False
USERNAME = '' # example:admin
PASSWORD = '' # example:admin
WIREGUARD_INTERFACE = '' # example:wireguard1
NUM_OF_HOSTS_TO_ADD = 0 # example: 2
OUTPUT_DIR = 'out'
ALLOWED_IPS = "" # example: 192.168.1.0/24
ENDPOINT = "" # example: 192.168.23.149

# Stop here if certain parameters aren't set
assert HOST.strip() != "" and USERNAME.strip() != "" and PASSWORD.strip() != ""


restclient = RestClientWrapper(HOST, USERNAME, PASSWORD, verify_ssl=VERIFY_SSL)

# Get current wireguard interfaces
wireguard_interfaces = restclient.get_wireguard_interfaces()

# Find wireguard interface by name
wireguard_interface = next((x for x in wireguard_interfaces if x['name'] == WIREGUARD_INTERFACE ), None)

# Verify that one interface has been found
assert wireguard_interface is not None

# Add port to ENDPOINT
ENDPOINT = f"{ENDPOINT}:{wireguard_interface['listen-port']}"

ip_addresses = restclient.get_ip_addresses()

# Verify that output directory exists
Path(OUTPUT_DIR).mkdir(exist_ok=True)

# get ip address with subnet for wireguard interface
wireguard_ip_address = next((i for i in ip_addresses if i["interface"] == WIREGUARD_INTERFACE), None)
existing_wireguard_peers = restclient.get_wireguard_peers()

wireguard_network = IPv4Network(wireguard_ip_address['address'],strict=False)

# BEGIN: Create list of free ip addresses
# Get list of all possible ip addresses
hosts: List[IPv4Address] = list(wireguard_network.hosts())
# Get router ip address
router_address = IPv4Address(helpers.extract_ip(wireguard_ip_address['address']))

# Get list of all ip addresses used by already configured wireguard peers
existing_peer_addresses = []
for peer in existing_wireguard_peers:
    if peer["interface"] != WIREGUARD_INTERFACE or peer["allowed-address"].strip() == '':
        continue
    existing_peer_addresses.append(IPv4Address(helpers.extract_ip(peer["allowed-address"])))

# Remove all used ip addresses from list of ip addresses
hosts.remove(router_address)
hosts = [h for h in hosts if h not in existing_peer_addresses]
# END

# Create desired number of hosts
for host_num in range(0, NUM_OF_HOSTS_TO_ADD):
    # Use mikrotik rest api to create keypair
    wg_keypair = restclient.create_wireguard_keypair()
    if len(hosts) == 0:
        print("No free ip addresses left")
    # get next free ip address
    host = hosts.pop(0)
    # add wireguard peer to mikrotik
    restclient.add_wireguard_peer(WIREGUARD_INTERFACE, wg_keypair['public-key'], allowed_address=f'{host}/32')
    # create config file content
    config_file_content = helpers.get_wireguard_config_file_str(wg_keypair['private-key'], f'{host}/32',
                                                                wireguard_interface['public-key'], ALLOWED_IPS,
                                                                ENDPOINT)
    # store config file as text file
    with open(Path(OUTPUT_DIR).joinpath(f'{host}.conf') , 'w') as fp:
        fp.write(config_file_content)

    # store config file as qrcode
    qrcode = segno.make(config_file_content)
    qrcode.save(str(Path(OUTPUT_DIR).joinpath(f'{host}.png')))

    print(f'Created host {host}')
