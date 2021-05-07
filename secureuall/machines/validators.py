from django.core.exceptions import ValidationError
import re
ipRegex = r"[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+"
dnsRegex = r"([a-zA-Z0-9]([-a-zA-Z0-9]{0,61}[a-zA-Z0-9])?\.){0,2}([a-zA-Z0-9]{1,2}([-a-zA-Z0-9]{0,252}[a-zA-Z0-9])?)\.([a-zA-Z]{2,63})"


def validate_dns(dns):
    if dns and not re.fullmatch(dnsRegex, dns):
        return False
    return True


def validate_ip(ip):
    if ip and not re.fullmatch(ipRegex, ip):
        return False
    return True
