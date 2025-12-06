from Business.Basic_Components.Bus import Bus
from Business.Basic_Components.Bit import Bit

class SystemBus:
    """
    Bus del sistema principal con arbitraje
    Conecta CPU, memoria y dispositivos de E/S
    """
    
    def __init__(self, data_width: int = 16, addr_width: int = 12):
        # Buses principales
        self.data_bus = Bus(data_width, 0)
        self.address_bus = Bus(addr_width, 0)
        self.control_bus = Bus(8, 0)
        
        # Dispositivos conectados
        self.devices = []
        
        # Señales de arbitraje
        self.bus_request = Bit(0)
        self.bus_grant = Bit(0)
        self.current_master = None
        
        # Temporización
        self.clock_cycles = 0
    
    def connect_device(self, device, name: str, address_range: tuple, device_type: str = "slave"):
        """
        Conecta un dispositivo al bus
        
        Args:
            device: Objeto del dispositivo (debe tener read/write)
            name: Nombre identificador
            address_range: (start_addr, end_addr)
            device_type: "master" (CPU) o "slave" (memoria, E/S)
        """
        self.devices.append({
            'name': name,
            'device': device,
            'address_range': address_range,
            'type': device_type
        })
        
        print(f"Dispositivo {name} conectado al bus (rango: {address_range[0]:04X}-{address_range[1]:04X})")
    
    def find_device(self, address: int):
        """Encuentra el dispositivo que maneja una dirección"""
        for dev in self.devices:
            start, end = dev['address_range']
            if start <= address <= end:
                return dev, address - start  # Devuelve dispositivo y dirección relativa
        return None, None
    
    def read(self, address: int, master_name: str = None) -> Bus:
        """
        Lee de la dirección especificada
        
        Args:
            address: Dirección absoluta
            master_name: Nombre del maestro que solicita (para arbitraje)
            
        Returns:
            Bus con el dato leído
        """
        if master_name and not self._request_bus(master_name):
            return Bus(self.data_bus.width, 0)
        
        # Colocar dirección en el bus
        self.address_bus.set_Binary_value(address)
        
        # Buscar dispositivo
        dev_info, rel_addr = self.find_device(address)
        if dev_info:
            # Leer del dispositivo
            data = dev_info['device'].read(rel_addr)
            # Colocar en bus de datos
            self.data_bus = data
        else:
            # Dirección no mapeada
            data = Bus(self.data_bus.width, 0xFFFF)  # Valor de error
            self.data_bus = data
        
        self.clock_cycles += 1
        
        if master_name:
            self._release_bus(master_name)
            
        return data
    
    def write(self, address: int, data: Bus, master_name: str = None):
        """
        Escribe en la dirección especificada
        
        Args:
            address: Dirección absoluta
            data: Dato a escribir
            master_name: Nombre del maestro que escribe
        """
        if master_name and not self._request_bus(master_name):
            return
        
        # Colocar dirección y dato en los buses
        self.address_bus.set_Binary_value(address)
        self.data_bus = data
        
        # Buscar dispositivo
        dev_info, rel_addr = self.find_device(address)
        if dev_info:
            # Escribir en el dispositivo
            dev_info['device'].write(rel_addr, data)
        
        self.clock_cycles += 1
        
        if master_name:
            self._release_bus(master_name)
    
    def _request_bus(self, master_name: str) -> bool:
        """Solicita control del bus"""
        if self.current_master is None:
            self.current_master = master_name
            self.bus_grant.set_value(1)
            return True
        
        # Si ya hay un maestro, esperar (en hardware real habría prioridades)
        # Por simplicidad, denegamos si ya hay otro maestro
        return False
    
    def _release_bus(self, master_name: str):
        """Libera control del bus"""
        if self.current_master == master_name:
            self.current_master = None
            self.bus_grant.set_value(0)
    
    def reset(self):
        """Resetea el bus"""
        self.data_bus.set_Binary_value(0)
        self.address_bus.set_Binary_value(0)
        self.control_bus.set_Binary_value(0)
        self.bus_request.set_value(0)
        self.bus_grant.set_value(0)
        self.current_master = None
        self.clock_cycles = 0
    
    def get_status(self):
        """Retorna estado del bus"""
        return {
            'address': self.address_bus.get_Hexadecimal_value(),
            'data': self.data_bus.get_Hexadecimal_value(),
            'control': self.control_bus.get_Binary_value(),
            'current_master': self.current_master,
            'cycles': self.clock_cycles
        }
    
    def __str__(self):
        status = self.get_status()
        return (f"SystemBus(Addr={status['address']}, Data={status['data']}, "
                f"Master={status['current_master']}, Cycles={status['cycles']})")