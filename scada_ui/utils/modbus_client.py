# scada_ui/utils/modbus_client.py

from pymodbus.client import ModbusTcpClient

def read_modbus_register(ip, port, address):
    try:
        client = ModbusTcpClient(ip, port=port)
        result = client.read_input_registers(address, count=1)
        client.close()
        if result and not result.isError():
            return result.registers[0]
    except:
        pass
    return None
