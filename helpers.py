import re


def extract_ip(str):
    ip_addr_without_range = re.findall('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', str)
    return ip_addr_without_range[0]


def get_wireguard_config_file_str(private_key, address, public_key, allowed_ips, endpoint):
    return (f"[Interface]\nPrivateKey = {private_key}\nAddress = {address}\n\n[Peer]\nPublicKey = {public_key}\n"
            f"AllowedIPs = {allowed_ips}\nEndpoint = {endpoint}\nPersistentKeepalive = 25\n")

