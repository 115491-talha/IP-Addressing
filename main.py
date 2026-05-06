from ip import IP, Octet

if __name__ == "__main__":
    ip = IP((Octet(201), Octet(20), Octet(30), Octet(40)))
    # print(ip.__repr__())

    network_id = ip.network_id
    print("Network ID:", network_id)

    host_id = 4
    host = ip.get_host(host_id)
    print(f"Host {host_id}:", host)
