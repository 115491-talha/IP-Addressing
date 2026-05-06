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
        if host_id < 1 or host_id > self.no_of_hosts:
            raise ValueError(f"Host ID must be between 1 and the number of hosts '{self.no_of_hosts}' in the network")
        
        network_id_octets = self.network_id.octets
        mask_octets = self.mask.octets

        host_ip_octets = []
        for i in range(4):
            host_ip_octets.append(Octet(network_id_octets[i].value | (host_id & ~mask_octets[i].value)))
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
