import random
import socket
from contextlib import closing
from inspect import signature
from typing import List

import ifaddr
from zeroconf import (ServiceBrowser, ServiceInfo, ServiceListener, Zeroconf,
                      ZeroconfServiceTypes)


class MyListener:

    def remove_service(self, zeroconf, type, name):
        print("Service {} of type {} removed".format(name, type))

    def add_service(self, zeroconf, type, name):
        info = zeroconf.get_service_info(type, name)
        print("Service %s added, service info: %s" % (name, info))

        # https://stackoverflow.com/a/51596612/8608146
        print("Address", socket.inet_ntoa(info.address))

        get_level_one_info(info)

# https://stackoverflow.com/a/45690594/8608146


def find_free_port():
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(('', 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]

# https://github.com/p-sanches/somabits/blob/d581abaab6f045d65a774a78fbb43e232cf6f8da/somoserver/SomoServer/ZeroConf.py#L42


def get_all_addresses() -> List[str]:
    return list(set(
        addr.ip
        for iface in ifaddr.get_adapters()
        for addr in iface.ips
        # Host only netmask 255.255.255.255
        if addr.is_IPv4 and addr.network_prefix != 32
    ))


def get_local_ip(starts_with="192"):
    list_ip = get_all_addresses()
    local_ip = [i for i in list_ip if i.startswith(starts_with)]
    return local_ip[0]


def get_level_one_info(obj):
    """Prints all the properties of an object"""
    print("\n"+"---"*9)
    for x in dir(obj):
        if not x.startswith("_"):
            data = getattr(obj, x)
            if callable(data):
                # https://stackoverflow.com/a/41188411/8608146
                sig = signature(data)
                params = sig.parameters

                if len(params) == 0:
                    print(x, ":", data())

            else:
                print(x, ":", data)


# print(get_all_addresses())
# print(get_local_ip())

print(ZeroconfServiceTypes.find())


zeroconf = Zeroconf()

# register a service
zeroconf.register_service(ServiceInfo(
    "_coolapp._udp.local.",
    "{}._coolapp._udp.local.".format(f"pc-{random.randint(0, 255)}"),
    socket.inet_aton(get_local_ip()), find_free_port(), 0, 0,
    # this is the txt record
    properties={"data": "device"}
))

listener = MyListener()
browser = ServiceBrowser(zeroconf, "_coolapp._udp.local.", listener)
try:
    input("Press enter to exit...\n\n")
finally:
    zeroconf.close()
