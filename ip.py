from ipclass import Class, get_class

class Octet:
    def __init__(self, value : 0):
        if not (0 <= value <= 255):
            raise ValueError("Octet value must be between 0 and 255")
        self.__value: int = value

    @property
    def value(self) -> int:
        return self.__value

    def __str__(self):
        return str(self.value)

class IP:
    def __init__(self, octets: tuple[Octet, Octet, Octet, Octet]):
        self.__octets: tuple = octets
    
    @property
    def is_last_ip(self) -> bool:
        return all(octet.value == 255 for octet in self.__octets)

    @property
    def ip_class(self) -> Class:
        return get_class(self.__octets[0].value)
    
    @property
    def octets(self) -> tuple[Octet, Octet, Octet, Octet]:
        return self.__octets
    
    @property
    def no_of_networks(self) -> int:
        _class = self.ip_class

        match _class:
            case Class.A:
                return 2 ** 7 - 2
            case Class.B:
                return 2 ** 14 - 2
            case Class.C:
                return 2 ** 21 - 2
            case Class.D | Class.E:
                return 0
 
    @property
    def no_of_hosts(self) -> int:
        _class = self.ip_class

        match _class:
            case Class.A:
                return 2 ** 24 - 2
            case Class.B:
                return 2 ** 16 - 2
            case Class.C:
                return 2 ** 8 - 2
            case Class.D | Class.E:
                return 0
            
    @property
    def mask(self) -> 'IP':
        _class = self.ip_class

        match _class:
            case Class.A:
                return IP((Octet(255), Octet(0), Octet(0), Octet(0)))
            case Class.B:
                return IP((Octet(255), Octet(255), Octet(0), Octet(0)))
            case Class.C:
                return IP((Octet(255), Octet(255), Octet(255), Octet(0)))
            case Class.D | Class.E:
                return IP((Octet(0), Octet(0), Octet(0), Octet(0)))

    @property
    def network_id(self) -> 'IP':
        return IP(tuple(Octet(self.octets[i].value & self.mask.octets[i].value) for i in range(4)))

    def get_host(self, host_id: int) -> 'IP':
        # ! Host ID starts from 1, not 0, because 0 is reserved for the network ID and the last IP is reserved for the broadcast address
        if host_id < 1 or host_id > self.no_of_hosts:
            raise ValueError(f"Host ID must be between 1 and the number of hosts '{self.no_of_hosts}' in the network")
        
        # * To get the host IP, we need to combine the network ID with the host ID. The host ID is represented in the last octets of the IP address, and we can use bitwise operations to calculate the host IP.
        network_id_octets = self.network_id.octets
        # * The mask octets are used to determine how many bits are used for the network ID and how many bits are used for the host ID. We can use the mask octets to calculate the host IP by performing a bitwise OR operation between the network ID octets and the host ID, while also ensuring that we only consider the bits that are relevant for the host ID (i.e., the bits that are not part of the network ID).
        mask_octets = self.mask.octets

        # ? We need to shift the host ID to the right by the number of bits used for the network ID in each octet, which is determined by the mask octets. This is done to ensure that we are only considering the bits that are relevant for the host ID when performing the bitwise OR operation.
        host_ip_octets = []
        for i in range(4):
            # * The bitwise OR operation combines the network ID octet with the host ID, while also ensuring that we only consider the bits that are relevant for the host ID by using the mask octets. The host ID is shifted to the right by the number of bits used for the network ID in each octet to ensure that we are only considering the bits that are relevant for the host ID.
            host_ip_octets.append(Octet(network_id_octets[i].value | (host_id & ~mask_octets[i].value)))
            
            # * After calculating the host IP octet, we need to shift the host ID to the right by the number of bits used for the network ID in each octet to prepare for the next iteration of the loop, where we will calculate the next host IP octet. This is done to ensure that we are correctly calculating the host IP for each octet based on the remaining bits of the host ID.
            host_id >>= (8 - mask_octets[i].value.bit_length())
        
        return IP(tuple(host_ip_octets))

    def __str__(self):
        return ".".join(str(octet) for octet in self.__octets)
    
    def __repr__(self):
        return f"""{'*' * 20} {id(self)} {'*' * 20}
IP:         {self}
Class:      {self.ip_class.name}
Last IP:    {self.is_last_ip}
Networks:   {self.no_of_networks}
Hosts:      {self.no_of_hosts}"""
